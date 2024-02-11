from openai import OpenAI
import openai
import os

# Set your OpenAI API key here
api_key = "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"

client = OpenAI(api_key=api_key)
email_content = open("first11.txt", "r").read()
completion = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": f"each line is a email.{email_content} Classify user's email into four catagories"}]
)
answer = completion.choices[0].message.content
answer = str(answer)
answer = answer.replace("\\n", "\n")
print(answer)
file_path = "classified11.txt"
with open(file_path, 'w') as file:
    file.write(str(answer))
