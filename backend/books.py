from mysql.connector import Error
from backend.sql import execQy, fAll, fOne
from backend.inventory import delete_book_inv

def add_book_det(isbn, title, author, publication, genre, language, description=None):
    try:
        if not all([isbn, title, author, publication, genre, language]):
            return "Error: All fields except description are required."
        if not isbn.isdigit() or len(isbn) not in (10, 13):
            return "Error: Invalid ISBN. Must be 10 or 13 digits."
        if fOne("SELECT 1 FROM Books WHERE ISBN = %s", (isbn,)):
            return "Error: This book already exists."

        execQy("""
            INSERT INTO Books (ISBN, Title, Description, Author, Publication, Genre, Language)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (isbn, title, description, author, publication, genre, language))
        return "Book added successfully."
    except Error as e:
        return f"Database Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def update_book_det(isbn, title=None, description=None, genre=None, author=None, publication=None, language=None, review=None):
    try:
        if not isbn or not isbn.isdigit() or len(isbn) not in (10, 13):
            return "Error: Invalid ISBN. Must be 10 or 13 digits."
        if not fOne("SELECT 1 FROM Books WHERE ISBN = %s", (isbn,)):
            return "Error: Book not found."

        fields, values = [], []
        for col, val in [("Title", title), ("Description", description), ("Author", author),
                         ("Publication", publication), ("Genre", genre), ("Language", language), ("Review", review)]:
            if val:
                fields.append(f"{col} = %s")
                values.append(val)

        if not fields:
            return "Error: Nothing to update."

        values.append(isbn)
        execQy(f"UPDATE Books SET {', '.join(fields)} WHERE ISBN = %s", tuple(values))
        return "Book updated successfully."
    except Error as e:
        return f"Database Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def delete_book_det(isbn):
    try:
        if not isbn or not isbn.isdigit() or len(isbn) not in (10, 13):
            return "Error: Invalid ISBN. Must be 10 or 13 digits."
        if not fOne("SELECT 1 FROM Books WHERE ISBN = %s", (isbn,)):
            return "Error: Book not found."

        execQy("DELETE FROM Books WHERE ISBN = %s", (isbn,))
        delete_book_inv(isbn=isbn)
        return "Book deleted successfully."
    except Error as e:
        return f"Database Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def get_book_det(isbn=None, title=None, author=None, publication=None, genre=None, language=None):
    try:
        if not any([isbn, title, author, publication, genre, language]):
            rows = fAll("SELECT * FROM Books")
            return rows if rows else "Error: No books found."

        if isbn and (not isbn.isdigit() or len(isbn) not in (10, 13)):
            return "Error: Invalid ISBN. Must be 10 or 13 digits."

        conditions, values = [], []
        for col, val in [("ISBN", isbn), ("Title", title), ("Author", author),
                         ("Publication", publication), ("Genre", genre), ("Language", language)]:
            if val:
                op = "LIKE" if col != "ISBN" else "="
                val = f"%{val}%" if op == "LIKE" else val
                conditions.append(f"{col} {op} %s")
                values.append(val)

        query = "SELECT * FROM Books WHERE " + " AND ".join(conditions)
        return fAll(query, tuple(values))
    except Error as e:
        return f"Database Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def get_books_list(isbns):
    try:
        if not isbns or any(not i.isdigit() or len(i) not in (10, 13) for i in isbns):
            return "Error: Invalid ISBNs. Must be 10 or 13 digits."

        query = f"SELECT * FROM Books WHERE ISBN IN ({','.join(['%s'] * len(isbns))})"
        rows = fAll(query, tuple(isbns))
        return rows if rows else "Error: No books found."
    except Error as e:
        return f"Database Error: {e}"
    except Exception as e:
        return f"Error: {e}"
