from groq import Groq
import json

client = Groq(api_key="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")

def get_product_info(product_name):
    prompt = f"""
    You are a product info agent. Return the information in JSON format:
    {{
      "product_name": "",
      "price": "",
      "availability": "",
      "rating": ""
    }}
    Product: {product_name}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    text_response = response.choices[0].message.content.strip()
    print("Raw response:", text_response)  # Debug print
    try:
        return json.loads(text_response)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Response content: {text_response}")
        return None

# Run once and exit
if __name__ == "__main__":
    product_info = get_product_info("iPhone 15")
    if product_info:
        print("\nFinal Product Information:")
        print(json.dumps(product_info, indent=2))
    exit()