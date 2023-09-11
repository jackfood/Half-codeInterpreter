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

with open('.env', 'r') as env_file:
    env_content = env_file.read()
    env_variables = {}
    exec(env_content, env_variables)
excel_csv_prompt = env_variables['excel_csv_prompt']
python_prompt = env_variables['python_prompt']
data_analyse_prompt = env_variables['data_analyse_prompt']


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
    result_text.insert(tk.END, "..\n")
    result_text.config(state=tk.DISABLED)

    def update_result():
        error_found = False  # Flag to check if 'error' is found in the output
        while True:
            output = running_process.stdout.readline()
            if output == '' and running_process.poll() is not None:
                break
            if output:
                result_text.config(state=tk.NORMAL)
                result_text.insert(tk.END, output)
                result_text.config(state=tk.DISABLED)
                result_text.see(tk.END)
                if 'error' in output.lower():  # Check if 'error' is present in the output
                    error_found = True
            time.sleep(0.1)

        if error_found:
            # If 'error' was found, copy the entire result_text to the clipboard
            root.clipboard_clear()
            root.clipboard_append(result_text.get("1.0", tk.END))
            root.update()  # Update the clipboard
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

    code = f'''{excel_csv_prompt}
Excel file: {input_location}
Save to directory if needed: {output_location}'''
    code_entry.delete("1.0", tk.END)
    code_entry.insert(tk.END, code)
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Paste prompt into ChatGPT\n")
    result_text.config(state=tk.DISABLED)

def process_python_prompt_option():
    code = f'''{python_prompt}'''
    code_entry.delete("1.0", tk.END)
    code_entry.insert(tk.END, code)
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Copy above python prompt into ChatGPT\n")
    result_text.config(state=tk.DISABLED)

def process_python_prompt_Analyse_S1():
    input_location_2 = filedialog.askopenfilename(title="Select Excel/CSV Input File", filetypes=[("Excel/CSV Files", "*.xlsx *.csv")])
    if not input_location_2:
        messagebox.showerror("Error", "Input location cannot be empty.")
        return

    code = f'''{data_analyse_prompt}'''
    
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
            root.after(1000, check_clipboard)

    check_clipboard()


root = tk.Tk()
root.title("Python Code Runner Lite v1.1.6")

menu_bar = Menu(root)
root.config(menu=menu_bar)

# Add "Excel/CSV Option" to the "Options" menu.
menu_bar.add_command(label="Excel/CSV Option", command=process_excel_csv_option)
menu_bar.add_command(label="List Python Scripts", command=list_python_scripts)
menu_bar.add_command(label="Python Prompt", command=process_python_prompt_option)
menu_bar.add_command(label="Anaylse Excel Step 1", command=process_python_prompt_Analyse_S1)


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
