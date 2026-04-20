import os
import openai
import dotenv

# loading secrets from the .env file
dotenv.load_dotenv()

# retrieve the key from the environment
API_KEY = os.environ.get("LLM_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Add key to .env.")

# initialise openai client
client = openai.OpenAI(
           api_key=API_KEY,
           base_url="https://api.groq.com/openai/v1"
         )

# select model
MODEL_NAME = "openai/gpt-oss-20b"
FALLBACK_MODEL = "llama-3.1-8b-instant"

def run_test():
    print("Sending test request...")

    response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role":"system","content":"You are a helpful assistant."},
                {"role":"user","content":"Say 'API Connection Successful!' and nothing else."}
              ]
            )
    print("\nResponse received:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    run_test()
