# 3. Google Gemini + Conversation History + Real-Time Search

from google import genai

API_KEY = "AIzaSyAH3_p3YEpd9ZZez-2dbwM09zYgBIF49Bs"

client = genai.Client(api_key=API_KEY)

print("Gemini Chatbot Started")

while True:
    msg = input("You: ")

    if msg.lower() == "exit":
        break

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=msg
        )

        print("Bot:", response.text)

    except Exception as e:
        print("Error:", e)