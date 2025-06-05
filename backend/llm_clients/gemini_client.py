import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def gemini_evaluate_submission(submission, canonical_answer):
    prompt = f"""
    You are an expert grader for a course on Answer Set Programming (ASP), Logic Programming, and Mathematics.

    Here is the canonical answer to a question:
    \"\"\"{canonical_answer}\"\"\"

    User's answer: "{submission}"

    Instructions: 1. Grade the student's submission into one of the following: - "fully_correct": The submission 
    covers everything in the canonical answer. - "partially_correct": The submission is mostly correct but is missing 
    some key points that are vital to the canonical answer. - "off_topic": The answer is irrelevant or not related to 
    the canonical answer.

    2. Give a brief, constructive feedback message for the user, in 1-2 sentences (preferably bullet points if 
    possible). If the submission is fully correct, just say "Correct. No feedback needed.". If it is partially 
    correct, identify the missing key points or keywords and suggest what to add or correct. If the submission is 
    off-topic, state that clearly and give the canonical answer.
    
    Reply ONLY in this JSON format:
    {{
      "grade": "...",
      "feedback": "..."
    }}
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    return response.text.strip()
