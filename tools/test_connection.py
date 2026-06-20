import ollama

print("Connecting...")

client = ollama.Client(host='http://127.0.0.1:11434')

print("Connected")

response = client.chat(
    model='qwen3:8b',
    messages=[
        {'role': 'user', 'content': 'What is AI?'}
    ]
)

print(response)