import ttkbootstrap as ttk
from backend.books import get_book_det
from ui.member.show_details import show_details_page
from ui.common import make_scrollable_frame, make_book_card

Books = get_book_det()

def view_books(app, email):
    def show_main_page():
        for w in app.winfo_children(): w.destroy()

        main = ttk.Frame(app, padding=30)
        main.pack(fill="both", expand=True)

        panel = ttk.Frame(main, padding=20)
        panel.pack(fill="both", expand=True)

        scrollable = make_scrollable_frame(panel)

        if Books:
            for idx, book in enumerate(Books):
                row, col = divmod(idx, 4)
                card = make_book_card(
                    parent=scrollable,
                    book=book,
                    on_click=lambda e, isbn=book[1]: show_details_page(
                        app, email, show_main_page, isbn, write_reviews=True, wishlist_mode="added"
                    )
                )
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            for i in range(4):
                scrollable.grid_columnconfigure(i, weight=1)
        else:
            ttk.Label(
                scrollable, text="No books found.",
                font=("Helvetica", 14, "bold")
            ).pack(anchor="center", pady=30)

    show_main_page()
