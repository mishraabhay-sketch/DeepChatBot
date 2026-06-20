import sqlite3
from rapidfuzz import fuzz
from ai_brain import ask_ai
from memory_manager import (get_memory,  get_memory_history)
DB = "data/chatbot.db"

def get_answer(user_question, language, username):

    q = user_question.lower()
    
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "SELECT question, answer FROM knowledge"
    )

    rows = cur.fetchall()

    conn.close()

    best_score = 0
    best_answer = None

    for question, answer in rows:
        
        score = max(

            fuzz.ratio(
                user_question.lower(),
                question.lower()
            ),

            fuzz.token_sort_ratio(
                user_question.lower(),
                question.lower()
            )
        )

        print(
            "DB Question =",
            question,
            " | Score =",
            score
        )

        if score > best_score:

            best_score = score
            best_answer = answer

    print("Best Score =", best_score)
    print("Best Answer =", best_answer)

    question_lower = user_question.lower()

    # ==========================
    # MEMORY RECALL
    # ==========================

    if q in [
        "what is my name",
        "mera naam kya hai",
        "my name?"
    ]:

        name = get_memory(
            username,
            "name"
        )

        if name:
            return f"Your name is {name}."

        return "I don't know your name yet."


    elif q in [
        "what is my previous name",
        "previous name",
        "mera purana naam kya tha",
        "old name"
    ]:

        names = get_memory_history(
            username,
            "name"
        )

        if len(names) >= 2:
            return f"Your previous name was {names[1]}."

        return "No previous name found."
    
    # if (
    #     "what is my name" in question_lower
    #     or "my name" in question_lower
    #     or "mera naam kya hai" in question_lower
    # ):

    #     saved_name = get_memory(
    #         username,
    #         "name"
    #     )

    #     if saved_name:

    #         if language == "Hindi":

    #             return f"आपका नाम {saved_name} है।"

    #         elif language == "Hinglish":

    #             return f"Tumhara naam {saved_name} hai."

    #         elif language == "Roman Hindi":

    #             return f"Tumhara naam {saved_name} hai."

    #         else:
 
    #             return f"Your name is {saved_name}."
    
    if best_score >= 70:

        print("RETURNING KNOWLEDGE =", best_answer)
        return best_answer

    print("Using AI Brain...")

    ai_answer = ask_ai(
        user_question,
        language, 
        username
    )

    print("AI Returned:", ai_answer[:100])

    return ai_answer