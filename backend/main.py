from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from log_utils import log_submission
from lesson_data import lesson_rubrics
from llm_utils import evaluate_submission


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


@app.post("/api/feedback/")
def give_feedback(submission: Submission):
    try:
        lesson = lesson_rubrics.get(submission.lesson_id)
        question = lesson.get(submission.question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found in the lesson")
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        feedback, tokens_used, prompt_tokens, completion_tokens = evaluate_submission(
            submission.submission,
            question["definition"],
            question["rubric"],
            question["expected_keywords"],
        )

        log_submission(
            user_id="test_user",
            lesson_id=submission.lesson_id,
            question_id=submission.question_id,
            submission=submission.submission,
            feedback=feedback,
            tokens_used=tokens_used,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens
        )
        return {"feedback": feedback}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
