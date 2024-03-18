import tkinter as tk
from tkinter import scrolledtext, Menu, Button, messagebox, simpledialog, filedialog
import subprocess
import os
import threading
import time
import pyautogui

running_process = None
last_code = None
listening_clipboard = False
print("auto_paste - Off")

# Load environment variables from .env2 file
with open('.env2', 'r', encoding='utf-8') as env_file:
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
prompt_generator_prompt = env_variables['prompt_generator']
table_organizer_prompt = env_variables['table_organizer']
summarise_text_prompt = env_variables['summarise_text']
ai_writing_assistant_prompt = env_variables['ai_writing_assistant']
unrestricted_opinion_prompt = env_variables['unrestricted_opinion']
cohesion_and_engagement_improver_prompt = env_variables['cohesion_and_engagement_improver']
professional_writer_prompt = env_variables['professional_writer']
vision_lmstudio_prompt = env_variables['vision_lmstudio']
# = env_variables['']
# = env_variables['']
# = env_variables['']


def update_result_text(message, state):
    print("def update_result_text")
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, message)
    result_text.config(state=state)
    print("def update_result_text completed")

def web_chatgpt_autoclick():
    print("def web_chatgpt_autoclick")
    chatgpt_send_msg = pyautogui.locateCenterOnScreen("a_sendmsg.png", grayscale=True, confidence=0.8)
    pyautogui.moveTo(chatgpt_send_msg)
    print(chatgpt_send_msg)
    pyautogui.click()
    time.sleep(0.3)
    root.after(500, lambda: pyautogui.hotkey('ctrl', 'v'))
    time.sleep(1)
    chatgpt_entry = pyautogui.locateCenterOnScreen("a_chatgptarrow.png", grayscale=True, confidence=0.8)
    pyautogui.moveTo(chatgpt_entry)
    print(chatgpt_entry)
    pyautogui.click()
    time.sleep(0.3)
    chatgpt_arrow_down = pyautogui.locateCenterOnScreen("a_arrowdown.png", grayscale=True, confidence=0.9)
    pyautogui.moveTo(chatgpt_arrow_down)
    print(chatgpt_arrow_down)
    pyautogui.click()
    time.sleep(0.3)

def save_and_run_python_code():
    print("def save_and_run_python_code")
    update_result_text("", tk.DISABLED)
    global last_code, running_process
    code = code_entry.get("1.0", "end-1c")
    last_code = code

    if running_process and running_process.poll() is None:
        running_process.kill()
        print("running_process.kill")

    with open('guiscript.py', 'w') as file:
        file.write(code)
        print("writed code to guiscript.txt")
         # Check if code starts with 'pip install'
        if code.strip().startswith('pip install'):
            print("pip install detected")
            # Save it as '_recordpippackage.txt'
            package_name = code.split(' ')[2].strip()
            with open('_recordpippackage.txt', 'w') as record_file:
                record_file.write(package_name)
                print("write _recordpippackage completed")

            # Define the pip install command as a list
            pip_install_command = ["pip", "install", package_name]

            print(f"Installing pip package {package_name}..\n")
            update_status_pip = f"Installing pip package {package_name}..\n"
            result_text.config(state=tk.NORMAL)
            result_text.insert(tk.END, update_status_pip)

            try:
                # Use subprocess to run the pip install command
                status_update_pip_install = subprocess.run(pip_install_command, check=True, capture_output=True, text=True)
                print(f"-- Successfully installed {package_name} -- \n{status_update_pip_install.stdout}")
                update_status_pip_success = f"Successfully installed {package_name}..:\n{status_update_pip_install.stdout}\n\n"
                result_text.config(state=tk.NORMAL)
                result_text.insert(tk.END, update_status_pip_success)
                root.clipboard_clear()
                root.clipboard_append(update_status_pip_success)

            except subprocess.CalledProcessError as e:
                print(f"-- Failed to install {package_name}: {e} --")
                update_status_pip_failed = f"Failed to install {package_name}:{e}"
                result_text.config(state=tk.NORMAL)
                result_text.insert(tk.END, update_status_pip_failed)
                root.clipboard_clear()
                root.clipboard_append(update_status_pip_failed)

            if os.path.exists('_recordpippackage.txt'):
                os.remove('_recordpippackage.txt')
                print(f"Removed _recordpippackage.txt\n")
                return
            
        # Check if code starts with 'pip uninstall'    
        elif code.strip().startswith('pip uninstall'):
            print("pip uninstall detected")
            # Save it as '_recordpippackage.txt'
            package_name = code.split(' ')[2].strip()
            with open('_recordpippackage.txt', 'w') as record_file:
                record_file.write(package_name)
                print("write _recordpippackage completed")

            try:      
                pip_uninstall_command = ["pip", "uninstall", "-y", package_name]
                status_update_pip_uninstall = subprocess.run(pip_uninstall_command, check=True, stdout=subprocess.PIPE, text=True)
                print(f"Uninstalling pip package {package_name}..\n")
                result_text.config(state=tk.NORMAL)
                # status_update_pip_uninstall = subprocess.run(pip_uninstall_command, check=True, stdout=subprocess.PIPE, text=True)
                print(f"-- Successfully uninstalled {package_name} -- \n{status_update_pip_uninstall.stdout}")
                update_status_unpip_success = f"{status_update_pip_uninstall.stdout}"
                result_text.config(state=tk.NORMAL)
                result_text.insert(tk.END, update_status_unpip_success)
                root.clipboard_clear()
                root.clipboard_append(update_status_unpip_success)

            except subprocess.CalledProcessError as e:
                print(f"-- Failed to uninstall {package_name}: {e} --")
                update_status_pip_failed = f"Failed to uninstall {package_name}::\n{e}"
                result_text.config(state=tk.NORMAL)
                result_text.insert(tk.END, update_status_pip_failed)
                root.clipboard_clear()
                root.clipboard_append(update_status_pip_failed)

            if os.path.exists('_recordpippackage.txt'):
                os.remove('_recordpippackage.txt')
                print(f"Removed _recordpippackage.txt\n")
                return
            
        else:
            #Run Python Code
            command = ["python", "guiscript.py"]
            print(f"Activate command python.txt")

            update_status_py = "Python..."
            print("Running Python...")
            running_process = subprocess.Popen(
                command, cwd=os.getcwd(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

            result_text.config(state=tk.NORMAL)
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, update_status_py)
            print(f"{running_process}")

            def update_result():
                print("def update_result")
                error_found = False
                while True:
                    output = running_process.stdout.readline()
                    if output == '' and running_process.poll() is not None:
                        break
                    if output:
                        print(f"{output}")
                        result_text.config(state=tk.NORMAL)
                        result_text.insert(tk.END, output)
                        print("def update_result - output updated")
                        if 'error' in output.lower():
                            error_found = True
                            print("def update_result - Error True")
                    time.sleep(0.10)

                if error_found:
                    root.clipboard_clear()
                    root.clipboard_append(result_text.get("1.0", tk.END))
                    print(result_text.get("1.0", tk.END))
                    root.update()

                elif result_text.get("1.0", tk.END).strip() == "Python..." or not result_text.get("1.0", tk.END).strip():
                    status_in_clipboard_success = "Python Executed Successfully"
                    result_text.delete("1.0", tk.END)
                    result_text.insert(tk.END, status_in_clipboard_success)
                    print("def update_result - python ran but result_text is empty")
                    root.clipboard_clear()
                    root.clipboard_append(result_text.get("1.0", tk.END))
                    print("def update_result - Clipboard updated as Python Executed Successfully")
                    root.update()

                else:
                    root.clipboard_clear()
                    root.clipboard_append(result_text.get("1.0", tk.END))
                    print(result_text.get("1.0", tk.END))
                    root.update()

            update_result_thread = threading.Thread(target=update_result)
            update_result_thread.start()
            print(f"update_result_thread.start")

def list_python_scripts():
    print("def list_python_scripts started.")
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
    print("def process_excel_csv_option started.")
    input_location = filedialog.askopenfilename(title="Select Excel/CSV Input File", filetypes=[("Excel/CSV Files", "*.xlsx *.csv")])
    if not input_location:
        messagebox.showerror("Error", "Input location cannot be empty.")
        print("messagbox.showerror - input location empty")
        return

    output_location = filedialog.askdirectory(title="Select Output Directory")
    if not output_location:
        messagebox.showerror("Error", "Output location cannot be empty.")
        print("messagbox.showerror - location empty")
        return

    code = f'''{excel_csv_prompt}
Excel file: {input_location}
Save to directory if needed: {output_location}'''
    code_entry.delete("1.0", tk.END)
    code_entry.insert(tk.END, code)
    update_result_text("Copy above python prompt into ChatGPT\n", tk.DISABLED)
    print("Completed/n")

def insert_code_into_entry(code):
    print("def insert_code_into_entry")
    code_entry.delete("1.0", tk.END)
    code_entry.insert(tk.END, code)
    update_result_text("Code input sucessfully\n", tk.DISABLED)
    print("Completed/n")

def process_chain_of_thought():
    print("def process_chain_of_thought started.")
    question_COT = simpledialog.askstring("Enter Your Question", "Enter Your Question:", parent=root)
    if question_COT is not None:
        code = f'''{chain_of_thought} {question_COT}'''
        insert_code_into_entry(code)

    # Bind Enter key to trigger 'OK' button
    root.bind('<Return>', lambda event=None: root.focus_force())
    print("Completed/n")

def vision_lmstudio():
    code = f'''{vision_lmstudio_prompt}'''
    insert_code_into_entry(code)
    print("Ensure LMstudio server is on")
    save_and_run_python_code()

def process_python_prompt_option():
    code = f'''{python_prompt}'''
    insert_code_into_entry(code)
    print("process_python_prompt_option selected")

def process_checkeng_prompt_option():
    code = f'''{checkeng_prompt}'''
    insert_code_into_entry(code)
    print("process_checkeng_prompt_option selected")

def process_visualization_mermaid():
    code = f'''{visualization_mermaid}'''
    insert_code_into_entry(code)
    print("process_visualization_mermaid selected")

def process_pyoptimise():
    code = f'''{python_optimise_prompt}'''
    insert_code_into_entry(code)
    print("process_pyoptimise selected")

def prompt_generator():
    code = f'''{prompt_generator_prompt}'''
    insert_code_into_entry(code)
    print("prompt_generator selected")
def table_organizer():
    code = f'''{table_organizer_prompt}'''
    insert_code_into_entry(code)
    print("table_organizer selected")
def summarise_text():
    code = f'''{summarise_text_prompt}'''
    insert_code_into_entry(code)
    print("summarise_text selected")
def ai_writing_assistant():
    code = f'''{ai_writing_assistant_prompt}'''
    insert_code_into_entry(code)
    print("ai_writing_assistant selected")
def unrestricted_opinion():
    code = f'''{unrestricted_opinion_prompt}'''
    insert_code_into_entry(code)
    print("unrestricted_opinion selected")
def cohesion_and_engagement_improver():
    code = f'''{cohesion_and_engagement_improver_prompt}'''
    insert_code_into_entry(code)
    print("cohesion_and_engagement_improver selected")

def professional_writer():
    code = f'''{professional_writer_prompt}'''
    insert_code_into_entry(code)
    print("professional_writer selected")

def process_python_prompt_Analyse_S1():
    print("process_python_prompt_Analyse_S1 selected")
    input_location_2 = filedialog.askopenfilename(title="Select Excel/CSV Input File", filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")])
    if not input_location_2:
        messagebox.showerror("Error", "Input location cannot be empty.")
        print("process_python_prompt_Analyse_S1 messagebox.showerror")
        return

    code = f'''
import pandas as pd

file_path = r"{input_location_2}"
{data_analyse_prompt}
'''
    code_entry.delete("1.0", tk.END)
    code_entry.insert(tk.END, code)
    save_and_run_python_code()
    print("process_python_prompt_Analyse_S1 running code")

def process_python_prompt_Analyse_S2():
    print("process_python_prompt_Analyse_S2 started. Starting new options.")
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
root.title("Python Code Runner Lite v1.6")
print("Creating form.")

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
gpt_prompt_menu.add_command(label="Prompt Generator", command=prompt_generator)
gpt_prompt_menu.add_command(label="Table Organizer", command=table_organizer)
gpt_prompt_menu.add_command(label="Summarise Text", command=summarise_text)
gpt_prompt_menu.add_command(label="AI writing assistant", command=ai_writing_assistant)
gpt_prompt_menu.add_command(label="Unrestricted Opinion Prompt", command=unrestricted_opinion)
gpt_prompt_menu.add_command(label="Flow and Cohesion of Sentence Improver", command=cohesion_and_engagement_improver)
gpt_prompt_menu.add_command(label="Professional Writer", command=professional_writer)
# gpt_prompt_menu.add_command(label="Image Vision Analyser - LMstudio", command=vision_lmstudio)
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

# Create and configure menu
vision_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Image analyse", command=vision_lmstudio)

code_label = tk.Label(root, text="Enter Python Code:")
code_label.pack()

code_frame = tk.Frame(root)
code_frame.pack(fill=tk.BOTH, expand=True)

code_entry = scrolledtext.ScrolledText(code_frame, height=15, width=50)
code_entry.pack(fill=tk.BOTH, expand=True)

save_and_run_button = tk.Button(root, text="Run Code", command=save_and_run_python_code)
save_and_run_button.pack()

result_text = scrolledtext.ScrolledText(root, height=10, width=40, bg="black", fg="white")
result_text.pack(fill=tk.BOTH, expand=True)
result_text.config(state=tk.DISABLED)
print("Form Creation Completed.")

root.mainloop()
