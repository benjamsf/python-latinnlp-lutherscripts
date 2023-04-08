import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import subprocess
import pkg_resources
from pathlib import Path


__author__ = "benjamsf"
__license__ = "MIT"


def create_image_label(parent):
    # Add the image of Martin Luther
    image_bytes = pkg_resources.resource_string("lutherscripts", "luther.gif")

    # Create a PhotoImage from the image bytes
    luther_photo = tk.PhotoImage(data=image_bytes)
    lbl_luther_image = tk.Label(parent, image=luther_photo)
    lbl_luther_image.image = luther_photo
    lbl_luther_image.pack(side=tk.LEFT, padx=10, pady=10)
    return lbl_luther_image


def gui_main():

    root = tk.Tk()
    root.geometry("1400x600")
    root.title("LutherScripts v0.2.0 - A NLP toolset for Latin language")

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
    create_image_label(tab1)
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

    lbl_output_file = tk.Label(tab1, text="Choose output file location:")
    lbl_output_file.pack(side=tk.LEFT, padx=10, pady=10)
    btn_output_file = tk.Button(tab1, text="Browse...", command=lambda: choose_output_file())
    btn_output_file.pack(side=tk.LEFT, padx=10, pady=10)

    output_file_label = tk.StringVar()
    output_file_label.set("No file selected")
    lbl_selected_output_file = tk.Label(tab1, textvariable=output_file_label)
    lbl_selected_output_file.pack(side=tk.LEFT, padx=10, pady=10)

    # function to choose output file and store the location in a variable
    def choose_output_file():
        global location_output
        location_output = filedialog.asksaveasfilename(title="Select output file location", defaultextension=".txt", initialdir=os.path.dirname(os.path.abspath(__file__)))
        output_file_label.set(location_output)
        print(f"Output file selected: {location_output}")


    # create widgets for Text Preparation tab
    create_image_label(tab2)
    lbl_operation = tk.Label(tab2, text="Choose Operation:")
    lbl_operation.pack(side=tk.LEFT, padx=10, pady=10)
    options = [
        ("word_tokenize_latin", "Tokenize Latin text by words"),
        ("sent_tokenize_latin", "Tokenize Latin text by sentences"),
    ]
    var_operation = tk.StringVar(tab2)
    var_operation.set(options[0][1])
    opt_operation = tk.OptionMenu(tab2, var_operation, *[option[1] for option in options])
    opt_operation.pack(side=tk.LEFT, padx=10, pady=10)
    
    explanation_label = tk.StringVar()
    explanation_label.set("This operation will tokenize your Latin text by words, which is required for further word-based natural language processing.")
    lbl_explanation = tk.Label(tab2, textvariable=explanation_label, wraplength=300)
    lbl_explanation.pack(side=tk.LEFT, padx=10, pady=10)

    def run_script():
        global location_raw_sourcetext, location_output_file
        operation_name = [option[0] for option in options if option[1] == var_operation.get()][0]
        cli_command = ['lutherscripts-cli', '-o', operation_name, '-s', os.path.abspath(location_raw_sourcetext), '-d', os.path.abspath(location_output)]
        output = subprocess.check_output(cli_command, encoding='utf-8', stderr=subprocess.STDOUT)
        txt_terminal.delete(1.0, tk.END)
        txt_terminal.insert(tk.END, output)



    btn_play = tk.Button(tab2, text="Play!", command=run_script)
    btn_play.pack(side=tk.LEFT, padx=10, pady=10)

    txt_terminal = tk.Text(tab2, height=20, width=1000)
    txt_terminal.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.BOTH, expand=True)
    tab2.grid_columnconfigure(0, weight=1)

    # create widgets for Text Processing tab
    lbl_nothing = tk.Label(tab3, text="Choose Operation:")
    lbl_nothing.pack(side=tk.LEFT, padx=10, pady=10)

    processing_options = {
        "nltk_do_kwic": "Perform KWIC analysis"
    }
    var_processing_operation = tk.StringVar(tab3)
    var_processing_operation.set(next(iter(processing_options.keys())))
    opt_processing_operation = tk.OptionMenu(tab3, var_processing_operation, *processing_options.keys())
    opt_processing_operation.pack(side=tk.LEFT, padx=10, pady=10)

    lbl_processing_explanation = tk.Label(tab3, text=processing_options[var_processing_operation.get()], wraplength=250, justify=tk.LEFT)
    lbl_processing_explanation.pack(side=tk.LEFT, padx=10, pady=10)

    def on_processing_option_change(*args):
        operation_key = var_processing_operation.get()
        lbl_processing_explanation.config(text=processing_options[operation_key])

    var_processing_operation.trace('w', on_processing_option_change)

# start the GUI
    root.mainloop()

if __name__ == '__main__':
    gui_main()
