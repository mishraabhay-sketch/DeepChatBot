import re

def extract_memory(text):

    memories = []

    patterns = [

        (
            r"my name is (.+)",
            "name"
        ),

        (
            r"i live in (.+)",
            "city"
        ),

        (
            r"my favorite color is (.+)",
            "favorite_color"
        ),

        (
            r"i am (\d+) years old",
            "age"
        )
    ]

    text = text.lower()

    for pattern, key in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            value = match.group(1).strip()

            memories.append(
                (key, value)
            )

    return memories