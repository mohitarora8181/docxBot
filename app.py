import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("openai_api_key")
openai.api_base = os.getenv("openai_api_base")
openai.api_version = os.getenv("openai_api_version")
openai.api_type = os.getenv("openai_api_type")

history = []

while True:
    inputStr = input("Enter the prompt :-  ")

    history.append({"role":"user","content":f"{inputStr}"})

    chat = openai.ChatCompletion.create(
                    engine="gpt-35-turbo", 
                    messages=history,
                    temperature=0.7, 
                    top_p=0.95, 
                    max_tokens=800, 
                    frequency_penalty=0, 
                    presence_penalty=0
                )
    content = chat.choices[0].message.content
    history.append({"role":"assistant","content":f"{content}"})
    print(content)
