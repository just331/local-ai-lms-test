from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
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
    submission: str
    # submission_type: str


@app.post("/api/feedback/")
def give_feedback(submission: Submission):
    try:
        lesson = lesson_rubrics.get(submission.lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        feedback = evaluate_submission(
            submission.submission,
            lesson["definition"],
            lesson["rubric"],
            lesson["expected_keywords"],
        )
        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
