import ttkbootstrap as ttk
from backend.books import get_book_det
from backend.account import get_user
from ui.member.show_details import show_details_page
from ui.common import make_scrollable_frame, make_book_card

def wishlist(app, email, db):
    def show_main_page():
        for widget in app.winfo_children():
            widget.destroy()

        wish = get_user(db=db, email=email, fields=["WishlistedBooks"])
        if wish in ("No records found.", None):
            isbns = []
        else:
            isbns = wish[0].split(",") if wish[0] else []

        main_frame = ttk.Frame(app, padding=30)
        main_frame.pack(fill="both", expand=True)

        panel = ttk.Frame(main_frame, padding=20)
        panel.pack(fill="both", expand=True)

        scrollable = make_scrollable_frame(panel)

        if isbns:
            for i, isbn in enumerate(isbns):
                row, col = divmod(i, 4)
                book_data = get_book_det(isbn=isbn)
                if not book_data:
                    continue
                book = book_data[0]

                card = make_book_card(
                    parent=scrollable,
                    book=book,
                    on_click=lambda isbn=isbn: show_details_page(
                        app, email, show_main_page, isbn,
                        write_reviews=False, wishlist_mode="removed"
                    )
                )
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            for i in range(4):
                scrollable.grid_columnconfigure(i, weight=1)
        else:
            ttk.Label(
                scrollable, text="No books in your wishlist 📭",
                font=("Helvetica", 14, "bold")
            ).pack(anchor="center", pady=30)

    show_main_page()
