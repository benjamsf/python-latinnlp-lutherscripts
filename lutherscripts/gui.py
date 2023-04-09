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
    lbl_luther_image.grid(row=0, rowspan=5, column=0, padx=10, pady=10)
    return lbl_luther_image


def gui_main():

    root = tk.Tk()
    root.geometry("1400x600")
    root.title("LutherScripts v0.2.0 - A NLP toolset for Latin language")

    # create widgets for Operations tab
    create_image_label(root)

    # Choose raw source text
    lbl_raw_sourcetext = tk.Label(root, text="Choose raw source text:")
    lbl_raw_sourcetext.grid(row=0, column=1, padx=10, pady=10)
    btn_raw_sourcetext = tk.Button(root, text="Browse...", command=lambda: choose_file())
    btn_raw_sourcetext.grid(row=0, column=2, padx=10, pady=10)

    file_label = tk.StringVar()
    file_label.set("No file selected")
    lbl_selected_file = tk.Label(root, textvariable=file_label)
    lbl_selected_file.grid(row=0, column=3, padx=10, pady=10)

    # Choose output file location
    lbl_output_file = tk.Label(root, text="Choose output file location:")
    lbl_output_file.grid(row=1, column=1, padx=10, pady=10)
    btn_output_file = tk.Button(root, text="Browse...", command=lambda: choose_output_file())
    btn_output_file.grid(row=1, column=2, padx=10, pady=10)

    output_file_label = tk.StringVar()
    output_file_label.set("No file selected")
    lbl_selected_output_file = tk.Label(root, textvariable=output_file_label)
    lbl_selected_output_file.grid(row=1, column=3, padx=10, pady=10)

    # Choose Operation
    lbl_operation = tk.Label(root, text="Choose Operation:")
    lbl_operation.grid(row=2, column=1, padx=10, pady=10)

    options = [
        ("word_tokenize_latin", "Tokenize Latin text by words"),
        ("sent_tokenize_latin", "Tokenize Latin text by sentences"),
        ("nltk_do_kwic", "Perform KWIC analysis"),
    ]

    var_operation = tk.StringVar(root)
    var_operation.set(options[0][1])
    opt_operation = tk.OptionMenu(root, var_operation, *[option[1] for option in options])
    opt_operation.grid(row=2, column=2, padx=10, pady=10)

    explanation_label = tk.StringVar()
    explanation_label.set("This operation will tokenize your Latin text by words, which is required for further word-based natural language processing.")
    lbl_explanation = tk.Label(root, textvariable=explanation_label, wraplength=300)
    lbl_explanation.grid(row=2, column=3, padx=10, pady=10)

    # Start Operation! button
    btn_play = tk.Button(root, text="Start Operation!", command=run_script)
    btn_play.grid(row=3, column=3, padx=10, pady=10)

    # Terminal output
    txt_terminal = tk.Text(root, height=20, width=1000)
    txt_terminal.grid(row=4, column=1, columnspan=3, padx=10, pady=10, sticky='nsew')
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(4, weight=1)

    # function to choose file and store the location in a variable
    def choose_file():
        global location_raw_sourcetext
        location_raw_sourcetext = filedialog.askopenfilename(title="Select a File", initialdir=os.path.dirname(os.path.abspath(__file__)))
        file_label.set(location_raw_sourcetext)
        print(f"File selected: {location_raw_sourcetext}")

    # function to choose output file and store the location in a variable
    def choose_output_file():
        global location_output
        location_output = filedialog.asksaveasfilename(title="Select output file location", defaultextension=".txt", initialdir=os.path.dirname(os.path.abspath(__file__)))
        output_file_label.set(location_output)
        print(f"Output file selected: {location_output}")

    def run_script():
        global location_raw_sourcetext, location_output
        operation_name = [option[0] for option in options if option[1] == var_operation.get()][0]
        source_path = os.path.normpath(location_raw_sourcetext)
        destination_path = os.path.normpath(location_output)
        cli_command = ['lutherscripts-cli', '-o', operation_name, '-s', source_path, '-d', destination_path]
        process = subprocess.Popen(cli_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        txt_terminal.delete(1.0, tk.END)
        while True:
            output = process.stdout.readline().decode('utf-8')
            if output == '' and process.poll() is not None:
                break
            txt_terminal.insert(tk.END, output)
            txt_terminal.see(tk.END)
        returncode = process.poll()

    # start the GUI
    root.mainloop()

if __name__ == '__main__':
    gui_main()

