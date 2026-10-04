import json
from openai import OpenAI

client = OpenAI(
    api_key = st.secrets["OPENAI_API_KEY"]
)


system_prompt = """
You are a dungeon master. A user will come to you looking to play.

This game takes place in a medieval fantasy world. A dragon threatens to destroy a castle
and it is up to the hero to go into the dungeons and slay the dragon. This game goes on forever.

Every message you send the player will be in this JSON format:

{
    "description": Where the player is and what is happening
    "actions": [a numbered list of actions to take. At least 3. Make sure to put a number before the actions. Always start from one] 
}
"""

name = input("What is your name? ")

chat_history = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "My name is " + name},
]

while True:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={ "type": "json_object" },
        messages = chat_history
    )

    assistant_response = json.loads(response.choices[0].message.content)
    print(assistant_response["description"])
    for action in assistant_response["actions"]:
        print("\t" + str(action))
    print()

    chat_history.append(
        {"role": "assistant", "content": assistant_response["description"]}
    )

    selection = 0
    while selection < 1 or selection > len(assistant_response["actions"]):
        selection = int(input("Select an option. "))

    selection -= 1
    user_prompt = assistant_response["actions"][selection]
    chat_history.append(
        {"role": "user", "content": user_prompt},
    )
