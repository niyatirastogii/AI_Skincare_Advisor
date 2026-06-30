from openai import OpenAI

client = OpenAI(
    api_key="YOUR_OPENAI_API_KEY"
)

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Hello"
)

print(response.output_text)