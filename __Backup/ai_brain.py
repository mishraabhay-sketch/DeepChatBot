import ollama
from memory_manager import (
    get_memory,
    get_memory_history
)

def ask_ai(question, language, username):

    print("AI BRAIN FILE =", __file__)
    # print("PYTHON =", sys.executable)
    print("OLLAMA =", ollama.__file__)
    
    context = ""

    name = get_memory(
        username,
        "name"
    )

    name_history = get_memory_history(
        username,
        "name"
    )

    # print("CONTEXT = ")
    # print(context)
    # print("=" * 50)
    name = get_memory(
        username,
        "name"
        )

    city = get_memory(
        username,
        "city"
    )
    
    prompt = f"""
    You are ChatBot.

    IMPORTANT LANGUAGE RULES:

    If LANGUAGE = English:
    - Reply only in English.

    If LANGUAGE = Hindi:
    - Reply only in Hindi (Devanagari script).

    If LANGUAGE = Hinglish:
    - Reply only in Hinglish.
    - Use Hindi words written in English letters.
    - Example:
        User: Kaise ho?
        AI: Main bilkul theek hu bhai.

    If LANGUAGE = Roman Hindi:
    - Reply only in Roman Hindi.
    - Never use English sentences unless necessary.

    You are continuing a conversation.
    Always answer ONLY the current question.
    Do not change topic.
    Do not ask unrelated questions unless asked.
    
    Current Language:
    {language}

    Known User Information:

    Current Name:
    {name}

    Name History:
    {name_history}

    Rules:
    - Latest name is the current valid name.
    - Older names are previous names.
    - If user asks current name, use latest name.
    - If user asks old name, check history.
    - Never guess.

    Previous Conversation:

    {context}

    Current Question:

    {question}
    """
   
    
    print("LANGUAGE =", language)
    
    language = detect_language(question)

    print("AUTO LANGUAGE =", language)
    
    print("PROMPT =", prompt)
    
    print("STEP 1")

    try:
        print("STEP 2")

        response = ollama.chat(
            model="qwen2.5:7b",
            messages=[
                {
                "role": "system",
                "content": """
            You are ChatBot.

            STRICT RULES:

            - ALWAYS reply in the selected language.
            - NEVER change language yourself.
            - If language is Hinglish, reply only in Hinglish.
            - If language is Hindi, reply only in Hindi.
            - If language is English, reply only in English.
            - Do not translate unless asked.

            STRICT LANGUAGE RULE:
            Do not use any language other than the selected one.
            No Chinese, no English, no mixed scripts.
            
            Example:

            User Language = Hinglish
            AI = Main theek hu bhai.

            User Language = Roman Hindi
            AI = Namaste, aap kaise ho?

            User Language = Hindi
            AI = नमस्ते, आप कैसे हैं?
            """},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        print("RETURNING =", response["message"]["content"][:100])
        print("STEP 3")
        print("RAW RESPONSE =", response)
        
        return response["message"]["content"]


    
    except Exception as e:

        import traceback

        print("STEP ERROR")
        print("AI ERROR =", e)

        traceback.print_exc()

        return (
            "AI Server is currently offline. "
            "Please start Ollama and try again."
        )

def detect_language(text):

    text = text.lower()

    hinglish_words = [
        "kya",
        "kaise",
        "bhai",
        "mera",
        "tum",
        "namaste",
        "haan",
        "nahi",
        "mai",
        "main",
        "acha",
        "accha",
        "theek",
        "badhiya",
        "kaun",
        "kyun",
        "kab",
        "kaha",
        "kaise ho"
    ]

    count = 0

    for word in hinglish_words:
        if word in text:
            count += 1

    if count >= 1:
        return "Hinglish"

    return "English"
   


