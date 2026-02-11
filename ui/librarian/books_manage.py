import tkinter as tk
from tkinter import ttk, messagebox
from backend.books import add_book_det, delete_book_det, get_book_det, update_book_det

column_widths = {
    "ISBN": 30,
    "Title": 10,
    "Description": 130,
    "Author": 10,
    "Publication": 10,
    "Genre": 5,
    "Language": 5,
}

def create_labeled_entry(parent, label, text_var, row, col):
    ttk.Label(parent, text=label, font=("Century Gothic", 8)).grid(row=row, column=col * 2, padx=5, pady=5, sticky="w")
    ttk.Entry(parent, textvariable=text_var, font=("Century Gothic", 10)).grid(row=row, column=col * 2 + 1, padx=5, pady=5, sticky="ew")

def build_form(parent, fields):
    for idx, (label, var) in enumerate(fields):
        create_labeled_entry(parent, label, var, idx // 2, idx % 2)

def open_add_book_popup(app, refresh_callback):
    popup = tk.Toplevel(app)
    popup.title("Add Book")

    vars = {
        label: tk.StringVar()
        for label in ("ISBN", "Title", "Author", "Publication", "Genre", "Language", "Description")
    }

    build_form(popup, list(vars.items()))

    def add():
        data = [v.get().strip() for v in vars.values()]
        if any(not val for val in data):
            messagebox.showerror("Error", "All fields are required.")
            return
        result = add_book_det(*data)
        messagebox.showinfo("Status", result)
        popup.destroy()
        refresh_callback()

    ttk.Button(popup, text="Add Book", command=add).grid(row=4, column=0, columnspan=4, pady=10)

def open_update_book_popup(app, isbn, refresh_callback):
    book_data = get_book_det(str(isbn))[0]
    if isinstance(book_data, str):
        messagebox.showerror("Error", book_data)
        return

    popup = tk.Toplevel(app)
    popup.title("Update Book")

    vars = {
        "Title": tk.StringVar(value=book_data[2]),
        "Description": tk.StringVar(value=book_data[3] or ""),
        "Genre": tk.StringVar(value=book_data[6]),
        "Author": tk.StringVar(value=book_data[4]),
        "Publication": tk.StringVar(value=book_data[5]),
        "Language": tk.StringVar(value=book_data[7]),
    }

    build_form(popup, list(vars.items()))

    def update():
        data = [vars[key].get().strip() for key in vars]
        if any(not val for val in data):
            messagebox.showerror("Error", "All fields are required.")
            return
        result = update_book_det(isbn, *data)
        messagebox.showinfo("Status", result)
        if "success" in result.lower():
            popup.destroy()
            refresh_callback()

    ttk.Button(popup, text="Update Book", command=update).grid(row=4, column=0, columnspan=4, pady=10)

def open_delete_book_popup(app, isbn, refresh_callback):
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete ISBN {isbn}?")
    if confirm:
        result = delete_book_det(isbn)
        messagebox.showinfo("Status", result)
        if "success" in result.lower():
            refresh_callback()

def books_manage(app):
    for widget in app.winfo_children():
        widget.destroy()

    table = ttk.Treeview(
        app,
        columns=("ISBN", "Title", "Description", "Author", "Publication", "Genre", "Language"),
        show="headings",
        bootstyle="secondary"
    )

    for col in table["columns"]:
        table.heading(col, text=col)
        table.column(col, width=column_widths[col], anchor="center")

    table.pack(fill="both", expand=True)

    def refresh_table():
        table.delete(*table.get_children())
        for row in get_book_det():
            table.insert("", "end", values=row[1:])

    def get_selected_isbn():
        selected = table.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a book.")
            return None
        return str(table.item(selected[0])["values"][0])

    button_frame = ttk.Frame(app)
    button_frame.pack(fill="x", pady=10)

    ttk.Button(button_frame, text="Add Book", command=lambda: open_add_book_popup(app, refresh_table)).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Update Book", command=lambda: open_update_book_popup(app, get_selected_isbn(), refresh_table)).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Delete Book", command=lambda: open_delete_book_popup(app, get_selected_isbn(), refresh_table)).pack(side="left", padx=5)

    refresh_table()
