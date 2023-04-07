import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import subprocess

# create the main window
root = tk.Tk()
root.title("NLP Text Analysis")

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

# function to choose file and store the location in a variable
def choose_file():
    global location_raw_sourcetext
    location_raw_sourcetext = filedialog.askopenfilename(title="Select a File")
    print(f"File selected: {location_raw_sourcetext}")

# create widgets for Text Preparation tab
lbl_operation = tk.Label(tab2, text="Choose Operation:")
lbl_operation.pack(side=tk.LEFT, padx=10, pady=10)
options = ["cltk_sentencetokenize_latin.py", "cltk_wordtokenize_latin.py"]
var_operation = tk.StringVar(tab2)
var_operation.set(options[0])
opt_operation = tk.OptionMenu(tab2, var_operation, *options)
opt_operation.pack(side=tk.LEFT, padx=10, pady=10)

def run_script():
    global location_raw_sourcetext
    global process
    script_name = var_operation.get()
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../text_preparation", script_name)
    process = subprocess.Popen(f"python {script_path} {location_raw_sourcetext}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            txt_terminal.insert(tk.END, output.decode('utf-8'))
    rc = process.poll()
    print(f"Return code: {rc}")
    
btn_play = tk.Button(tab2, text="Play!", command=run_script)
btn_play.pack(side=tk.LEFT, padx=10, pady=10)

txt_terminal = tk.Text(tab2, height=10, width=50)
txt_terminal.pack(side=tk.BOTTOM, padx=10, pady=10)

# create widgets for Text Processing tab
lbl_nothing = tk.Label(tab3, text="Nothing so far.")
lbl_nothing.pack(side=tk.LEFT, padx=10, pady=10)

# start the GUI
root.mainloop()
