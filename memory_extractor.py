import re

def extract_memory(text):

    memories = []

    patterns = [

    (r"(?:my name is|i am|i'm)\s+(.+)", "name"),

    (r"i am from (.+)", "city"),

    (r"(?:i live in|i am from)\s+(.+)", "city"),

    (r"my city is (.+)", "city"),

    (r"my favorite color is (.+)", "favorite_color"),

    (r"i am (\d+) years old", "age"),

    (r"mera naam (.+) hai", "name"),

    (r"mai (.+) hu", "name"),

    (r"main (.+) hu", "name"),

    (r"mai (.+) se hu", "city"),

    (r"main (.+) se hu", "city"),

    (r"mai (.+) me rehta hu", "city"),

    (r"main (.+) me rehta hu", "city"),

    (r"meri favourite color (.+) hai", "favorite_color"),

    (r"mera favorite color (.+) hai", "favorite_color"),

]

    lower_text = text.lower()

    for pattern, key in patterns:

        match = re.search(
            pattern,
            lower_text
        )

        if match:

            start = match.start(1)
            end = match.end(1)

            value = text[start:end].strip()

            memories.append(
                (key, value)
            )

    return memories