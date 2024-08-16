import openai

openai.api_key = "46fe65fb0a7a46218fa8f83655c4f31b"
openai.api_base = "https://fixitgptfourindia.openai.azure.com/"
openai.api_version = "2024-02-01"
openai.api_type = "azure"

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