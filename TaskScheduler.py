import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
import threading
from plyer import notification
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Global flag for user permission
notifications_enabled = False

# Notify the user at the specified time
def notify(task, deadline):
    while True:
        now = datetime.now()
        deadline_time = datetime.strptime(deadline, '%Y-%m-%d %H:%M')

        if now >= deadline_time:
            if notifications_enabled:
                notification.notify(
                    title='🕒 Task Reminder',
                    message=f"⏰ Reminder for: {task}",
                    timeout=10,
                    app_name="Creative Task Manager"
                )
            break
        time.sleep(30)

# Add the task to the list and set notification
def add_task():
    task = task_entry.get()
    deadline = deadline_entry.get()
    if task and deadline:
        try:
            deadline_time = datetime.strptime(deadline, '%Y-%m-%d %H:%M')
            if deadline_time <= datetime.now():
                messagebox.showwarning("Time Error", "Please enter a future time for the deadline.")
                return
            task_list.insert(tk.END, f"{task} - {deadline}")
            threading.Thread(target=notify, args=(task, deadline), daemon=True).start()
            task_entry.delete(0, tk.END)
            deadline_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Format Error", "Deadline format must be YYYY-MM-DD HH:MM")
    else:
        messagebox.showwarning("Input Error", "Please enter both task and deadline")

# GUI Setup
root = tk.Tk()
root.title("Creative Task Manager")
root.geometry("500x600")
root.configure(bg='lightblue')

# Ask for Notification Permission
def ask_notification_permission():
    global notifications_enabled
    allow = messagebox.askyesno("Permission Required", "Do you want to allow task notifications?")
    notifications_enabled = allow

root.after(100, ask_notification_permission)  # Ask shortly after GUI starts

# Clock Image Handling
try:
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Clock_Font_Awesome.svg/1024px-Clock_Font_Awesome.svg.png"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content)).convert("RGBA").resize((100, 100))
        clock_photo = ImageTk.PhotoImage(img)
        clock_label = tk.Label(root, image=clock_photo, bg='lightblue')
        clock_label.pack(pady=10)
except Exception:
    clock_label = tk.Label(root, text="🕒", font=("Arial", 48), bg='lightblue')
    clock_label.pack(pady=10)

# Input Fields
tk.Label(root, text="Enter Task:", bg='lightblue', font=("Arial", 12, "bold")).pack()
task_entry = tk.Entry(root, width=40, font=("Arial", 12))
task_entry.pack(pady=5)

tk.Label(root, text="Enter Deadline (YYYY-MM-DD HH:MM):", bg='lightblue', font=("Arial", 12, "bold")).pack()
deadline_entry = tk.Entry(root, width=40, font=("Arial", 12))
deadline_entry.pack(pady=5)

add_btn = tk.Button(root, text="Add Task", command=add_task, bg='navy', fg='white', font=("Arial", 12, "bold"))
add_btn.pack(pady=10)

task_list = tk.Listbox(root, width=50, height=10, font=("Arial", 11))
task_list.pack(pady=20)

root.mainloop()
