import tkinter as tk
from tkinter import scrolledtext, Menu, Button, messagebox
import subprocess
import os
import threading
import time

running_process = None
last_code = ""

def save_and_run_python_code():
    global last_code, running_process
    code = code_entry.get("1.0", "end-1c")
    last_code = code

    if running_process and running_process.poll() is None:
        running_process.kill()

    with open('guiscript.py', 'w') as file:
        file.write(code)

    command = ["python", "guiscript.py"]
    running_process = subprocess.Popen(
        command, cwd=os.getcwd(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Running the script...\n")
    result_text.config(state=tk.DISABLED)

    def update_result():
        while True:
            output = running_process.stdout.readline()
            if output == '' and running_process.poll() is not None:
                break
            if output:
                result_text.config(state=tk.NORMAL)
                result_text.insert(tk.END, output)
                result_text.config(state=tk.DISABLED)
                result_text.see(tk.END)
            time.sleep(0.1)

    update_result_thread = threading.Thread(target=update_result)
    update_result_thread.start()

def list_python_scripts():
    scripts_window = tk.Toplevel(root)
    scripts_window.title("List of Python Scripts")
    script_listbox = tk.Listbox(scripts_window)
    script_listbox.pack(fill=tk.BOTH, expand=True)

    scripts = [file for file in os.listdir() if file.endswith(".py")]
    for script in scripts:
        script_listbox.insert(tk.END, script)

    def on_script_selected():
        selected_index = script_listbox.curselection()
        if selected_index:
            selected_script = script_listbox.get(selected_index)
            with open(selected_script, 'r') as file:
                script_content = file.read()

            root.clipboard_clear()
            root.clipboard_append(script_content)
            scripts_window.destroy()

    copy_button = tk.Button(scripts_window, text="Copy Script to Clipboard", command=on_script_selected)
    copy_button.pack()

root = tk.Tk()
root.title("Python Code Runner Lite v1.0")

menu_bar = Menu(root)
root.config(menu=menu_bar)

scripts_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Scripts", menu=scripts_menu)
scripts_menu.add_command(label="List Python Scripts", command=list_python_scripts)

code_label = tk.Label(root, text="Enter Python Code:")
code_label.pack()

code_frame = tk.Frame(root)
code_frame.pack(fill=tk.BOTH, expand=True)

code_entry = scrolledtext.ScrolledText(code_frame, height=10, width=40)
code_entry.pack(fill=tk.BOTH, expand=True)

save_and_run_button = tk.Button(root, text="Save and Run Code", command=save_and_run_python_code)
save_and_run_button.pack()

result_text = scrolledtext.ScrolledText(root, height=10, width=40, bg="black", fg="white")
result_text.pack(fill=tk.BOTH, expand=True)
result_text.config(state=tk.DISABLED)

root.mainloop()
