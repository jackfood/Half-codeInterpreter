import tkinter as tk
from tkinter import scrolledtext, Menu, Button, messagebox, simpledialog, filedialog
import subprocess
import os
import threading
import time

running_process = None
last_code = ""
listening_clipboard = False

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

            code_entry.delete("1.0", tk.END)
            code_entry.insert(tk.END, script_content)  # Paste the script into the code entry window

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

    code = f'''
You are an expert Python developer with an AI interpreter called 'Code Interpreter.' You are ready to help me analyze Excel or csv data, or any other format and perform various data analysis and visualization tasks. You will respond with comprehensive high level Python code tailored to my needs, whether it's data exploration, cleaning, analysis, or finding the right dataset. You will avoid using comments (#) or explanations, providing me with clean and efficient code. 

In each step below, you will write a python and until you have a clear understanding of the data then you are allowed to move to the next step. The flow as such,
1. Explore the Data to get an initial understanding of my data.
2. Checking and handle missing values by either removing rows/columns or imputing them with mean, median, mode, or custom values.
3. Detect and handle duplicate data
4. Correct data types and Rename columns for clarity if needed.
5. Encode categorical variables using one-hot encoding or label encoding
6. Scale or standardize numerical features if necessary 
7. Create new features or derive insights from existing ones.

With each step, rewrite python for importing necessary dependencies and the data file directory.
The file is located in {input_location} and the save directory should be in {output_location}.
'''
    code_entry.delete("1.0", tk.END)
    code_entry.insert(tk.END, code)

def process_python_prompt_option():
    code = f'''
You are an expert Python developer. You are ready to help me create or debug a Python script. You will respond with comprehensive high level Python code tailored to my needs, with exceptional debugging skills. With request for adding features, you will try to minimize change to my original python code and without removing any of the functionality, unless i asked you to. You will avoid using comments (#) or explanations, providing me with clean and efficient code. You will reply with the whole python code in code block, and provide a overview of what you changed in code block.
'''
    code_entry.delete("1.0", tk.END)
    code_entry.insert(tk.END, code)

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
        global listening_clipboard  # Add this line to access the global variable
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
            root.after(2000, check_clipboard)

    check_clipboard()


root = tk.Tk()
root.title("Python Code Runner Lite v1.1")

menu_bar = Menu(root)
root.config(menu=menu_bar)

# Add "Excel/CSV Option" to the "Options" menu.
menu_bar.add_command(label="Excel/CSV Option", command=process_excel_csv_option)
menu_bar.add_command(label="List Python Scripts", command=list_python_scripts)
menu_bar.add_command(label="Python Prompt", command=process_python_prompt_option)

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
