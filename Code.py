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


# Load environment variables from .env2 file
with open('.env2', 'r') as env_file:
    env_content = env_file.read()
    env_variables = {}
    exec(env_content, env_variables)
excel_csv_prompt = env_variables['excel_csv_prompt']
python_prompt = env_variables['python_prompt']
data_analyse_prompt = env_variables['data_analyse_prompt']
chain_of_thought = env_variables['chain_of_thought']
checkeng_prompt = env_variables['checkeng_prompt']
visualization_mermaid = env_variables['visualization_mermaid']
python_optimise_prompt = env_variables['python_optimise_prompt']
# = env_variables['']
# = env_variables['']


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
    update_result_text("Copy above python prompt into ChatGPT\n", tk.DISABLED)

# Add insert code function ####################
def insert_code_into_entry(code):
    code_entry.delete("1.0", tk.END)
    code_entry.insert(tk.END, code)
    update_result_text("Copy above python prompt into ChatGPT\n", tk.DISABLED)

def process_chain_of_thought():
    question_COT = simpledialog.askstring("Enter Your Question", "Enter Your Question:", parent=root)
    if question_COT is not None:
        code = f'''{chain_of_thought} {question_COT}'''
        insert_code_into_entry(code)

    # Bind Enter key to trigger 'OK' button
    root.bind('<Return>', lambda event=None: root.focus_force())

def process_python_prompt_option():
    code = f'''{python_prompt}'''
    insert_code_into_entry(code)

def process_checkeng_prompt_option():
    code = f'''{checkeng_prompt}'''
    insert_code_into_entry(code)

def process_visualization_mermaid():
    code = f'''{visualization_mermaid}'''
    insert_code_into_entry(code)

def process_pyoptimise():
    code = f'''{python_optimise_prompt}'''
    insert_code_into_entry(code)

def process_python_prompt_Analyse_S1():
    input_location_2 = filedialog.askopenfilename(title="Select Excel/CSV Input File", filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")])
    if not input_location_2:
        messagebox.showerror("Error", "Input location cannot be empty.")
        return

    code = f'''
import pandas as pd

file_path = r"{input_location_2}"
{data_analyse_prompt}
'''

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

def process_python_prompt_Analyse_S2():
    plot_types = [
        "----Select a plot----",
        "Plot Chart",
        "Pie chart",
        "linestyle chart using (-), with butt capstyle",
        "linestyle chart using (-), with round capstyle",
        "linestyle chart using (-), with projecting capstyle",
        "linestyle chart using (!)",
        "linestyle chart using (--) chart",
        "linestyle chart using (0, 0.1, 2) chart",
        "Scatter chart",
        "bar chart",
        "imshow - heatmap chart",
        "contour chart",
        "pcolormesh chart",
        "quiver chart",
        "text chart",
        "fill_between chart",
        "step chart",
        "box plot chart",
        "errorbar chart",
        "histogram chart",
        "violinplot chart",
        "barbs chart",
        "eventplot chart",
        "hexbin chart",
        "linear scale chart",
        "log chart",
        "symlog chart",
        "logit chart",
        "subplot chart"
    ]


    colour_type = [
        "Appropriate colours",
        "Black",
        "Red",
        "Blue",
        "Green",
        "Cyan",
        "Magenta",
        "Yellow",
        "White",
        "Purple",
        "Brown",
        "Orange",
        "Pink",
        "Olive",
        "Teal",
        "Lavender",
        "Maroon",
        "Navy",
        "Turquoise",
        "Gold",
        "Indigo"
    ]

    colour_scheme = [
        "no colour scheme",
        "appropriate colour scheme",
        "-----ColourMaps-----",
        "Uniform - viridis",
        "Uniform - magma",
        "Uniform - plasma",
        "Sequential - grey",
        "Sequential - YlorBr",
        "Sequential - Wistia",
        "Diverging - Spectral",
        "Diverging - Coolwarm",
        "Diverging - RdGy",
        "Qualitative - tab10",
        "Qualitative - tab20",
        "Cyclic - twlight",
    ]

    selected_plot = tk.StringVar(root)
    selected_plot.set(plot_types[0])  # Set the initial value
    selected_color_scheme = tk.StringVar(root)
    selected_color_scheme.set(colour_scheme[0])
    selected_color_type = tk.StringVar(root)
    selected_color_type.set(colour_type[0])

    # Create the OptionMenu with plot types
    plot_type_menu = tk.OptionMenu(root, selected_plot, *plot_types)
    color_scheme_menu = tk.OptionMenu(root, selected_color_scheme, *colour_scheme)
    color_type_menu = tk.OptionMenu(root, selected_color_type, *colour_type)

    plot_type_menu.pack()
    color_scheme_menu.pack()
    color_type_menu.pack()

    def open_dialogs():
        # Function to open input dialogs after plot type selection
        headers_vis = simpledialog.askstring("Type of Variables", "Name your variable for correlation, write as 'name of header 1' and 'name of header 2'", parent=root)
        title_vis = simpledialog.askstring("Title of chart", "Specify Name of title", parent=root)

        code = f'''I want you to act as a data scientist coding in Python strictly without explanation and #. Given the provided dataframe containing the columns, use matplotlib to plot a ({selected_plot.get()}) to visualize the variables ({headers_vis}). Insert title as ({title_vis}). Set the color theme ({selected_color_scheme.get()}) using the main colour as light ({selected_color_type.get()}). Please include the file directory for df in python code block.'''


        insert_code_into_entry(code)
        plot_type_menu.pack_forget()
        color_scheme_menu.pack_forget()
        color_type_menu.pack_forget()
        confirm_button.pack_forget()

    # Create a button to trigger the input dialogs
    confirm_button = tk.Button(root, text="Confirm", command=open_dialogs)
    confirm_button.pack()
root = tk.Tk()
root.title("Python Code Runner Lite v1.2")

menu_bar = Menu(root)
root.config(menu=menu_bar)

# Create and configure menu
analysis_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Analysis Workflow", menu=analysis_menu)
analysis_menu.add_command(label="Step 1 - Define Directory", command=process_excel_csv_option)
analysis_menu.add_command(label="Step 2 - Provide Analyse Info", command=process_python_prompt_Analyse_S1)
analysis_menu.add_command(label="Step 3 - Visualization using Malplotlib", command=process_python_prompt_Analyse_S2)

# Add a command directly to the menu_bar
menu_bar.add_command(label="List Python Scripts", command=list_python_scripts)

# Create and configure menu
gpt_prompt_menu = Menu(menu_bar)
menu_bar.add_cascade(label="ChatGPT prompts", menu=gpt_prompt_menu)
gpt_prompt_menu.add_command(label="English Check", command=process_checkeng_prompt_option)
# gpt_prompt_menu.add_command(label="", command=)
# gpt_prompt_menu.add_command(label="", command=)
# gpt_prompt_menu.add_command(label="", command=)
# gpt_prompt_menu.add_command(label="", command=)


# Create and configure menu
python_prompt_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Python Prompts", menu=python_prompt_menu)
python_prompt_menu.add_command(label="Python Prompt", command=process_python_prompt_option)
python_prompt_menu.add_command(label="Python Code Optimization", command=process_pyoptimise)
python_prompt_menu.add_command(label="Mermaid Flow Diagram Prompt", command=process_visualization_mermaid)
#python_prompt_menu.add_command(label="", command=)


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
