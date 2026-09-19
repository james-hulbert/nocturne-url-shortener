import string
import random
from app.database import get_db_connection
from flask import request_tearing_down


def generate_short_code(length: int = 6) -> str:
    """Generates a random mix of letters and numbers for the short URL code."""
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))

def create_url_mapping(target_url: str) -> str:
    """Saves the original URL and a generate short code into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Generate a unique short code
    short_code = generate_short_code()

    # Insert it into our SQLite database
    cursor.execute(
        "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
        (target_url, short_code)
    )

    conn.commit()
    conn.close()

    return short_code

def get_url_by_code(short_code: str):
    """ Looks up a short code in the database to retrieve the original URL and click count."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM urls WHERE short_code = ?", (short_code,))
    row = cursor.fetchone()

    conn.close()
    return row

def increment_clicks(short_code: str):
    """Increments the click counter every time a short link is visited."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (short_code,))

    conn.commit()
    conn.close()