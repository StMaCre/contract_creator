# google_setup.py (Simplified Version)
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from dotenv import load_dotenv
import os

# Load environment variables (API Key)
load_dotenv()
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY not found in environment variables. Please create a .env file with API_KEY=YOUR_API_KEY.")

# Configure the generativeai library
genai.configure(api_key=api_key)

def setup_genai_client(model_name="gemini-1.5-flash-latest"):
    """
    Sets up the Google GenAI client and returns a text generation function.

    Args:
        model_name (str): The name of the Gemini model to use.

    Returns:
        function: A function that takes a prompt and optional config,
                  and returns the generated text.
    """
    try:
        model = genai.GenerativeModel(model_name)
        print(f"Successfully initialized model: {model_name}")

        def generate_text(prompt, config=None):
            generation_config = config or GenerationConfig(
                temperature=0.2, # Default low temperature
            )
            try:
                response = model.generate_content(
                    contents=[prompt],
                    generation_config=generation_config
                )
                # Basic check for response content
                if response.candidates:
                    # Handle potential lack of 'text' if parts are blocked/empty
                    if hasattr(response.candidates[0].content.parts[0], 'text'):
                       return response.text # Access text safely
                    else: 
                       print("Warning: Response part generated but contains no text.")
                       return "[[NO TEXT IN RESPONSE PART]]"

                else:
                    blockage_info = response.prompt_feedback if hasattr(response, 'prompt_feedback') else 'No details provided.'
                    print(f"Warning: Response blocked or empty. Reason: {blockage_info}")
                    return "[[RESPONSE BLOCKED/EMPTY]]"
            except Exception as e:
                print(f"Error during text generation: {e}")
                return f"[[GENERATION ERROR: {e}]]"

        return generate_text # Return ONLY the generation function

    except Exception as e:
        print(f"Error setting up GenAI client for model {model_name}: {e}")
        raise # Re-raise the exception to stop execution if setup fails