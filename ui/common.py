import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def create_card(parent, title, value):
    frame = ttk.Frame(parent, padding=15, style="secondary.TFrame")
    frame.pack(side=LEFT, expand=True, fill=BOTH, padx=10)
    ttk.Label(frame, text=value, font=("Helvetica", 18, "bold"),background="#4682B4").pack()
    ttk.Label(frame, text=title, font=("Helvetica", 10),background="#4682B4").pack()

import ttkbootstrap as ttk

ACCENT_COLOR = "#6CA6CD"

def make_scrollable_frame(parent):
    canvas = ttk.Canvas(parent, highlightthickness=0)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable = ttk.Frame(canvas)

    scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return scrollable

def make_book_card(parent, book, on_click, status=None):
    style = ttk.Style()
    style.configure("hover.TFrame", background="#f0f0f0", borderwidth=0)

    card = ttk.Frame(parent, width=100, height=160, borderwidth=3, bootstyle="dark")
    card.grid_propagate(False)

    def on_hover(e): card.configure(style="hover.TFrame")
    def on_leave(e): card.configure(bootstyle="dark")

    card.bind("<Enter>", on_hover)
    card.bind("<Leave>", on_leave)

    title = ttk.Label(
        card,
        text=f"{book[2]}\t\t\t\t\t", 
        font=("Helvetica", 14, "bold"),
        style="crimson.TButton", 
        wraplength=172,
        anchor="center"
    )
    title.pack(padx=5, expand=True, fill="both", anchor="center", side="top")
    title.bind("<Button-1>", lambda e: on_click(book[1]))

    desc = ttk.Label(
        card,
        text=f"Description: {book[3]}",
        font=("Helvetica", 10),
        wraplength=200,
        justify="left"
    )
    desc.pack(padx=5, expand=True, fill="both")
    desc.bind("<Button-1>", lambda e: on_click(book[1]))

    author = ttk.Label(
        card,
        text=f"Author: {book[4]}",
        font=("Helvetica", 10)
    )
    author.pack(padx=5, expand=True, fill="both")
    author.bind("<Button-1>", lambda e: on_click(book[1]))

    if status:
        status_label = ttk.Label(
            card,
            text=f"Status: {status}",
            font=("Helvetica", 10)
        )
        status_label.pack(padx=5, expand=True, fill="both")
        status_label.bind("<Button-1>", lambda e: on_click(book[1]))

    card.bind("<Button-1>", lambda e: on_click(book[1]))

    return card