import tkinter as tk
from tkinter import StringVar, ttk, messagebox
from backend.inventory import add_book_inv, get_book_inv, update_book_inv


def show_category(category):
    if category not in ["Unshelved", "Lost", "Missing", "Damaged", "Borrowed"]:
        messagebox.showerror("Error", "Invalid category chosen.")
        return

    books = get_book_inv(status=category)
    if isinstance(books, str):
        messagebox.showerror("Error", books)
        return

    if not books:
        messagebox.showinfo(f"{category} Books", "No books were found.")
        return

    books_list = "\n".join([book[0] for book in books])
    messagebox.showinfo(f"{category} Books", f"{category} Books:\n\n{books_list}")


def build_popup_fields(popup, fields):
    entries = {}
    for i, (label_text, var_type) in enumerate(fields):
        tk.Label(popup, text=label_text).grid(row=i, column=0, padx=10, pady=5)
        var = StringVar() if var_type == "str" else None
        entry = tk.Entry(popup, textvariable=var) if var else tk.Entry(popup)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label_text.lower()] = entry
    return entries


def open_shelve_popup(app, update_view):
    def shelve_book():
        try:
            sku = entries["sku"].get()
            isbn = entries["isbn"].get()
            bay = int(entries["bay number"].get())
            shelf = int(entries["shelf number"].get())
            row = int(entries["row number"].get())
            col = int(entries["column number"].get())

            if not sku:
                raise ValueError("SKU cannot be empty.")

            res = add_book_inv(sku, isbn, "Shelved", bay, shelf, row, col)
            messagebox.showinfo("Success", res)
            update_view()
            popup.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    popup = tk.Toplevel(app)
    popup.title("Shelve Book")

    fields = [
        ("SKU", "str"), ("ISBN", "str"), ("Bay Number", "int"),
        ("Shelf Number", "int"), ("Row Number", "int"), ("Column Number", "int")
    ]
    entries = build_popup_fields(popup, fields)

    ttk.Button(popup, text="Submit", command=shelve_book, style="crimson.TButton")\
        .grid(row=len(fields), column=0, columnspan=2, pady=20)


def open_update_popup(app, update_view):
    def update_book():
        try:
            sku = entries["sku"].get()
            status = entries["status"].get()
            bay = int(entries["bay number"].get())
            shelf = int(entries["shelf number"].get())
            row = int(entries["row number"].get())
            col = int(entries["column number"].get())

            if not sku:
                raise ValueError("SKU cannot be empty.")

            res = update_book_inv(sku, status, bay, shelf, row, col)
            messagebox.showinfo("Success", res)
            update_view()
            popup.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    popup = tk.Toplevel(app)
    popup.title("Update Book Info")

    fields = [
        ("SKU", "str"), ("Status", "str"), ("Bay Number", "int"),
        ("Shelf Number", "int"), ("Row Number", "int"), ("Column Number", "int")
    ]
    entries = build_popup_fields(popup, fields)

    ttk.Button(popup, text="Submit", command=update_book, style="crimson.TButton")\
        .grid(row=len(fields), column=0, columnspan=2, pady=20)


def bay_manager(app):
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    paned = ttk.PanedWindow(app, orient="horizontal")
    paned.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    outer_canvas = tk.Canvas(paned, bg="#1e1e1e", highlightthickness=0)
    paned.add(outer_canvas, weight=4)

    outer_scroll = ttk.Scrollbar(app, orient=tk.HORIZONTAL, command=outer_canvas.xview, bootstyle="dark")
    outer_canvas.configure(xscrollcommand=outer_scroll.set)
    outer_scroll.grid(row=1, column=0, sticky="ew")

    outer_frame = tk.Frame(outer_canvas, bg="#1e1e1e")
    outer_id = outer_canvas.create_window((0, 0), window=outer_frame, anchor="nw")

    outer_canvas.bind("<Configure>", lambda e: outer_canvas.itemconfig(outer_id, height=e.height))

    right = ttk.Frame(paned, width=200)
    paned.add(right, weight=1)

    button_data = [
        ("Add New Book to Inventory", lambda: open_shelve_popup(app, update_shelf_view)),
        ("Re-add Book / Update Book Position", lambda: open_update_popup(app, update_shelf_view)),
        ("View Deshelved Books", lambda: show_category("Unshelved")),
        ("View Missing Books", lambda: show_category("Missing")),
        ("View Lost Books", lambda: show_category("Lost")),
        ("View Damaged Books", lambda: show_category("Damaged")),
    ]
    for i, (text, cmd) in enumerate(button_data):
        ttk.Button(right, text=text, command=cmd, style="crimson.TButton").grid(row=i, column=0, pady=10)

    def update_shelf_view():
        for widget in outer_frame.winfo_children():
            widget.destroy()

        books = get_book_inv()
        bay_map = {}
        for book in books:
            bay, shelf, row, col = book[3:7]
            if 0 in (bay, shelf, row, col): continue
            bay_map.setdefault(bay, []).append(book)

        for bay_no, bay_books in sorted(bay_map.items()):
            bay_wrap = tk.Frame(outer_frame, bg="#1e1e1e")
            bay_wrap.pack(side=tk.LEFT, padx=30, fill=tk.Y)

            bay_canvas = tk.Canvas(bay_wrap, width=280, height=500, bg="#1e1e1e", highlightthickness=0)
            bay_canvas.pack(side=tk.LEFT, fill=tk.Y)

            bay_scroll = ttk.Scrollbar(bay_wrap, orient=tk.VERTICAL, command=bay_canvas.yview, bootstyle="dark")
            bay_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            bay_canvas.configure(yscrollcommand=bay_scroll.set)

            bay_frame = tk.Frame(bay_canvas, bg="white", width=280)
            bay_canvas.create_window((0, 0), window=bay_frame, anchor="nw")

            tk.Label(bay_frame, text=f"Bay {bay_no}", font=("Arial", 12, "bold"), bg="white").pack(pady=5)

            shelf_map = {}
            for book in bay_books:
                shelf_map.setdefault(book[4], []).append(book)

            for shelf_no in sorted(shelf_map):
                shelf_books = shelf_map[shelf_no]
                shelf_box = tk.Frame(bay_frame, bg="#e0e0e0", height=220, bd=1, relief="solid", highlightthickness=1)
                shelf_box.pack(fill=tk.X, pady=10)

                tk.Label(shelf_box, text=f"Shelf {shelf_no}", font=("Arial", 9, "bold"), bg="#e0e0e0", anchor="w")\
                    .pack(fill=tk.X)

                shelf_canvas = tk.Canvas(shelf_box, width=240, height=180, bg="#e0e0e0", highlightthickness=0)
                shelf_canvas.pack(side=tk.LEFT, fill=tk.X, expand=True)

                for book in shelf_books:
                    row, col = book[5], book[6]
                    x0, y0 = col * 60 + 10, row * 30 + 10
                    x1, y1 = x0 + 60, y0 + 30
                    shelf_canvas.create_rectangle(x0, y0, x1, y1, fill="lightgreen", outline="black")
                    shelf_canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=book[0], font=("Arial", 8), width=56)

                shelf_canvas.config(scrollregion=shelf_canvas.bbox("all"))

            bay_frame.update_idletasks()
            bay_canvas.config(scrollregion=bay_canvas.bbox("all"))

            bay_canvas.bind("<Enter>", lambda e, c=bay_canvas: c.bind_all("<MouseWheel>", lambda e: c.yview_scroll(int(-e.delta / 120), "units")))
            bay_canvas.bind("<Leave>", lambda e, c=bay_canvas: c.unbind_all("<MouseWheel>"))

        outer_frame.update_idletasks()
        outer_canvas.config(scrollregion=outer_canvas.bbox("all"))

    update_shelf_view()
