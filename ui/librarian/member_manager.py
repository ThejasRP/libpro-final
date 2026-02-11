import tkinter as tk
import ttkbootstrap as ttk
from tkinter import StringVar, messagebox
from backend.account import delete_user, get_user, redeem_points_mem, signup_user, update_user

def create_labeled_entry(parent, label, var, show=None):
    ttk.Label(parent, text=label, font=("Century Gothic", 8)).pack(pady=5)
    ttk.Entry(parent, textvariable=var, font=("Century Gothic", 10), show=show).pack(pady=5)

def create_popup(title, size="600x400"):
    popup = ttk.Toplevel()
    popup.title(title)
    popup.geometry(size)
    form = ttk.Frame(popup)
    form.pack(fill="both", expand=True)
    return popup, form

def open_add_member_popup(app, refresh):
    popup, form = create_popup("Add Member")
    ttk.Label(form, text="Add New Member", font=("Cambria", 18, "bold")).pack(pady=20)

    fields = {label: StringVar() for label in ["Full Name", "Email Address", "Mobile Number", "Password"]}
    for label in fields:
        create_labeled_entry(form, label, fields[label], show="*" if label == "Password" else None)

    def submit():
        res = signup_user("Members", fields["Email Address"].get(), fields["Full Name"].get(),
                          fields["Password"].get(), fields["Mobile Number"].get())
        messagebox.showinfo("Success" if "Error:" not in res else "Error", res)
        if "Error:" not in res:
            popup.destroy()
            refresh()

    ttk.Button(form, text="Add Member", command=submit, style="crimson.TButton").pack(pady=10)
    ttk.Label(form, text="Fill the details and click 'Add Member' to create new membership.", font=("Calibri", 10, "italic")).pack(pady=10)

def update_member_popup(app, data, refresh):
    popup, form = create_popup("Update Member Details")
    ttk.Label(form, text="Update Member Details", font=("Cambria", 18, "bold")).pack(pady=20)

    fields = {
        "Full Name": StringVar(value=data[2]),
        "Mobile Number": StringVar(value=data[4]),
        "Old Password": StringVar(),
        "New Password": StringVar()
    }
    for label in fields:
        create_labeled_entry(form, label, fields[label], show="*" if "Password" in label else None)

    def save():
        res = update_user("Members", data[1], fields["Old Password"].get(), fields["Full Name"].get(),
                          fields["Mobile Number"].get(), fields["New Password"].get())
        messagebox.showinfo("Success" if res == "Update successful." else "Error", res)
        if res == "Update successful.":
            popup.destroy()
        refresh()

    ttk.Button(form, text="Save Changes", command=save, style="crimson.TButton").pack(pady=10)
    ttk.Label(form, text="Enter old password again if you don't want to change it.", font=("Calibri", 10, "italic")).pack(pady=10)

def remove_points_popup(app, refresh):
    selected = table.selection()
    if not selected:
        return messagebox.showerror("Error", "No member selected!")

    email = table.item(selected)["values"][1]
    popup, form = create_popup("Update Pro Points")
    ttk.Label(form, text="Update Pro Points", font=("Cambria", 18, "bold")).pack(pady=20)

    points = StringVar()
    create_labeled_entry(form, "Enter no. of points redeemed: ", points)

    def save():
        res = redeem_points_mem(email, points.get())
        messagebox.showinfo("Success" if "points redeemed" in res else "Error", res)
        if "points redeemed" in res:
            popup.destroy()
        refresh()

    ttk.Button(form, text="Save Changes", command=save, style="crimson.TButton").pack(pady=10)

def open_delete_member_popup(app, table, refresh, admin_email):
    selected = table.selection()
    if not selected:
        return messagebox.showerror("Error", "No member selected!")

    email = table.item(selected)["values"][1]
    popup = tk.Toplevel(app)
    popup.geometry("300x150")
    popup.title("Confirm Membership Cancellation")
    popup.grab_set()

    ttk.Label(popup, text=f"Cancel membership for:\n{email}").pack(pady=10)
    ttk.Label(popup, text="Enter Admin Password:").pack()

    password = ttk.Entry(popup, show="*")
    password.pack(pady=5)

    def confirm():
        if not password.get():
            return messagebox.showerror("Error", "Password is required.")

        res = delete_user("Members", email, password.get(), admin_email)
        messagebox.showinfo("Success" if res == "Account deleted successfully." else "Error", res)
        if res == "Account deleted successfully.":
            popup.destroy()
            refresh()

    ttk.Button(popup, text="Confirm", command=confirm).pack(pady=10)

def open_update_member_popup(app, refresh):
    selected = table.selection()
    if not selected:
        return messagebox.showerror("Error", "No member selected!")

    email = table.item(selected)["values"][1]
    member = get_user("Members", email=email)
    if member:
        update_member_popup(app, member, refresh)

def populate_table():
    table.delete(*table.get_children())
    for member in get_user("Members"):
        table.insert("", "end", values=(member[0], member[1], member[2], member[4], member[6], member[7]))

def member_manager(app, admin_email):
    global table
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    frame = ttk.Frame(app)
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    columns = ("Member No.", "Email", "Full Name", "Mobile Number", "Points", "Date of Joining")
    table = ttk.Treeview(frame, columns=columns, show="headings", height=40, bootstyle="secondary")

    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor="center", stretch=True)

    table.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

    scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=table.xview)
    table.configure(xscrollcommand=scrollbar.set)
    scrollbar.grid(row=1, column=0, sticky="ew")

    btn_frame = ttk.Frame(app)
    btn_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    buttons = [
        ("Add New Member", lambda: open_add_member_popup(app, populate_table)),
        ("Update Member Details", lambda: open_update_member_popup(app, populate_table)),
        ("Update ProPoints", lambda: remove_points_popup(app, populate_table)),
        ("Delete Member", lambda: open_delete_member_popup(app, table, populate_table, admin_email)),
    ]

    for text, cmd in buttons:
        ttk.Button(btn_frame, text=text, command=cmd, style="crimson.TButton").pack(fill="x", pady=5)

    populate_table()
