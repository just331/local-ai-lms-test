from lesson_training_data import answers
from lesson_data import lesson_canonicals
from llm_clients.openai_client import openai_evaluate_submission
from llm_clients.gemini_client import gemini_evaluate_submission
import csv

with open("feedback_log.csv", mode="w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["lesson_id", "question_id", "submission", "category", "llm_name", "llm_feedback",])

    for lesson_id, questions in answers.items():
        for question_id, data in questions.items():
            canonical = lesson_canonicals[lesson_id][question_id]["definition"]
            for category, subs, in data.items():
                for sub in subs:
                    for llm_name, llm_func in [
                        ("openai", lambda sub: openai_evaluate_submission(sub, canonical)),
                        ("gemini", lambda sub: gemini_evaluate_submission(sub, canonical))
                    ]:
                        print(f"Processing {lesson_id} - {question_id} - {category} - {llm_name}...")
                        feedback = llm_func(sub)
                        writer.writerow([
                            lesson_id,
                            question_id,
                            sub,
                            category,
                            llm_name,
                            feedback
                        ])
                        