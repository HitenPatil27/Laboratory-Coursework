from groq import Groq
from serpapi.google_search import GoogleSearch
import json

# Initialize clients with your API keys
groq_client = Groq(api_key="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")
serpapi_key = "664fd8b77cf97d5fbe7e8cbe41515f64e9725f171667d8cd9cf939ffcf441492"

def web_search_agent(user_query):
    # Fixed system prompt
    system_prompt = "You are a helpful web search agent. Provide real-time, relevant, and accurate responses based on the provided search results."
    
    # Fixed user prompt template
    user_prompt_template = """
    User Query: {query}
    
    Search Results:
    {search_summary}
    
    Respond concisely and informatively. If the results don't directly answer the query, note that and suggest related insights.
    """
    
    # Step 1: Perform web search using SerpApi
    search_params = {
        "q": user_query,
        "api_key": serpapi_key,
        "num": 10  # Number of search results
    }
    
    search = GoogleSearch(search_params)
    search_results = search.get_dict()
    
    # Extract relevant snippets from organic results
    organic_results = search_results.get('organic_results', [])
    snippets = []
    for result in organic_results:
        title = result.get('title', '')
        snippet = result.get('snippet', '')
        link = result.get('link', '')
        snippets.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n")
    
    search_summary = "\n".join(snippets[:5])  # Limit to top 5 for brevity
    
    # Step 2: Format user prompt
    user_prompt = user_prompt_template.format(query=user_query, search_summary=search_summary)
    
    # Step 3: Prompt Groq LLM with system and user messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.1  # Low temperature for accuracy
    )
    
    agent_response = response.choices[0].message.content.strip()
    return agent_response

# Interactive usage: Get query from user input
if __name__ == "__main__":
    query = input("Enter your query: ")
    response = web_search_agent(query)
    print("\nResponse:")
    print(response)