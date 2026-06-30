import google.generativeai as genai
import json
import re
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_api_key():
    """
    Retrieves the Gemini API Key.
    Prioritizes Streamlit secrets, then environment variables, and finally a working fallback.
    """
    # 1. Try streamlit secrets first
    try:
        if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    
    # 2. Try environment variable
    env_key = os.getenv("GEMINI_API_KEY")
    if env_key:
        # Check if it starts with 'sk-', which is an OpenAI key. If so, don't use it for Gemini.
        if not env_key.startswith("sk-"):
            return env_key
            
    # 3. Hardcoded fallback key from test_gemini.py
    return None

def analyze_skin_image(image):
    """
    Sends the skin image to Gemini for analysis.
    Returns parsed JSON data or an error dict.
    """
    api_key = get_api_key()
    if not api_key:
        return {"error": "API Key not configured."}
        
    try:
        genai.configure(api_key=api_key)
        # Use gemini-2.5-flash as it is supported by the API key
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = """
You are an expert dermatological advisor. Carefully analyze this skin or face photo.
Identify any visible skin issues, determine the likely skin type, and provide recommendations.

You MUST respond ONLY with a valid JSON object. Do NOT include any markdown code fences, backticks, or other text outside the JSON.

Expected JSON schema:
{
  "skin_type": "Oily / Dry / Combination / Normal / Sensitive",
  "skin_issues": [
    {
      "issue": "e.g., Acne / Redness / Dry patches / Fine lines",
      "severity": "Mild / Moderate / Severe",
      "description": "Brief description of the issue seen"
    }
  ],
  "recommended_ingredients": [
    "e.g., Salicylic Acid",
    "e.g., Niacinamide"
  ],
  "recommended_products": [
    "e.g., Cetaphil Gentle Skin Cleanser",
    "e.g., La Roche-Posay Effaclar Duo"
  ],
  "home_remedies": [
    {
      "remedy": "Name of remedy (e.g. Aloe Vera Gel)",
      "instructions": "How to use/apply it",
      "benefits": "Why it helps this specific skin condition"
    }
  ],
  "doctor_advice": "Dermatologist consultation advice based on the severity of issues."
}

If the image is not a photo of human skin or face, return:
{"error": "Please upload a clear close-up image of your skin or face for analysis."}
"""
        response = model.generate_content([prompt, image])
        raw_text = response.text.strip()
        
        # Clean markdown wrappers if present
        raw_text = re.sub(r"^```json\s*", "", raw_text, flags=re.MULTILINE)
        raw_text = re.sub(r"\s*```$", "", raw_text, flags=re.MULTILINE)
        raw_text = raw_text.strip()
        
        # Parse JSON
        result = json.loads(raw_text)
        return result
        
    except json.JSONDecodeError as je:
        # If parsing failed, try finding JSON block inside text using regex
        try:
            match = re.search(r"\{.*\}", raw_text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception:
            pass
        return {"error": "Failed to parse analysis response. Please try again.", "raw": raw_text}
        
    except Exception as e:
        return {"error": f"AI Analysis Error: {str(e)}"}
