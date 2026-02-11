from tkinter import messagebox
import ttkbootstrap as ttk 

from ui.login import login_screen

def on_close():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        app.destroy()

app = ttk.Window(themename="darkly")
app.geometry("1200x800") 
app.state('zoomed')
app.title("LibPro | Library Management App")

app.protocol("WM_DELETE_WINDOW", on_close)

style = ttk.Style()
style.configure("crimson.TButton",
                background="#4682B4", 
                foreground="white",  
                borderwidth=0,
                focusthickness=0)
            
style.configure("inactive.TButton",
                background="#171717", 
                foreground="white",  
                borderwidth=0,
                focusthickness=0,
                padding=20)

style.configure("active.TButton",
                background="#4682B4",
                foreground="white",
                relief="flat",
                borderwidth=0,
                padding=20,
                padx=(5,0)) 

style.configure("My.TFrame", background="#171717")

style.configure("secondary.TFrame", background="#4682B4")

login_screen(app)
app.mainloop()