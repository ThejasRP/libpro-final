import ttkbootstrap as ttk
from tkinter import messagebox
from backend.bookrecord import get_record
from backend.books import get_book_det
from backend.reviews import add_review
from ui.common import make_scrollable_frame, make_book_card

def view_borrowed_books(app, email):
    def show_main_page():
        for w in app.winfo_children(): w.destroy()

        records = get_record(email=email)
        if not records or records == "No records found." or records[0] == "":
            records = []

        main = ttk.Frame(app, padding=30)
        main.pack(fill="both", expand=True)

        panel = ttk.Frame(main, padding=20)
        panel.pack(fill="both", expand=True)

        scrollable = make_scrollable_frame(panel)

        for idx, rec in enumerate(records):
            book_data = get_book_det(isbn=rec[3])
            if not book_data: continue
            book = book_data[0]
            sku = rec[1]
            book = get_book_det(isbn=rec[3])[0]
            card = make_book_card(
                parent=scrollable,
                book=book,
                on_click=lambda s=sku: show_details_page(sku),
                status=rec[2]
            )
            row, col = divmod(idx, 4)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        if not records:
            ttk.Label(scrollable, text="No books found 📭", font=("Helvetica", 14, "bold")) \
               .pack(pady=30)

        for i in range(4):
            scrollable.grid_columnconfigure(i, weight=1)

    def show_details_page(sku):
        for w in app.winfo_children(): w.destroy()
        rec = next((r for r in get_record(email=email) if r[1] == sku), None)
        if not rec:
            messagebox.showerror("Error", "Book record not found.")
            show_main_page()
            return

        book_data = get_book_det(isbn=rec[3])[0]

        container = ttk.Frame(app, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="📖 Borrowed Book Details", font=("Century Gothic", 18, "bold")) \
           .pack(pady=(0, 15))

        info = ttk.Frame(container, padding=10)
        info.pack(side="left", fill="both", expand=True)

        fields = [
            ("SKU", rec[1]), ("Status", rec[2]), ("ISBN", rec[3]), ("Title", book_data[2]),
            ("Author", book_data[4]), ("Genre", book_data[6]), ("Language", book_data[7]),
            ("Borrower", f"{rec[5]} ({rec[4]})"), ("Borrowed On", rec[13]),
            ("Days Borrowed", rec[7]), ("Due On", rec[10]),
            ("Returned On", rec[11] or "Not returned yet"), ("Days Late", rec[8]),
            ("Fine (Rs.)", rec[9]), ("Points Awarded", rec[6]),
            ("Updated On", rec[12])
        ]
        for label, value in fields:
            row = ttk.Frame(info, padding=5)
            row.pack(fill="x")
            ttk.Label(row, text=f"{label}:", font=("Helvetica", 13, "bold"), width=16) \
               .pack(side="left")
            ttk.Label(row, text=value, font=("Helvetica", 13), wraplength=300) \
               .pack(side="left", fill="x", expand=True)

        right = ttk.Frame(container, padding=10)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(right, text="✍️ Write a Review", font=("Helvetica", 16, "bold")) \
           .pack(anchor="w", pady=(0, 10))
        review_box = ttk.Text(right, height=6, wrap="word")
        review_box.pack(fill="x", pady=(0, 10))
        ttk.Label(right, text="⭐ Rating (1 to 5):", font=("Helvetica", 11)) \
           .pack(anchor="w", pady=(5, 2))
        rating_var = ttk.StringVar(value="5")
        ttk.Combobox(right, textvariable=rating_var, values=["1","2","3","4","5"], 
                     width=5, state="readonly").pack(anchor="w", pady=(0,10))

        def submit_review():
            review = review_box.get("1.0", "end").strip()
            rating = rating_var.get()
            res = add_review(isbn=rec[3], fullname=rec[5], email=email,
                             review=review, rating=rating)
            if "successfully" in res:
                messagebox.showinfo("✅ Success", res)
                review_box.delete("1.0", "end"); rating_var.set("5")
            else:
                messagebox.showerror("❌ Error", res)

        ttk.Button(right, text="✅ Submit Review", command=submit_review, style="crimson.TButton") \
           .pack(pady=10)
        ttk.Button(info, text="⬅ Back", command=show_main_page, style="crimson.TButton") \
           .pack(pady=20, anchor="w")

    show_main_page()
