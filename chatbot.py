import sqlite3
from rapidfuzz import fuzz
from ai_brain import ask_ai
from memory_manager import (get_memory, get_recent_context ,get_memory_history)
from knowledge_manager import (get_latest_version_by_question)
from utils import normalize_question
from knowledge_manager import (get_latest_change, get_latest_version_by_question)
from search_engine import keyword_score
DB = "data/chatbot.db"

def get_answer(user_question, language, username):

    q = user_question.lower()
    
    synonyms = {
    "college": "institute",
    "collage": "institute",
    "clg": "institute",
    "hostel time": "hostel rules",
    "library time": "library timing",
    "exam rules": "examination rules"
    }

    for old, new in synonyms.items():
        q = q.replace(old, new)
    
    user_question = q
    user_question = normalize_question(user_question)
    
    
    
    recent_context = get_recent_context(
        username,
        limit=2
    )

    print("RECENT CONTEXT =")
    print(recent_context)
    
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
        
        db_question = normalize_question(question)
        
        fuzzy_score = max(
            fuzz.ratio(user_question, db_question),
            fuzz.token_sort_ratio(user_question, db_question),
            fuzz.token_set_ratio(user_question, db_question),
            fuzz.partial_ratio(user_question, db_question)
        )

        keyword_bonus = keyword_score(
            user_question,
            db_question
        )

        score = fuzzy_score + keyword_bonus

        print(
            "DB Question =",
            question,
            "| Score =",
            score
        )

        print("FUZZY =", fuzzy_score)
        print("KEYWORD =", keyword_bonus)
        print("FINAL =", score)

        if score > best_score:

            best_score = score
            best_answer = answer
            best_question = question
    print("Best Score =", best_score)
    print("Best Answer =", best_answer)

    question_lower = user_question.lower()

    # ==========================
    # MEMORY RECALL
    # ==========================

    if q in ["hi", "hello", "hey"]:
        return "Hello! How can I help you?"

    if "kaise ho" in q:
        return "Main badhiya hu bhai 😄"
    
    if q in ["namaste", "good morning", "good evening"]:
        
        return ask_ai(
            user_question,
            language,
            username,
            None
        )
    
        # add_learning_queue(
        #     user_question,
        #     ai_reply
        # )
    
    if any(x in q for x in [

        "what is my name",
        "who am i",
        "my name",
        "do you know my name",
        "what's my name"

    ]):

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
    
    if (
        "where do i live" in q
        or "my city" in q
        or "mera city" in q
        or "mera shehar" in q
    ):

        city = get_memory(
            username,
            "city"
        )

        if city:
            
            return f"You live in {city}."

        return "I don't know your city yet."
    
    if q in [
        "who am i",
        "tell me about me",
        "do you remember me"
    ]:

        name = get_memory(
            username,
            "name"
        )

        city = get_memory(
            username,
            "city"
        )

        response = []

        if name:
            response.append(
                f"Your name is {name}"
            )

        if city:
            response.append(
                f"You live in {city}"
            )

        if response:
            return ". ".join(response)

        return "I don't know much about you yet."


    print("FINAL BEST SCORE =", best_score)
    print("CHECK =", best_score >= 75)
    print("BEST MATCH =", best_answer)
    
    if best_score >= 85:
        
        

        version = get_latest_version_by_question(question)

        change = get_latest_change(best_question)

        if version:

            old_answer = version[0]
            new_answer = version[1]

            if old_answer != new_answer:

                return f"""

                Current Information:

                {new_answer}

                --------------------

                Previous Information:

                {old_answer}
                """

        if change:

            old_answer = change[0]
            new_answer = change[1]

            return f"""
        Current Information:

        {new_answer}

        ----------------

        Previous Information:

        {old_answer}
        """
        return best_answer
    
    print("Using AI Brain...")
    
    knowledge = None

    if best_score >= 70:
        knowledge = best_answer

    else:
        knowledge = None
    
    return ask_ai(
        user_question,
        language,
        username,
        knowledge
    )
