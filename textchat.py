# Chat with an intelligent assistant in your terminal
from openai import OpenAI

# Point to the local server
# Change localhost with the IP ADDRESS of the computer acting as a server
# itmay be something like "http://192.168.1.52:8000/v1"
client = OpenAI(base_url="http://localhost:8000/v1", 
                api_key="not-needed")
history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
]
print("\033[92;1m")
while True:
    conv_messages = []
    len_context = len(history)
    if len_context > 13:
        print("\033[93;1m")
        print('Limiter passed')
        print("\033[92;1m")
        x=13-4
        conv_messages.append(history[0])
        for i in range(0,x):
            conv_messages.append(history[-x+i])
    else:
        conv_messages = history
    completion = client.chat.completions.create(
        model="local-model", # this field is currently unused
        messages=conv_messages,
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}
    # the first generation is based on the initial messages
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)
    # here we ask the user input and we check if we want to exit the program
    print("\033[91;1m")
    userinput = input("> ")
    if userinput.lower() in ["quit", "exit"]:
        print("\033[0mBYE BYE!")
        break
    history.append({"role": "user", "content": userinput})
    print("\033[92;1m")
