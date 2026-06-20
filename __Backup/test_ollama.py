import ollama

print("START")

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "What is AI?"
        }
    ]
)

print(response["message"]["content"])