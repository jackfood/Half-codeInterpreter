import tkinter as tk
from tkinter import scrolledtext, Menu, Button, messagebox, simpledialog, filedialog
import subprocess
import os
import threading
import time
import pyautogui

running_process = None
last_code = ""
listening_clipboard = False

# Load environment variables from .env file
with open('.env', 'r') as env_file:
    env_content = env_file.read()
    env_variables = {}
    exec(env_content, env_variables)
excel_csv_prompt = env_variables['excel_csv_prompt']
python_prompt = env_variables['python_prompt']
data_analyse_prompt = env_variables['data_analyse_prompt']
chain_of_thought = env_variables['chain_of_thought']

def update_result_text(message, state):
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, message)
    result_text.config(state=state)

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
    
    update_result_text("..\n", tk.DISABLED)

    def update_result():
        error_found = False
        while True:
            output = running_process.stdout.readline()
            if output == '' and running_process.poll() is not None:
                break
            if output:
                result_text.config(state=tk.NORMAL)
                result_text.insert(tk.END, output)
                result_text.config(state=tk.DISABLED)
                result_text.see(tk.END)
                if 'error' in output.lower():
                    error_found = True
            time.sleep(0.1)

        if error_found:
            root.clipboard_clear()
            root.clipboard_append(result_text.get("1.0", tk.END))
            root.update()
            if listening_clipboard:
                root.after(1000, lambda: pyautogui.hotkey('ctrl', 'v'))
                root.after(1500, lambda: pyautogui.press('enter'))

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

            code_entry.delete("1.0", tk.END)
            code_entry.insert(tk.END, script_content)

            root.clipboard_clear()
            root.clipboard_append(script_content)
            scripts_window.destroy()

    copy_button = tk.Button(scripts_window, text="Copy Script to Clipboard", command=on_script_selected)
    copy_button.pack()

def process_excel_csv_option():
    input_location = filedialog.askopenfilename(title="Select Excel/CSV Input File", filetypes=[("Excel/CSV Files", "*.xlsx *.csv")])
    if not input_location:
        messagebox.showerror("Error", "Input location cannot be empty.")
        return

    output_location = filedialog.askdirectory(title="Select Output Directory")
    if not output_location:
        messagebox.showerror("Error", "Output location cannot be empty.")
        return

    code = f'''{excel_csv_prompt}
Excel file: {input_location}
Save to directory if needed: {output_location}'''

    code_entry.delete("1.0", tk.END)
    code_entry.insert(tk.END, code)
    update_result_text("Paste prompt into ChatGPT\n", tk.DISABLED)

def process_chain_of_thought():
    question_COT = simpledialog.askstring("Enter Your Question", "Enter Your Question:", parent=root)
    if question_COT is not None:
        code = f'''{chain_of_thought} {question_COT}'''
        code_entry.delete("1.0", tk.END)
        code_entry.insert(tk.END, code)
        update_result_text("Copy above python prompt into ChatGPT\n", tk.DISABLED)

    # Bind Enter key to trigger 'OK' button
    root.bind('<Return>', lambda event=None: root.focus_force())

def process_python_prompt_option():
    code = f'''{python_prompt}'''
    code_entry.delete("1.0", tk.END)
    code_entry.insert(tk.END, code)
    update_result_text("Copy above python prompt into ChatGPT\n", tk.DISABLED)

def process_python_prompt_Analyse_S1():
    input_location_2 = filedialog.askopenfilename(title="Select Excel/CSV Input File", filetypes=[("Excel/CSV Files", "*.xlsx *.csv")])
    if not input_location_2:
        messagebox.showerror("Error", "Input location cannot be empty.")
        return

    code = f'''import pandas as pd
import os
file_path = r"{input_location_2}"
{data_analyse_prompt}'''
    
    code_entry.delete("1.0", tk.END)
    code_entry.insert(tk.END, code)
    save_and_run_python_code()

def auto_paste_and_execute():
    global listening_clipboard
    listening_clipboard = not listening_clipboard
    if listening_clipboard:
        auto_paste_button.config(text="Disable Auto Paste & Execute")
    else:
        auto_paste_button.config(text="Enable Auto Paste & Execute")

    clipboard_content = ""

    def check_clipboard():
        nonlocal clipboard_content
        global listening_clipboard
        if listening_clipboard:
            new_content = root.clipboard_get()
            if new_content != clipboard_content and 'import' in new_content:
                clipboard_content = new_content
                code_entry.delete("1.0", tk.END)
                code_entry.insert(tk.END, clipboard_content)
                save_and_run_python_code()
                if 'import matplotlib' in clipboard_content:
                    listening_clipboard = False
                    auto_paste_button.config(text="Enable Auto Paste & Execute")
            root.after(1000, check_clipboard)

    check_clipboard()

root = tk.Tk()
root.title("Python Code Runner Lite v1.1.7")

menu_bar = Menu(root)
root.config(menu=menu_bar)

analysis_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Analysis Options", menu=analysis_menu)
analysis_menu.add_command(label="Excel/CSV Option", command=process_excel_csv_option)
analysis_menu.add_command(label="Analyse Excel Step 1", command=process_python_prompt_Analyse_S1)

menu_bar.add_command(label="List Python Scripts", command=list_python_scripts)

python_prompt_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Python Prompts", menu=python_prompt_menu)
python_prompt_menu.add_command(label="Chain of Thought", command=process_chain_of_thought)
python_prompt_menu.add_command(label="Python Prompt", command=process_python_prompt_option)

code_label = tk.Label(root, text="Enter Python Code:")
code_label.pack()

code_frame = tk.Frame(root)
code_frame.pack(fill=tk.BOTH, expand=True)

code_entry = scrolledtext.ScrolledText(code_frame, height=10, width=40)
code_entry.pack(fill=tk.BOTH, expand=True)

save_and_run_button = tk.Button(root, text="Save and Run Code", command=save_and_run_python_code)
save_and_run_button.pack()

auto_paste_button = tk.Button(root, text="Enable Auto Paste & Execute", command=auto_paste_and_execute)
auto_paste_button.pack()

result_text = scrolledtext.ScrolledText(root, height=10, width=40, bg="black", fg="white")
result_text.pack(fill=tk.BOTH, expand=True)
result_text.config(state=tk.DISABLED)

root.mainloop()
