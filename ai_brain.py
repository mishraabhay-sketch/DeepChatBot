import ollama
from memory_manager import (
    get_memory,
    get_memory_history,
    get_recent_context
)

def ask_ai(question, language, username, best_answer):

    print("RECEIVED KNOWLEDGE =", best_answer)
    print("PASSED LANGUAGE =", language)
    print("AI BRAIN FILE =", __file__)
    # print("PYTHON =", sys.executable)
    print("OLLAMA =", ollama.__file__)
    
    auto_language = detect_language(question)

    if language is None:
        language = auto_language
    
    if best_answer is None:
        best_answer = ""
    
    context = get_recent_context(username, limit=2)

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
    
    
    favorite_color = get_memory(
        username,
        "favorite_color"
    )

    age = get_memory(
        username,
        "age"
    )


    print("AUTO LANGUAGE =", language)
    
    
    prompt = f"""
    You are ChatBot.
    
    Current Language:
    {language}
    
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
    
    IMPORTANT KNOWLEDGE RULES:

    - If Knowledge section contains the answer, use it.
    - Prefer Knowledge over your own assumptions.
    - Do not invent facts.
    - If Knowledge is empty, then answer normally.

    Known User Information:
    
    Name: {name}
    City: {city}
    Favorite Color: {favorite_color}
    Age: {age}

    Relevant Knowledge:

    {best_answer if best_answer else "NO KNOWLEDGE FOUND"}

    Current Name:
    {name}

    Current City:
    {city}

    Name History:
    {name_history}

    Previous Conversation:

    {context}

    IMPORTANT:

    Use previous conversation only if the
    current question depends on it.

    Example:

    User: institute timing
    AI: 9 AM to 5 PM

    User: and library?
    AI: Library timing is ...

    Do not ignore follow-up questions.

    Current Question:

    {question}


    Rules:
    - Latest name is the current valid name.
    - Older names are previous names.
    - If user asks current name, use latest name.
    - If user asks old name, check history.
    - Never guess.
    - If Relevant Knowledge is not NO KNOWLEDGE FOUND,
    - answer from that knowledge first.
    - Use Known User Information when relevant.
    - If user asks about himself, use saved memory.
    - Never invent memory.
    """
    
    print("LANGUAGE =", language)

    try:

        response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "system",
            "content": f"""
You are ChatBot.

Current language is:

{language}

VERY IMPORTANT:

Reply ONLY in {language}

Never change language.

If language is English:
Reply only in English.

If language is Hindi:
Reply only in Hindi.

If language is Hinglish:
Reply only in Hinglish.

Never use Chinese.
Never use random Hindi if language is English.
Never mix languages.

Use Relevant Knowledge first.
"""
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)
        print("RETURNING =", response["message"]["content"][:100])

        DEBUG = False

        if DEBUG:
            print(...)
        
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
   


