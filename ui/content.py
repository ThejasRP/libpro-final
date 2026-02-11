import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.constants import *
from backend.account import get_user
from backend.bookrecord import get_record, overdue_books
from backend.inventory import get_book_inv
from backend.utils import update_time
from ui.common import create_card

column_widths = {
        "SKU": 90,
        "ID": 40,
        "Member": 20,
        "Borrowed On": 20,
        "Return Date": 90,
        "Days Borrowed": 20,
        "Status":10,
        "Returned On":50
    }

def dashboard_content(app, email, db):
    if not app and db not in ["Librarian", "Members"]:
        messagebox.showerror("Error", "Application instance not found / database error.")
        return
    
    userDet = get_user(db, email=email)

    ttk.Label(app, text="Hello, "f'{userDet[2]}.', font=("Helvetica", 20, "bold"), foreground="#6CA6CD").pack(anchor="w", padx=20, pady=(10, 0))
    time_label = ttk.Label(app, font=("Helvetica", 10))
    time_label.pack(anchor="w", padx=20)
    update_time(time_label)

    summary_frame = ttk.Frame(app)
    summary_frame.pack(fill=X, padx=20, pady=20)

    content_frame = ttk.Frame(app)
    content_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

    books_frame = ttk.Labelframe(content_frame, text="Overdue Books", padding=10, width=500)
    books_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
    books_frame.pack_propagate(0)

    if db == "Librarian":
        create_card(summary_frame, "Borrowed Books", f"{get_record(status="Borrowed",count=True)}")
        create_card(summary_frame, "Overdue Books", f"{overdue_books(count=True)}")
        create_card(summary_frame, "Members Count", f"{get_user(db="Members", count=True)}")
        create_card(summary_frame, "Available Books",f"{get_book_inv(count=True)}")
    
        lost_frame = ttk.Labelframe(content_frame, text="Books Details", padding=10, width=500)
        lost_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        lost_frame.pack_propagate(0)

        overdue_tree = ttk.Treeview(
        books_frame,
        columns=("SKU", "Member", "Return Date"),
        show="headings",
        bootstyle="secondary"
        )   
    
        for col in overdue_tree["columns"]:
            overdue_tree.heading(col, text=col)
            overdue_tree.column(col, anchor='center', minwidth=80, width=column_widths[col], stretch=True)

        overdue_tree.pack(fill=BOTH, expand=True)

        overdue_tree.insert("", "end", values=("","","",""))
        if not overdue_books() or overdue_books() == "No overdue records.":
            overdue_tree.insert("", "end", values=("NO","OVERDUE","RECORDS"))
        else:    
            for rec in overdue_books():
                overdue_tree.insert("", "end", values=(rec[0],rec[1],rec[3]))

        books_tree = ttk.Treeview(
        lost_frame,
        columns=("SKU", "Status", "Member", "Returned On"),
        show="headings",
        bootstyle="secondary"
        )   
    
        for col in books_tree["columns"]:
            books_tree.heading(col, text=col)
            books_tree.column(col, anchor='center', minwidth=80, width=column_widths[col], stretch=True)

        books_tree.pack(fill=BOTH, expand=True)

        books_tree.insert("", "end", values=("","","","","",""))
        count = get_record(count=True)
        if count < 25:
            for i in range(0,count): 
                rec = get_record()[i]
                values = (rec[0],rec[1],rec[4],rec[11])
                books_tree.insert("", "end", values=values)
        else:
            for i in range(0,25): 
                books_tree.insert("", "end", values=get_record()[i])

    elif db=="Members":
        create_card(summary_frame, "Overdue Books", f"{overdue_books(email=email,count=True)}")
        create_card(summary_frame, "Borrowed Books", f"{get_record(email=email, status="Borrowed", count=True)}")
        create_card(summary_frame, "ProPoints ", f"{userDet[6]}")
        create_card(summary_frame, "Available Books",f"{get_book_inv(count=True)}")
 
        books_tree = ttk.Treeview(
         books_frame,
         columns=("SKU", "Borrowed On", "Return Date", "Days Borrowed"),
         show="headings",
         bootstyle="secondary"
        )
 
        for col in books_tree["columns"]:
            books_tree.heading(col, text=col)
            books_tree.column(col, anchor='center', minwidth=80, width=column_widths[col], stretch=True)
     
        books_tree.pack(fill=BOTH, expand=True)

        books_tree.insert("", "end", values=(
            "",     
            "",     
            "",     
            ""
        ))
        
        if not overdue_books(email=email) or overdue_books(email=email) == "No overdue records.":
            books_tree.insert("", "end", values=("NO","OVERDUE","RECORDS"))
        else:    
            for rec in overdue_books(email=email):
                books_tree.insert("", "end", values=(rec[0],rec[6],rec[3],rec[5]))
