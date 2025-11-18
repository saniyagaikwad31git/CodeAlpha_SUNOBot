import google.generativeai as genai

# Your API Key
genai.configure(api_key="AIzaSyDY_kpM0SZWvWaP2gP22LayrUPhVdvPkNU")

model = genai.GenerativeModel("gemini-2.5-flash")

print("Chatbot is ready! Type your question:")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    
    response = model.generate_content(user_input)
    print("Bot:", response.text)