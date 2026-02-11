from ttkbootstrap.widgets import Frame, Label, Treeview, Scrollbar
from backend.account import get_user

redemption_items = [
    {"name": "Library Tote Bag", "cost": 100},
    {"name": "Notebook", "cost": 80},
    {"name": "Pen Set", "cost": 50},
    {"name": "Free Book", "cost": 200}
]

def points_dashboard(app, email):
    for widget in app.winfo_children():
        widget.destroy()

    userData = get_user("Members", email=email)

    container = Frame(app, padding=20)
    container.pack(fill="both", expand=True)

    if userData != "No records found.":
        points = userData[6]

        title = Label(container, text="🎁 Redeem Your Points", font=("Segoe UI", 16, "bold"))
        title.pack(anchor="center", pady=(0, 10))

        points_display = Label(
            container,
            text=f"Available Points",
            font=("Segoe UI", 14),
            bootstyle="success"
        )
        points_display.pack(anchor="center", pady=(0, 15))
        points_display = Label(
            container,
            text=f"{points}",
            font=("Segoe UI", 20, "bold"),
            bootstyle="success"
        )
        points_display.pack(anchor="center", pady=(0, 15))

        table_frame = Frame(container)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("Item", "Points Required")
        tree = Treeview(table_frame, columns=columns, show="headings", bootstyle="info")
        tree.heading("Item", text="Item")
        tree.heading("Points Required", text="Points Required")
        tree.column("Item", anchor="center", width=250)
        tree.column("Points Required", anchor="center", width=150)
        tree.pack(side="left", fill="both", expand=True)

        for item in redemption_items:
            tree.insert("", "end", values=(item["name"], item["cost"]))

        scrollbar = Scrollbar(table_frame, orient="vertical", command=tree.yview, bootstyle="round")
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
    else:
        Label(container, text="⚠️ Unable to fetch your points.", font=("Segoe UI", 14, "bold"), bootstyle="danger").pack(anchor="center", pady=20)
