from rapidfuzz import fuzz

def keyword_score(user_question, db_question):

    user_words = set(user_question.split())
    db_words = set(db_question.split())

    common = user_words.intersection(db_words)

    return len(common) * 10