import openai

openai.api_key = "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"
SET_MSG = {"role": "system", "content": "Personal assistance"}
MSGS = {}

def get_response(query, asker):
    global MSGS
    if asker not in MSGS:
        MSGS[asker] = [{"role":"user", "content":query}]
    else:
        MSGS[asker].append({"role":"user", "content":query})
    MSGS[asker] = MSGS[asker][-30:]
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[SET_MSG]+MSGS[asker],
        temperature=1.11
    )
    message = completions.choices[0].message.content
    if ("an ai language model" in message.lower() and ("economic" in message.lower() or "current" in message.lower() or "time" in message.lower())):
        message = "Beep Boop, I couldn't find in my memory banks..."
    
    MSGS[asker].append({"role": "assistant", "content": message})
    print(MSGS[asker])
    return message