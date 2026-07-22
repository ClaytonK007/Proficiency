import requests

RANDOM_VERSE = "https://labs.bible.org/api/?passage=random&type=json"

FALLBACK_VERSE = {
    "text": "Trust in the LORD with all thine heart; and lean not unto thine own understanding.",
    "reference": "Proverbs 3:5",
}

def get_random_quote():
    try:
        response = requests.get(RANDOM_VERSE, timeout=5)
        response.raise_for_status()
        data = response.json()[0]

        text = data["text"].strip()
        reference = f"{data["bookname"]} {data["chapter"]}:{data["verse"]}"
        return {"text": text, "reference": reference}

    except (requests.RequestException, KeyError, IndexError, ValueError):
        return FALLBACK_VERSE
