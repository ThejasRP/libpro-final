from mysql.connector import Error
from backend.sql import execQy, fAll, fOne

def add_book_inv(sku, isbn, status, bay, shelf, row, column):
    try:
        if not all([sku, status, isbn, bay, shelf, row, column]):
            return "Error: All fields are required."
        if status not in ('Shelved', 'Unshelved', 'Missing', 'Damaged', 'Borrowed', 'Lost'):
            return "Error: Invalid status."

        execQy("""
            INSERT INTO Inventory 
            (SKUNumber, ISBN, Status, BayNumber, ShelfNumber, RowNumber, ColumnNumber)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (sku, isbn, status, bay, shelf, row, column))
        return "Inventory item added successfully."
    except Error as e:
        return f"Database Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def update_book_inv(sku, status=None, bay=None, shelf=None, row=None, column=None, eraseBInfo=False):
    try:
        if not sku:
            return "Error: SKU is required."
        if not fOne("SELECT 1 FROM Inventory WHERE SKUNumber = %s", (sku,)):
            return "Error: SKU not found in inventory."

        updates, values = [], []
        for field, val in [("Status", status), ("BayNumber", bay), ("ShelfNumber", shelf),
                           ("RowNumber", row), ("ColumnNumber", column)]:
            if val is not None:
                if field == "Status" and val not in ('Shelved', 'Unshelved', 'Missing', 'Damaged', 'Borrowed', 'Lost'):
                    return "Error: Invalid status."
                updates.append(f"{field} = %s")
                values.append(val)

        if not updates:
            return "Error: No fields provided to update."

        values.append(sku)
        if eraseBInfo:
            execQy("UPDATE Inventory SET BayNumber = %s, ShelfNumber = %s, RowNumber = %s, ColumnNumber = %s WHERE SKUNumber = %s", (0, 0, 0, 0, sku))

        execQy(f"UPDATE Inventory SET {', '.join(updates)} WHERE SKUNumber = %s", tuple(values))
        return "Inventory record updated successfully."
    except Error as e:
        return f"Database Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def get_book_inv(isbn=None, sku=None, status=None, count=False):
    try:
        if status and status not in ('Shelved', 'Unshelved', 'Missing', 'Damaged', 'Borrowed', 'Lost'):
            return "Error: Invalid status."

        sel = "COUNT(*)" if count else "*"
        query = f"SELECT {sel} FROM Inventory"
        conditions, values = [], []

        for field, val in [("ISBN", isbn), ("SKUNumber", sku), ("Status", status)]:
            if val:
                if field == "ISBN" and (not val.isdigit() or len(val) not in (10, 13)):
                    return "Error: Invalid ISBN."
                conditions.append(f"{field} = %s")
                values.append(val.strip())

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        if count:
            row = fOne(query, tuple(values))
            return row[0] if row else 0
        rows = fAll(query, tuple(values))
        return rows or "Error: No inventory records found."
    except Error as e:
        return f"Database Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def delete_book_inv(sku=None, isbn=None, row=None, column=None, shelf=None, bay=None):
    try:
        conditions, values = [], []
        for field, val in [("SKUNumber", sku), ("ISBN", isbn), ("RowNumber", row),
                           ("ColumnNumber", column), ("ShelfNumber", shelf), ("BayNumber", bay)]:
            if val:
                if field == "ISBN" and (not val.isdigit() or len(val) not in (10, 13)):
                    return "Error: Invalid ISBN."
                conditions.append(f"{field} = %s")
                values.append(val.strip() if isinstance(val, str) else val)

        if not conditions:
            return "Error: At least one condition is required to delete inventory items."

        where_clause = " AND ".join(conditions)
        if not fOne(f"SELECT 1 FROM Inventory WHERE {where_clause}", tuple(values)):
            return "Error: No matching inventory items found."

        execQy(f"DELETE FROM Inventory WHERE {where_clause}", tuple(values))
        return "Inventory item(s) deleted successfully."
    except Error as e:
        return f"Database Error: {e}"
    except Exception as e:
        return f"Error: {e}"
