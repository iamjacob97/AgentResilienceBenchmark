import os
import openai
import dotenv

# loading secrets from the .env file
dotenv.load_dotenv()

# retrieve the key from the environment
API_KEY = os.environ.get("LLM_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Add key to environment...")

# define model chain
MODEL_CHAIN = [{"id":"primary","name":"openai/gpt-oss-20b"},
               {"id":"fallback","name":"llama-3.1-8b-instant"}]

# initialise openai client
client = openai.OpenAI(
           api_key=API_KEY,
           base_url="https://api.groq.com/openai/v1"
         )

def run_test():
    print("Initialising connection test...")

    for MODEL in MODEL_CHAIN:
        try:
            print(f"Attempting request with {MODEL['id']} model {MODEL['name']}.")

            response = client.responses.create(
                    model=MODEL['name'],
                    input=[
                        {"role":"system","content":"You are a helpful assistant."},
                        {"role":"user","content":"Say 'API Connection Successful!' and nothing else."}
                      ],
                    timeout=10.0
                    )

            print("\n[SUCCESS] response received:")
            print(response.output_text)
            return

        except (openai.RateLimitError, openai.APIStatusError) as e:
            status = getattr(e, "status_code", "unknown")
            print(f"[ERROR] failed with code: {status}")
            print(e.message)

        except openai.APIConnectionError as e:
            print("[NETWORK ERROR] could not reach server...")
                  
    print("All models in the model chain have failed.")

if __name__ == "__main__":
    run_test()
