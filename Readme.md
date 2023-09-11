# Python Code Runner Lite (Half Code interpreter) for Data Analysis

This code is made by GPT 3.5 turbo on my idea. I have no coding experience.

This Python code runner (Half Code interpreter) with a graphical user interface (GUI) aims to mimic the behavior of Code Interpreter in GPT-4, where code execution happens locally. 
Please note that for error prompt assistance after execute the code, you will input copy errors to the web version of ChatGPT 3.5 Turbo (OpenAI account required) or other generative AI services (e.g. Claude 2, poe) for debugging. (ensure Mouse Cursor / focus is on the input text if automatic listening is on)

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
- **(Main Feature) Auto Paste & Execute:** Automatically paste code from the clipboard and execute it when the word 'import' is detected. Using the web version of generative AI with an embedded code block can be useful. You can simply click the 'Copy' button within the code block to copy the code to your clipboard. This action leads to the immediate execution of the copied Python code. If an error is detected, this will again automatically copies the error message back to your clipboard. This facilitates the process of debugging or further processing by allowing you to easily return the error message to the web generative AI, which is very similar to the existing code interpreter in GPT-4.

## Requirements

Before using this tool, ensure that you have the following installed:

- Python 3.x
- tkinter library (usually included in Python standard library)
- pandas library (for Excel/CSV processing)
- subprocess library (for running Python scripts)
- matplotlib library (for data visualization)

You can install the required Python libraries using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Executing Python Code

1. Enter your Python code in the text area labeled "Enter Python Code."

2. Click the "Save and Run Code" button to execute the code. The output will be displayed in the lower text area.

3. If an error occurs during code execution, the error message will be automatically copied to the clipboard for your convenience. Seek assistance in the web version of ChatGPT 3.5 Turbo (OpenAI account required) by pasting the error.

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

- When enabled, the tool will periodically (every 2 seconds) check your clipboard for Python code. If it detects the word 'import' in your clipboard, it will automatically paste and execute the code. It also compares whether the data in the existing python code input area is the same as the clipboard data. If it is the same, it will prevent copying and execute the code to prevent duplicate running of the code every 2 seconds, afterwhich, it will continue to listen until user clicked on the "Disable Auto Paste & Execute" button.

- To disable this feature, click the "Disable Auto Paste & Execute" button.

## Running 'code.py'

After setting up the requirements, you can run the 'code.py' file in your Python environment to launch the Python Code Runner Lite.

## Contributing

If you would like to contribute to this project, please feel free to submit issues or pull requests on the GitHub repository.
