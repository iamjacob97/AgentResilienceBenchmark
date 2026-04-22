import os
import openai
import dotenv

# loading secrets from the .env file
dotenv.load_dotenv()

# retrieve key-values from the environment
API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("BASE_URL")
MODEL_NAME = os.environ.get("MODEL_NAME")


if not API_KEY or not BASE_URL or not MODEL_NAME:
    raise ValueError("Credentials missing. Check environment file...")

# initialise openai client
client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)

def run_test():
    print("Initialising connection test...")

    try:
        print(f"Attempting request with {MODEL_NAME}.")

        response = client.responses.create(
            model=MODEL_NAME,
            instructions="You are a helpful assistant.",
            input="Say 'API Connection Successful!' and nothing else.",
            timeout=7.0,
        )

        print("\n[SUCCESS] response received:")
        print(response.output_text)

    except (openai.RateLimitError, openai.APIStatusError) as e:
        status = getattr(e, "status_code", "unknown")
        print(f"[ERROR] failed with code: {status}")
        print(e.message)

    except openai.APIConnectionError:
        print("[NETWORK ERROR] could not reach server...")

    finally:
        print("Test Complete.")

if __name__ == "__main__":
    run_test()