from mysql.connector import Error
from backend.sql import execQy, fAll, fOne

def add_review(isbn, fullname, email, review, rating):
    try:
        if not all([isbn, fullname, email, review, rating]):
            return "Error: All fields are required."
        if not isbn.isdigit() or len(isbn) not in (10, 13):
            return "Error: Invalid ISBN. Must be 10 or 13 digits."
        if not rating.isdigit() or not (1 <= int(rating) <= 5):
            return "Error: Rating must be an integer between 1 and 5."
        if not fOne("SELECT 1 FROM Books WHERE ISBN = %s", (isbn,)):
            return "Error: Book not found."

        execQy("""
            INSERT INTO Reviews (ISBN, ReviewerName, ReviewerEmail, Rating, Review)
            VALUES (%s, %s, %s, %s, %s)
        """, (isbn, fullname, email, rating, review))
        return "Review added successfully."
    except Error as e:
        return f"Database Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def update_review(isbn, email, review, rating):
    try:
        if not all([isbn, email, review, rating]):
            return "Error: All fields are required."
        if not isbn.isdigit() or len(isbn) not in (10, 13):
            return "Error: Invalid ISBN. Must be 10 or 13 digits."
        if not rating.isdigit() or not (1 <= int(rating) <= 5):
            return "Error: Rating must be an integer between 1 and 5."
        if not fOne("SELECT 1 FROM Books WHERE ISBN = %s", (isbn,)):
            return "Error: Book not found."

        execQy("""
            UPDATE Reviews SET Review = %s, Rating = %s
            WHERE ISBN = %s AND ReviewerEmail = %s
        """, (review, rating, isbn, email))
        return "Review updated successfully."
    except Error as e:
        return f"Database Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def delete_review(isbn, email):
    try:
        if not isbn or not email:
            return "Error: ISBN and email are required."
        if not isbn.isdigit() or len(isbn) not in (10, 13):
            return "Error: Invalid ISBN. Must be 10 or 13 digits."
        if not fOne("SELECT 1 FROM Books WHERE ISBN = %s", (isbn,)):
            return "Error: Book not found."

        execQy("DELETE FROM Reviews WHERE ISBN = %s AND ReviewerEmail = %s", (isbn, email))
        return "Review deleted successfully."
    except Error as e:
        return f"Database Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def get_reviews(isbn):
    try:
        if not isbn or not isbn.isdigit() or len(isbn) not in (10, 13):
            return "Error: Invalid ISBN. Must be 10 or 13 digits."

        reviews = fAll("SELECT * FROM Reviews WHERE ISBN = %s", (isbn,))
        return reviews or "No reviews found for this book."
    except Error as e:
        return f"Database Error: {e}"
    except Exception as e:
        return f"Error: {e}"
