import google.generativeai as genai
from config import GEMINI_API_KEY

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_model():
    """Initializes and returns the Gemini model."""
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key is not configured. Please set it in your .env file.")
    return genai.GenerativeModel('gemini-1.5-flash')

def detect_intent(user_message):
    """
    Uses Gemini to detect the user's intent ('summarize', 'translate', 'qa').
    """
    model = get_model()
    prompt = f"""
    Analyze the user's message to determine the primary intent.
    Possible intents are: 'summarize', 'translate', 'sentiment', or 'qa'.
    - 'summarize': User wants a summary.
    - 'translate': User wants to translate the transcript.
    - 'sentiment': User is asking for sentiment analysis.
    - 'qa': User is asking a specific question.
    Default to 'summarize' if the intent is unclear.

    User Message: "{user_message}"

    Respond with only one word: summarize, translate, sentiment, or qa.
    """
    try:
        response = model.generate_content(prompt)
        intent = response.text.strip().lower()
        # Basic validation to ensure the response is one of the expected intents
        if intent in ['summarize', 'translate', 'sentiment', 'qa']:
            return intent
        return 'qa'
    except Exception as e:
        print(f"Error in intent detection: {e}")
        return 'qa'

def detect_language(user_message):
    """
    Uses Gemini to detect the target language for translation from the user message.
    """
    model = get_model()
    prompt = f"""
    Analyze the following user message, which requests a translation.
    Identify the target language.
    If no specific language is mentioned, default to 'English'.
    Respond with only the name of the language (e.g., "Spanish").

    User Message: "{user_message}"
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in language detection: {e}")
        return 'English'  # Default to English if detection fails

def process_with_gemini(transcript, user_message, intent, language=None):
    """
    Generates a response from Gemini based on the detected intent.
    """
    model = get_model()
    prompt = ""
    if intent == 'summarize':
        prompt = f"Summarize the following YouTube transcript in a concise paragraph:\n\nTranscript:\n{transcript}"
    elif intent == 'translate':
        lang = language if language else 'French'
        prompt = f"Translate the following YouTube transcript to {lang}:\n\nTranscript:\n{transcript}"
    elif intent == 'sentiment':
        prompt = f"Analyze the sentiment of the following YouTube transcript and provide a brief summary of the overall sentiment:\n\nTranscript:\n{transcript}"
    elif intent == 'qa':
        prompt = f"Based on the provided YouTube transcript, answer the user's question.\n\nTranscript:\n{transcript}\n\nQuestion:\n{user_message}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Sorry, there was an error processing your request with the AI model: {e}"