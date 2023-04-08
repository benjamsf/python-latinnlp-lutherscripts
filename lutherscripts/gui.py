import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import subprocess

__author__ = "benjamsf"
__license__ = "MIT"

def gui_main():

# create the main window
    root = tk.Tk()
    root.title("LutherScript v0.1.0 - Latin NLP Toolset")

# create the tabs
    tab_parent = ttk.Notebook(root)
    tab1 = ttk.Frame(tab_parent)
    tab2 = ttk.Frame(tab_parent)
    tab3 = ttk.Frame(tab_parent)
    tab_parent.add(tab1, text="Config")
    tab_parent.add(tab2, text="Text Preparation")
    tab_parent.add(tab3, text="Text Processing")
    tab_parent.pack(expand=1, fill='both')

# create widgets for Config tab
    lbl_raw_sourcetext = tk.Label(tab1, text="Choose raw source text:")
    lbl_raw_sourcetext.pack(side=tk.LEFT, padx=10, pady=10)
    btn_raw_sourcetext = tk.Button(tab1, text="Browse...", command=lambda: choose_file())
    btn_raw_sourcetext.pack(side=tk.LEFT, padx=10, pady=10)

    file_label = tk.StringVar()
    file_label.set("No file selected")
    lbl_selected_file = tk.Label(tab1, textvariable=file_label)
    lbl_selected_file.pack(side=tk.LEFT, padx=10, pady=10)

# function to choose file and store the location in a variable
    def choose_file():
        global location_raw_sourcetext
        location_raw_sourcetext = filedialog.askopenfilename(title="Select a File", initialdir=os.path.dirname(os.path.abspath(__file__)))
        file_label.set(location_raw_sourcetext)
        print(f"File selected: {location_raw_sourcetext}")

# create widgets for Text Preparation tab
    lbl_operation = tk.Label(tab2, text="Choose Operation:")
    lbl_operation.pack(side=tk.LEFT, padx=10, pady=10)
    options = ["word_tokenize_latin", "sent_tokenize_latin"]
    var_operation = tk.StringVar(tab2)
    var_operation.set(options[0])
    opt_operation = tk.OptionMenu(tab2, var_operation, *options)
    opt_operation.pack(side=tk.LEFT, padx=10, pady=10)

    def run_script():
        global location_raw_sourcetext
        operation_name = var_operation.get()
        cli_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cli.py')
        cli_command = f'python "{cli_path}" -o {operation_name} -s "{location_raw_sourcetext}" -d "output.txt"'
        output = subprocess.getoutput(cli_command)
        txt_terminal.delete(1.0, tk.END)
        txt_terminal.insert(tk.END, output)

    btn_play = tk.Button(tab2, text="Play!", command=run_script)
    btn_play.pack(side=tk.LEFT, padx=10, pady=10)

    txt_terminal = tk.Text(tab2, height=10, width=50)
    txt_terminal.pack(side=tk.BOTTOM, padx=10, pady=10)

# create widgets for Text Processing tab
    lbl_nothing = tk.Label(tab3, text="Nothing so far.")
    lbl_nothing.pack(side=tk.LEFT, padx=10, pady=10)

# start the GUI
    root.mainloop()
