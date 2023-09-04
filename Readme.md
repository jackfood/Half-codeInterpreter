# Python Code Runner Lite (Half Code interpreter) for Data Analysis

This Python code runner (Half Code interpreter) with a graphical user interface (GUI) aims to mimic the behavior of Code Interpreter in GPT-4, where code execution happens locally. 
Please note that for error prompt assistance, you must manually copy errors and use the web version of ChatGPT 3.5 Turbo (OpenAI account required).

Certainly, I've updated the README to include running 'code.py' in a Python environment and highlighted the main feature of auto-listening to clipboard changes:

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Usage](#usage)
  - [Executing Python Code](#executing-python-code)
  - [Handling Excel/CSV Files](#handling-excelcsv-files)
  - [Working with Python Prompts](#working-with-python-prompts)
- [Auto Paste & Execute](#auto-paste--execute)
- [Running 'code.py'](#running-codepy)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Execute Python Code:** Write and execute Python code snippets or scripts within the GUI.
- **Interactive with ChatGPT:** Utilize the built-in interface with ChatGPT for code generation and debugging. Please note that this tool does not execute code in the background like GPT-4; you must manually run the code.
- **Handle Excel/CSV Data Analysis:** Simplify data analysis tasks for Excel and CSV files. Generate Python code snippets to assist in data exploration, cleaning, and analysis.
- **List Python Scripts:** View a list of Python scripts in your directory and select them for editing.
- **Auto Paste & Execute:** Automatically paste code from the clipboard and execute it when the word 'import' is detected.

## Requirements

Before using this tool, ensure that you have the following installed:

- Python 3.x
- tkinter library (usually included in Python standard library)
- pandas library (for Excel/CSV processing)
- subprocess library (for running Python scripts)
- matplotlib library (for data visualization)

You can install the required Python libraries using pip:

```bash
pip install pandas matplotlib
```

## Usage

### Executing Python Code

1. Enter your Python code in the text area labeled "Enter Python Code."

2. Click the "Save and Run Code" button to execute the code. The output will be displayed in the lower text area.

3. If an error occurs during code execution, manually copy the error message and seek assistance in the web version of ChatGPT 3.5 Turbo (OpenAI account required).

### Handling Excel/CSV Files

1. Click on the "Excel/CSV Option" in the "Options" menu.

2. Select an Excel or CSV file when prompted.

3. Select an output directory where the processed data or code will be saved.

4. The code for handling Excel/CSV data will be automatically generated in the code entry area. You can modify it as needed.

### Working with Python Prompts

1. You can use the "Python Prompt" option in the "Options" menu to generate Python code prompts for various tasks.

2. After selecting a prompt, the corresponding Python code will be generated in the code entry area. You can then execute it or modify it as needed.

3. For specific prompts, such as "Analyse Excel Step 1," you will be prompted to select an Excel or CSV file. The code generated will be tailored to analyzing the selected data.

## Auto Paste & Execute

- Click the "Enable Auto Paste & Execute" button to enable automatic code pasting and execution.

- When enabled, the tool will periodically check your clipboard for Python code. If it detects the word 'import' in your clipboard, it will automatically paste and execute the code.

- To disable this feature, click the "Disable Auto Paste & Execute" button.

## Running 'code.py'

After setting up the requirements, you can run the 'code.py' file in your Python environment to launch the Python Code Runner Lite.

## Contributing

If you would like to contribute to this project, please feel free to submit issues or pull requests on the GitHub repository.
