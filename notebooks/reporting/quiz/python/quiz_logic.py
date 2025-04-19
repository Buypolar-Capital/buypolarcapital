# notebooks/reporting/quiz/python/quiz_logic.py

import duckdb
import random
import os

DB_PATH = os.path.join("quiz_data", "questions.duckdb")

def get_random_questions(n=3, seed=None):
    """
    Fetch n random questions from the DuckDB database.
    Returns a list of dictionaries with keys: 'question', 'answer'.
    """
    con = duckdb.connect(DB_PATH)
    query = f"""
        SELECT question, answer
        FROM quiz_questions
        USING SAMPLE {n} ROWS {'(REPEATABLE(' + str(seed) + '))' if seed is not None else ''}
    """
    rows = con.execute(query).fetchall()
    con.close()

    return [{"question": q, "answer": a} for q, a in rows]