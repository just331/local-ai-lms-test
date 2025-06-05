import os
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def get_embedding(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(
        model=model,
        input=text
    )
    return response.data[0].embedding


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def classify_submission_category(user_submission, correct_samples, partial_samples, nonsense_samples,
                                 correct_threshold=0.90, partial_threshold=0.75):
    user_emb = get_embedding(user_submission)
    correct_emb = np.mean([get_embedding(s) for s in correct_samples], axis=0)
    partial_emb = np.mean([get_embedding(s) for s in partial_samples], axis=0)
    nonsense_emb = np.mean([get_embedding(s) for s in nonsense_samples], axis=0)
    sim_correct = cosine_similarity(user_emb, correct_emb)
    sim_partial = cosine_similarity(user_emb, partial_emb)
    sim_nonsense = cosine_similarity(user_emb, nonsense_emb)
    similarities = {
        "fully_correct": sim_correct,
        "partially_correct": sim_partial,
        "off_topic": sim_nonsense
    }
    # Find max similarity
    best_category = max(similarities, key=similarities.get)
    # Optional: Use thresholds
    if best_category == "fully_correct" and sim_correct >= correct_threshold:
        return "fully_correct"
    elif best_category == "partially_correct" and sim_partial >= partial_threshold:
        return "partially_correct"
    else:
        return "off_topic"
