import re

def normalize_question(text):

    text = text.lower().strip()

    text = re.sub(
        r'[^\w\s]',
        '',
        text
    )

    text = " ".join(
        text.split()
    )

    return text