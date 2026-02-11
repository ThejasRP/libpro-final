import ttkbootstrap as ttk
from tkinter import StringVar, messagebox
from backend.account import get_user
from backend.bookrecord import borrow_book, get_record, return_book
from backend.inventory import get_book_inv

def create_labeled_entry(parent, label, var, show=None):
    ttk.Label(parent, text=label, font=("Century Gothic", 8)).pack(pady=5)
    ttk.Entry(parent, textvariable=var, font=("Century Gothic", 10), show=show).pack(pady=5)

def open_borrow_book(app, refresh):
    popup = ttk.Toplevel(app)
    popup.geometry("600x400")
    popup.title("Add Borrowing Record")

    form = ttk.Frame(popup)
    form.pack(fill="both", expand=True)

    ttk.Label(form, text="Add Borrowing Record", font=("Cambria", 18, "bold")).pack(pady=20)

    email, sku, days = StringVar(), StringVar(), StringVar()
    for label, var in [("Email Address", email), ("SKU Number", sku), ("Number of Days Borrowed", days)]:
        create_labeled_entry(form, label, var)
    
    def submit():
        userDet = get_user("Members", email=email.get())
        bookDet = (get_book_inv(sku=sku.get()))[0]

        if not userDet or bookDet=="N":
            messagebox.showerror("Error", "Invalid user or book details.")
            popup.destroy()
            refresh()
            return
        
        res = borrow_book(email.get(), sku.get(), userDet[2], bookDet[1], days.get())
        if "Book borrowed successfully." not in res:
            messagebox.showerror("Error", res)
        else:
            messagebox.showinfo("Success", "Book Record added successfully!")
            popup.destroy()
            refresh()

    ttk.Button(form, text="Add Record", command=submit, style="crimson.TButton").pack(pady=10)
    ttk.Label(form, text="Fill the details and click 'Add Record' to create new record.", font=("Calibri", 10, "italic")).pack(pady=10)

def open_return_book(app, refresh):
    popup = ttk.Toplevel(app)
    popup.geometry("400x200")
    popup.title("Return Book")

    form = ttk.Frame(popup)
    form.pack(fill="both", expand=True)

    ttk.Label(form, text="Return Book", font=("Cambria", 18, "bold")).pack(pady=20)

    sku = StringVar()
    create_labeled_entry(form, "SKU Number", sku)

    def submit():
        if not sku.get():
            messagebox.showerror("Error", "SKU is required.")
            return
        
        res = return_book(sku.get())
        if "Book returned successfully." not in res:
            messagebox.showerror("Error", res)
        else:
            messagebox.showinfo("Success", res)
            popup.destroy()
            refresh()

    ttk.Button(form, text="Return Book", command=submit, style="crimson.TButton").pack(pady=10)
    ttk.Label(form, text="Enter the SKU of the book to return and click 'Return Book'.", font=("Calibri", 10, "italic")).pack(pady=10)
    
def populate_table():
    table.delete(*table.get_children())
    rec = get_record()
    if rec!="No records found.":
        for record in get_record():
            table.insert("", "end", values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[10], record[11], record[12]))
    else:
        table.insert("", "end", values=("No records found",) * 9)

def books_record(app, admin_email):
    global table

    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    frame = ttk.Frame(app)
    frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    columns = ("Record No.", "SKU", "Status", "ISBN", "Email", "Full Name", "Points", "Days Borrowed", "Due On", "Returned On", "UpdatedOn")
    table = ttk.Treeview(frame, columns=columns, show="headings", height=40, bootstyle="secondary")

    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor="center", width=120, stretch=False)

    table.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=table.xview)
    table.configure(xscrollcommand=scrollbar.set)
    scrollbar.grid(row=1, column=0, sticky="ew")

    btn_frame = ttk.Frame(app)
    btn_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    ttk.Button(btn_frame, text="Borrow Book", command=lambda: open_borrow_book(app, populate_table), style="crimson.TButton").pack(fill="x", pady=5)
    ttk.Button(btn_frame, text="Return Book", command=lambda: open_return_book(app, populate_table), style="crimson.TButton").pack(fill="x", pady=5)

    populate_table()
