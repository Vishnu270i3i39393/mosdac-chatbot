import json
import requests

with open("scraper/mosdac_data.json", "r", encoding="utf-8") as f:

    data = json.load(f)


qa_pairs = []

def generate_qa(text):
    try:
        prompt = f"""
Given the following content, generate 3 helpful Q&A pairs for users who may ask about this topic.

CONTENT:
{text}

Output format (JSON):
[
  {{"question": "...", "answer": "..."}},
  ...
]
"""
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        result = response.json()
        raw = result['response']

        # attempt to extract JSON safely
        start = raw.find('[')
        end = raw.rfind(']') + 1
        json_text = raw[start:end]

        return json.loads(json_text)

    except Exception as e:
        print("Error generating Q&A:", e)
        return []

for item in data:
    text = item.get("text", "")
    if len(text) > 200:
        print(f"Generating Q&A for: {item.get('title', 'Untitled')}")
        qa = generate_qa(text[:2000])
        qa_pairs.extend(qa)

with open("backend/data/mosdac_qa_pairs.json", "w", encoding="utf-8") as f:
    json.dump(qa_pairs, f, ensure_ascii=False, indent=2)

print(f"\n Saved {len(qa_pairs)} Q&A pairs to mosdac_qa_pairs.json")
