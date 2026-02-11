import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.constants import *
from backend.inventory import get_book_inv
from backend.reviews import get_reviews, add_review
from backend.books import get_book_det
from backend.account import get_user, wishlist_mem

Books = get_book_det()

def add_to_wishlist(email, isbn):
    res = wishlist_mem(email, isbn, "added")
    (messagebox.showinfo if "Error:" not in res else messagebox.showerror)("Wishlist", res)

def remove_from_wishlist(app, email, isbn, revert):
    res = wishlist_mem(email, isbn, "removed")
    if "Error:" in res:
        messagebox.showerror("Wishlist", res)
    else:
        messagebox.showinfo("Wishlist", res)
        for widget in app.winfo_children():
            widget.destroy()
        revert()

def show_details_page(app, email, revert, isbn, write_reviews, wishlist_mode):
    if wishlist_mode not in ("added", "removed"):
        return

    for widget in app.winfo_children():
        widget.destroy()

    frame = ttk.Frame(app, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="📘 Book Details", font=("Century Gothic", 20, "bold")).pack()
    ttk.Label(frame, text="Detailed Information about the selected book.", font=("Arial", 12, "italic")).pack()

    book = next((b for b in Books if b[1] == isbn), None)
    if not book:
        messagebox.showerror("Error", "Book not found.")
        return revert()

    content = ttk.Frame(frame)
    content.pack(fill="both", expand=True)

    left = ttk.Frame(content, padding=10)
    left.pack(side="left", fill="both", expand=True)

    canvas = ttk.Canvas(left, highlightthickness=0)
    scroll_y = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
    scrollable = ttk.Frame(canvas)

    canvas.create_window((0, 0), window=scrollable, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)
    scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    fields = [
        ("ISBN", book[1]), ("Title", book[2]), ("Description", book[3]),
        ("Author", book[4]), ("Publication", book[5]), ("Genre", book[6]),
        ("Language", book[7]), ("Added On", book[8]), ("Updated On", book[9])
    ]
    for key, val in fields:
        f = ttk.Frame(scrollable, padding=5)
        f.pack(fill="x", anchor="w")
        ttk.Label(f, text=f"{key}:", font=("Helvetica", 13, "bold")).pack(anchor="w")
        ttk.Label(f, text=val, font=("Helvetica", 13), wraplength=350).pack(anchor="w")

    qty = get_book_inv(isbn=isbn, count=True)
    ttk.Label(scrollable, text=f"Quantity: {qty or 'All copies borrowed.'}", font=("Helvetica", 13, "bold")).pack(anchor="w", pady=10)

    right = ttk.Frame(content, padding=20)
    right.pack(side="right", fill="both", expand=True)

    if write_reviews:
        ttk.Label(right, text="✍️ Write a Review", font=("Helvetica", 16, "bold")).pack(anchor="w", pady=(0, 10))
        review_box = ttk.Text(right, height=5, wrap="word")
        review_box.pack(fill="x", pady=(0, 10))

        ttk.Label(right, text="Rating (1-5):", font=("Helvetica", 11)).pack(anchor="w")
        rating_var = ttk.StringVar(value="5")
        ttk.Combobox(right, textvariable=rating_var, values=["1", "2", "3", "4", "5"], width=5, state="readonly").pack(anchor="w", pady=(0, 10))

        def submit_review():
            review = review_box.get("1.0", "end").strip()
            rating = rating_var.get()
            fullname = get_user("Members", email=email, fields=["FullName"])[0]
            res = add_review(book[1], fullname, email, review, rating)
            (messagebox.showinfo if "successfully" in res else messagebox.showerror)("Review", res)
            if "successfully" in res:
                show_details_page(app, email, revert, isbn, write_reviews, wishlist_mode)

        ttk.Button(right, text="Submit", command=submit_review, style="success.TButton").pack(anchor="center", pady=5)

    ttk.Label(right, text="🗨️ All Reviews", font=("Helvetica", 14, "bold")).pack(anchor="w", pady=(20, 5))

    r_canvas = ttk.Canvas(right, highlightthickness=0)
    r_scroll = ttk.Scrollbar(right, orient="vertical", command=r_canvas.yview)
    r_inner = ttk.Frame(r_canvas)
    r_canvas.create_window((0, 0), window=r_inner, anchor="nw")
    r_canvas.configure(yscrollcommand=r_scroll.set)
    r_inner.bind("<Configure>", lambda e: r_canvas.configure(scrollregion=r_canvas.bbox("all")))

    r_canvas.pack(side="left", fill="both", expand=True)
    r_scroll.pack(side="right", fill="y")

    reviews = get_reviews(isbn)
    if isinstance(reviews, str):
        ttk.Label(r_inner, text="No reviews yet!", font=("Helvetica", 11)).pack(anchor="w", padx=5)
    else:
        for r in reviews:
            ttk.Label(r_inner, text=f"👤 {r[2]}", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(5, 0), padx=5)
            ttk.Label(r_inner, text=f"⭐ Rating: {r[4]}/5", font=("Helvetica", 10)).pack(anchor="w", padx=5)
            ttk.Label(r_inner, text=r[5], font=("Helvetica", 10), wraplength=350).pack(anchor="w", padx=5)
            ttk.Label(r_inner, text="─" * 40).pack(pady=5)

    if wishlist_mode == "added":
        ttk.Button(left, text="➕ Add to Wishlist", command=lambda: add_to_wishlist(email, isbn), style="primary.TButton").pack(side="bottom", padx=5)
    elif wishlist_mode == "removed":
        ttk.Button(left, text="❌ Remove from Wishlist", command=lambda: remove_from_wishlist(app, email, isbn, revert), style="primary.TButton").pack(side="bottom", padx=5)

    ttk.Button(left, text="⬅ Back", command=revert, style="secondary.TButton").pack(side="bottom", padx=5, pady=10)
