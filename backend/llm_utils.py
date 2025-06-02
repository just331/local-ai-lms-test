import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def evaluate_submission(submission, precise_answer, rubric, expected_keywords):
    prompt = f"""
    You are an expert grader for a course on Answer Set Programming (ASP).

    Acceptable answer: "{precise_answer}"

    Rubric: {chr(10).join(f"- {point}" for point in rubric)}
    Expected keywords or phrases the student should use: {', '.join(expected_keywords)}

    Student's answer: "{submission}"

    Instructions: 1. If the student's answer matches the acceptable answer and covers all rubric points and expected 
    keywords, reply: "Correct. No feedback needed." 2. If not, identify which rubric points or keywords are 
    missing, and suggest what to add or correct. Be constructive, specific, and brief. - If submission is completely 
    off-topic, say so and provide the acceptable answer.

    List missing points or errors explicitly.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    feedback = response.choices[0].message.content.strip()
    tokens_used = response.usage.total_tokens if response.usage else None
    prompt_tokens = response.usage.prompt_tokens if response.usage else None
    completion_tokens = response.usage.completion_tokens if response.usage else None

    return feedback, tokens_used, prompt_tokens, completion_tokens
