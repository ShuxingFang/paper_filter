import os
from openai import OpenAI
import json
from collections import defaultdict


def ask_gpt(client, criteria, title, abstract):
    prompt = f"""
Given the following paper information:

Title: {title}
Abstract: {abstract}

Determine whether the paper should be disqualified based on the following criteria (type: explaination):
{criteria}

As soon as the paper meets any one of the above disqualification criteria, it should be disqualified.

Your task is to:

- Decide whether the paper should be disqualified.
- If disqualified, provide the type of the first applicable disqualification reason from the list above, without any further explanation.
- If not disqualified, simply state that the paper is approved.

Respond in the following JSON format without any additional text:

{{
"disqualified": true or false,
"reason": "Disqualification type here" or null
}}
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": "You are an assistant that helps filter academic papers based on specific criteria."},
                {"role": "user", "content": prompt}
            ]
        )

        content = completion.choices[0].message.content.strip()
        result = json.loads(content)
        return result['disqualified'], result.get('reason', '')
    except Exception as e:
        print(f"An error occurred while processing the paper titled '{title}': {e}")
        return True, 'Error in API call'

def check(criteria):
    with open("data/parsed/cleaned_papers.json", "r") as f:
        papers= json.load(f)

    approved_papers = []
    disqualified_papers = []
    disqualification_counts = defaultdict(int)
    counter = 0
    client = OpenAI()
    print("paper filtering begins")

    for paper in papers:
        is_disqualified, reason = ask_gpt(client, criteria, paper["title"], paper["abstract"])
        if is_disqualified:
            disqualification_counts[reason] += 1
            disqualified_papers.append(paper)
        else:
            approved_papers.append(paper)
        counter += 1
        print(f"{counter} / {len(papers)}" , end="\r")

    with open("output/approved_papers.json", "w") as file:
        json.dump(approved_papers, file, indent=4)
        print(f"{len(approved_papers)} papers approved")


    with open("output/disqualified_papers.json", "w") as file:
        data = {
            "counts": disqualification_counts,
            "list": disqualified_papers
        }
        json.dump(data, file, indent=4)
        print(f"{len(disqualified_papers)} papers disqualified")
