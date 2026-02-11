from datetime import datetime
from mysql.connector import Error
from backend.sql import execQy, fOne, fAll
from backend.constants import LIBRARIAN_HEADERS, MEMBER_HEADERS
from backend.utils import encrypt_password, decrypt_password, validate_fields

HEADERS_MAP = {
    "Librarian": LIBRARIAN_HEADERS,
    "Members": MEMBER_HEADERS,
}

def _validate_user_type(db): 
    if db not in HEADERS_MAP:
        raise ValueError("Error: Invalid user type.")

def _validate_mobile(mobile):
    if not (mobile and mobile.isdigit() and len(mobile) == 10):
        raise ValueError("Error: Invalid mobile number.")

def _ensure_email_exists(db, email):
    row = fOne(f"SELECT Password FROM {db} WHERE EmailID = %s", (email,))
    if not row:
        raise ValueError("Error: Email not found.")
    return decrypt_password(row[0])

def _ensure_member_exists(email):
    row = fOne("SELECT Points FROM Members WHERE EmailID = %s", (email,))
    if not row:
        raise ValueError("Error: Member not found.")
    return row[0]

def signup_user(db, email, fullname, password, mobile):
    try:
        _validate_user_type(db)
        if not all([email, fullname, password, mobile]):
            return "Error: All fields are required."
        _validate_mobile(mobile)
        if fOne(f"SELECT 1 FROM {db} WHERE EmailID = %s", (email,)):
            return "Error: Email already registered."

        execQy(
            f"INSERT INTO {db} (EmailID, FullName, Password, MobileNumber) VALUES (%s, %s, %s, %s)",
            (email, fullname, encrypt_password(password), mobile),
        )
        return "Signup successful."
    except (ValueError, Error) as e:
        return str(e)
    except Exception as e:
        return f"Error: {e}"

def signin_user(db, email, password):
    try:
        _validate_user_type(db)
        if not email or not password:
            return "Error: Email and password are required."

        stored_pwd = _ensure_email_exists(db, email)
        if password != stored_pwd:
            return "Error: Invalid email or password."

        execQy(f"UPDATE {db} SET LastLoginOn = %s WHERE EmailID = %s", (datetime.now(), email))
        return "Login successful."
    except (ValueError, Error) as e:
        return str(e)
    except Exception as e:
        return f"Error: {e}"

def update_user(db, email, old_password, fullname=None, mobile=None, new_password=None):
    try:
        _validate_user_type(db)
        if not email or not old_password:
            return "Error: Email and old password are required."

        if old_password != _ensure_email_exists(db, email):
            return "Error: Old password is incorrect."

        fields, values = [], []
        if fullname: fields += ["FullName = %s"]; values += [fullname]
        if mobile:
            _validate_mobile(mobile)
            fields += ["MobileNumber = %s"]; values += [mobile]
        if new_password: fields += ["Password = %s"]; values += [encrypt_password(new_password)]

        if not fields:
            return "Error: Nothing to update."

        values.append(email)
        execQy(f"UPDATE {db} SET {', '.join(fields)} WHERE EmailID = %s", tuple(values))
        return "Update successful."
    except (ValueError, Error) as e:
        return str(e)
    except Exception as e:
        return f"Error: {e}"

def delete_user(db, email, password, librarianEmail=None):
    try:
        _validate_user_type(db)
        if not email or not password:
            return "Error: Email and password are required."

        admin_pwd = _ensure_email_exists("Librarian", librarianEmail)
        if admin_pwd != password:
            return "Error: Incorrect password."

        execQy(f"DELETE FROM {db} WHERE EmailID = %s", (email,))
        return "Account deleted successfully."
    except (ValueError, Error) as e:
        return str(e)
    except Exception as e:
        return f"Error: {e}"

def get_user(db, fields=None, email=None, count=False, bool=False):
    try:
        _validate_user_type(db)
        selected_fields = validate_fields(fields, HEADERS_MAP[db]) if fields else "*"
        if selected_fields == "INVALID":
            return "Error: Invalid field(s) provided."

        if email:
            row = fOne(f"SELECT {selected_fields} FROM {db} WHERE EmailID = %s", (email,))
            return (row is not None if bool else row or f"{db[:-1]} not found.")

        if count:
            row = fOne(f"SELECT COUNT(*) FROM {db}")
            return row[0] if row else 0

        return fAll(f"SELECT {selected_fields} FROM {db}")
    except (ValueError, Error) as e:
        return False if bool else str(e)
    except Exception as e:
        return False if bool else f"Error: {e}"

def wishlist_mem(email, isbn, action):
    try:
        if not all([email, isbn, action]):
            return "Error: Email, ISBN, and action are required."
        if not (isbn.isdigit() and len(isbn) in (10, 13)):
            return "Error: Invalid ISBN."
        if action not in ("added", "removed"):
            return "Error: Action must be 'added' or 'removed'."

        row = fOne("SELECT WishlistedBooks FROM Members WHERE EmailID = %s", (email,))
        if not row:
            return "Error: Member not found."

        wishlist = row[0].split(",") if row[0] else []

        if action == "added":
            if isbn in wishlist: return "Error: ISBN already in wishlist."
            wishlist.append(isbn)
        else:
            if isbn not in wishlist: return "Error: ISBN not in wishlist."
            wishlist.remove(isbn)

        execQy("UPDATE Members SET WishlistedBooks = %s WHERE EmailID = %s", (",".join(wishlist), email))
        return f"{action.title()} book in wishlist."
    except (ValueError, Error) as e:
        return str(e)
    except Exception as e:
        return f"Error: {e}"

def add_points_mem(email, isbn, val=10):
    try:
        if not email or not isbn:
            return "Error: Email and ISBN are required."

        if not fOne("SELECT 1 FROM Books WHERE ISBN = %s", (isbn,)):
            return "Error: Book not found."

        current_points = _ensure_member_exists(email)
        execQy("UPDATE Members SET Points = %s WHERE EmailID = %s", (current_points + val, email))
        return val
    except (ValueError, Error) as e:
        return str(e)
    except Exception as e:
        return f"Error: {e}"

def redeem_points_mem(email, points):
    try:
        if not email or not points:
            return "Error: Email and points are required."
        if not str(points).isdigit() or int(points) <= 0:
            return "Error: Invalid points."

        points = int(points)
        current_points = _ensure_member_exists(email)
        if current_points < points:
            return "Error: Insufficient points."

        execQy("UPDATE Members SET Points = %s WHERE EmailID = %s", (current_points - points, email))
        return f"{points} points redeemed. New total: {current_points - points}."
    except (ValueError, Error) as e:
        return str(e)
    except Exception as e:
        return f"Error: {e}"
