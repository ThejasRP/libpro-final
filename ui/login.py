import ttkbootstrap as ttk
from tkinter import messagebox
import tkinter as tk
from backend.account import get_user, signin_user
from ui.dashboard import dashboard
from PIL import Image, ImageTk

def login_screen(app):
    global login_frame, email_var, password_var

    def add_entry(frame, label, var, is_password=False):
        ttk.Label(frame, text=label, font=("Century Gothic", 14)).pack(anchor="w", pady=5)
        ttk.Entry(frame, textvariable=var, font=("Century Gothic", 12), show="*" if is_password else "").pack(fill="x", pady=5)

    login_frame = ttk.Frame(app, padding=30)
    login_frame.pack(expand=True, fill="both")

    branding = ttk.Frame(login_frame, padding=20)
    branding.pack(side="left", expand=True, fill="both", padx=20, pady=20)

    img = Image.open("./ui/images/banner.png").resize((450, 450))
    photo = ImageTk.PhotoImage(img)
    tk.Label(branding, image=photo, bg="#1e1e1e").pack(expand=True, pady=40)
    Img1 = tk.Label(branding, image=photo, bg="#1e1e1e")
    Img1.image = photo  
    Img1.place(relx=0.5, rely=0.5, anchor="center")

    login_section = ttk.Frame(login_frame, padding=20)
    login_section.pack(side="right", expand=True, fill="both", padx=10, pady=20)

    canvas = tk.Canvas(login_section, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    w, h, r = 500, 500, 20
    ovals = [(0, 0, r*2, r*2), (w - r*2, 0, w, r*2), (0, h - r*2, r*2, h), (w - r*2, h - r*2, w, h)]
    for x1, y1, x2, y2 in ovals:
        canvas.create_oval(x1, y1, x2, y2, outline="#ffffff")
    canvas.create_rectangle(r, 0, w - r, h, outline="#ffffff")
    canvas.create_rectangle(0, r, w, h - r, outline="#ffffff")

    form = ttk.Frame(canvas)
    canvas.create_window(w // 2, h // 2, window=form, anchor="center")

    ttk.Label(form, text="Login", font=("Gotham Bold", 40, "bold")).pack(pady=20)

    email_var = ttk.StringVar()
    password_var = ttk.StringVar()
    add_entry(form, "Email ID:", email_var)
    add_entry(form, "Password:", password_var, is_password=True)

    ttk.Button(form, text="Login", command=lambda: validate_login(app), style="crimson.TButton").pack(pady=20, fill="x")
    ttk.Label(form, text="Welcome to the modern library experience.", font=("Calibri", 10, "italic")).pack(pady=10)

def validate_login(app):
    email, password = email_var.get().strip(), password_var.get().strip()
    if not email or not password:
        return messagebox.showerror("Error", "Email and password cannot be empty.")

    try:
        for role in ("Librarian", "Members"):
            if role == "Librarian" and not get_user(role, email=email, bool=True):
                continue
            result = signin_user(role, email, password)
            if result == "Login successful.":
                messagebox.showinfo("Success", f"{role} login successful!")
                login_frame.pack_forget()
                return dashboard(app, email, role)
            elif role == "Members":
                return messagebox.showerror("Error", result)
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")
