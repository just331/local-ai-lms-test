import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from lesson_data import lesson_canonicals

from lesson_training_data import answers
from classifier_utils import classify_submission_category

with open("curated_feedback.json", "r", encoding="utf-8") as f:
    feedback_bank = json.load(f)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Submission(BaseModel):
    lesson_id: str
    question_id: str
    submission: str
    # submission_type: str
    # user_id: str
    # llm: str = "openai"  # or "gemini"


@app.post("/api/feedback/")
def give_feedback(submission: Submission):
    try:
        lesson = lesson_canonicals.get(submission.lesson_id)
        question = lesson.get(submission.question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found in the lesson")
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        # Fetch training data for this question
        sample_sets = answers[submission.lesson_id][submission.question_id]
        correct = sample_sets.get("correct", [])
        partial = sample_sets.get("partial", [])
        nonsense = sample_sets.get("nonsense", [])
        # Classify
        category = classify_submission_category(submission.submission, correct, partial, nonsense)
        feedback = feedback_bank[submission.lesson_id][submission.question_id][category]
        print(category)
        print(feedback)
        return {
            "category": category,
            "feedback": feedback
        }

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
