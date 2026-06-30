import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash-latest")

response = model.generate_content("Hello")

print(response.text)
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

for model in genai.list_models():
    print(model.name)
    from openai import OpenAI

print("OpenAI imported successfully")