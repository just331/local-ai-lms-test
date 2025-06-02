import csv
import os
from datetime import datetime

LOGFILE = "submission_log.csv"


def log_submission(user_id, lesson_id, submission, feedback, tokens_used, prompt_tokens, completion_tokens):
    """
    Log the submission details to a CSV file.
    """
    if not os.path.exists(LOGFILE):
        with open(LOGFILE, mode='w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "user_id", "lesson_id", "submission", "tokens_used", "prompt_tokens", "completion_tokens", "feedback"])

    with open(LOGFILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().isoformat(),
            user_id,
            lesson_id,
            submission,
            tokens_used,
            prompt_tokens,
            completion_tokens,
            feedback,
        ])
