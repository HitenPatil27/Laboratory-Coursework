import os
import tempfile
from flask import Flask, request, jsonify, send_from_directory
import PyPDF2
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq
import logging
import time

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
os.environ["GROQ_API_KEY"] = "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"
# Function to extract text from PDF
def extract_text_from_pdf(pdf_file_path):
    try:
        with open(pdf_file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            if not text.strip():
                raise ValueError("No text could be extracted from the PDF.")
            return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        raise

# Function to chunk text into smaller pieces
def chunk_text(text, chunk_size=500):
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    current_length = 0
    for sentence in sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length <= chunk_size:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            chunks.append(". ".join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
    if current_chunk:
        chunks.append(". ".join(current_chunk))
    return [chunk for chunk in chunks if chunk.strip()]

# Basic RAG implementation with Groq
class GroqRAG:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set.")
        try:
            self.model = SentenceTransformer(model_name)
            self.client = Groq(api_key=self.api_key)
            self.chunks = []
            self.embeddings = None
            logging.info("GroqRAG initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize GroqRAG: {e}")
            raise

    def process_pdf(self, pdf_file_path):
        try:
            text = extract_text_from_pdf(pdf_file_path)
            self.chunks = chunk_text(text)
            if not self.chunks:
                raise ValueError("No valid text chunks extracted from PDF.")
            self.embeddings = self.model.encode(self.chunks, show_progress_bar=False)
            logging.info(f"Processed PDF with {len(self.chunks)} chunks.")
        except Exception as e:
            logging.error(f"Error processing PDF: {e}")
            raise

    def retrieve(self, query, top_k=3):
        try:
            query_embedding = self.model.encode([query])[0]
            similarities = cosine_similarity([query_embedding], self.embeddings)[0]
            top_k = min(top_k, len(self.chunks))
            top_k_indices = np.argsort(similarities)[-top_k:][::-1]
            results = [(self.chunks[i], similarities[i]) for i in top_k_indices]
            return results
        except Exception as e:
            logging.error(f"Error retrieving chunks for query '{query}': {e}")
            raise

    def generate_response(self, query, retrieved_chunks):
        try:
            context = "\n\n".join([chunk for chunk, _ in retrieved_chunks])
            prompt = f"Context:\n{context}\n\nQuery: {query}\nAnswer the query based on the provided context."
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-70b-8192",
                max_tokens=500
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            logging.error(f"Error generating response for query '{query}': {e}")
            raise

# Initialize RAG
rag = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    global rag
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file uploaded'}), 400
    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf_file.save(tmp_file.name)
            tmp_file_path = tmp_file.name

        # Process the PDF
        rag = GroqRAG()
        rag.process_pdf(tmp_file_path)

        # Attempt to delete the temporary file with retry
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                os.unlink(tmp_file_path)
                logging.info(f"Deleted temporary file: {tmp_file_path}")
                break
            except PermissionError as e:
                logging.warning(f"Attempt {attempt + 1}: Failed to delete {tmp_file_path}: {e}")
                time.sleep(1)  # Wait before retrying
            except Exception as e:
                logging.error(f"Error deleting temporary file {tmp_file_path}: {e}")
                break

        return jsonify({'message': f'PDF processed successfully! Found {len(rag.chunks)} text chunks.'})
    except Exception as e:
        # Attempt to clean up if an error occurs
        if 'tmp_file_path' in locals():
            try:
                os.unlink(tmp_file_path)
            except:
                pass
        return jsonify({'error': f'Error processing PDF: {str(e)}'}), 500

@app.route('/query', methods=['POST'])
def query_pdf():
    global rag
    if not rag:
        return jsonify({'error': 'No PDF processed yet'}), 400
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    try:
        retrieved_chunks = rag.retrieve(query)
        response = rag.generate_response(query, retrieved_chunks)
        chunks = [{'text': chunk, 'score': float(score)} for chunk, score in retrieved_chunks]
        return jsonify({'response': response, 'chunks': chunks})
    except Exception as e:
        return jsonify({'error': f'Error generating response: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)