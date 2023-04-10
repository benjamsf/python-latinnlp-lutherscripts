import asyncio
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import sys
import subprocess
import pkg_resources
from pathlib import Path
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
import asyncio
import time


__author__ = "benjamsf"
__license__ = "MIT"

stop_flag = [False]

class CustomTextRedirector:
    def __init__(self, widget):
        self.widget = widget
        self.widget.configure(background='black', foreground='green')  # Set background and text color
        self.encoding = 'utf-8'  # Set the encoding for the widget

    def write(self, message):
        self.widget.configure(state='normal')
        self.widget.insert(tk.END, message.encode(self.encoding))  # Encode the message with the specified encoding
        self.widget.see(tk.END)
        self.widget.configure(state='disabled')
        self.widget.update()

    def flush(self):
        pass

    def readline(self):
        return ''

def create_image_label(parent, root, frames):
    lbl_luther_image = tk.Label(parent, image=frames[0])
    lbl_luther_image.grid(row=0, rowspan=8, column=0, padx=10, pady=10)

    return lbl_luther_image


def gui_main():

    root = tk.Tk()
    root.geometry("1500x640")
    root.title("Lutherscripts (Dev version) - A NLP toolset for Latin language")

    txt_terminal = tk.Text(root, height=20, width=1000)

    gif1 = tk.PhotoImage(file=pkg_resources.resource_filename(__name__, "luther0.gif"))
    gif2 = tk.PhotoImage(file=pkg_resources.resource_filename(__name__, "luther1.gif"))
    gif3 = tk.PhotoImage(file=pkg_resources.resource_filename(__name__, "luther2.gif"))


    lbl_luther_image = tk.Label(root, image=gif1)
    lbl_luther_image.grid(row=0, rowspan=8, column=0, padx=10, pady=10)
    
    frames = [gif1, gif2, gif3]
    interval = 0.5  # in seconds



    logging.basicConfig(level=logging.INFO)

    # Choose raw source text ROW 0
    lbl_raw_sourcetext = tk.Label(root, text="Choose the Primary Source:")
    lbl_raw_sourcetext.grid(row=0, column=1, padx=10, pady=10)
    btn_raw_sourcetext = tk.Button(root, text="Browse...", command=lambda: choose_file())
    btn_raw_sourcetext.grid(row=0, column=2, padx=10, pady=10)

    file_label = tk.StringVar()
    file_label.set("No file selected")
    lbl_selected_file = tk.Label(root, textvariable=file_label)
    lbl_selected_file.grid(row=0, column=3, padx=10, pady=10)

    # Choose dictionary file ROW 1
    lbl_dictionarysourcetext = tk.Label(root, text="Choose the Dictionary Source, if applicable:")
    lbl_dictionarysourcetext.grid(row=1, column=1, padx=10, pady=10)
    lbl_dictionarysourcetext = tk.Button(root, text="Browse...", command=lambda: choose_dictionary_file())
    lbl_dictionarysourcetext.grid(row=1, column=2, padx=10, pady=10)

    dictionarysourcefile_label = tk.StringVar()
    dictionarysourcefile_label.set("No file selected")
    lbl_dictionarysourceselected_file = tk.Label(root, textvariable=dictionarysourcefile_label)
    lbl_dictionarysourceselected_file.grid(row=1, column=3, padx=10, pady=10)

    # Choose output file location ROW 2
    lbl_output_file = tk.Label(root, text="Choose the Output File location:")
    lbl_output_file.grid(row=2, column=1, padx=10, pady=10)
    btn_output_file = tk.Button(root, text="Browse...", command=lambda: choose_output_file())
    btn_output_file.grid(row=2, column=2, padx=10, pady=10)

    output_file_label = tk.StringVar()
    output_file_label.set("No file selected")
    lbl_selected_output_file = tk.Label(root, textvariable=output_file_label)
    lbl_selected_output_file.grid(row=2, column=3, padx=10, pady=10)

    # Entry field for argument 1&2 ROW 3
    lbl_argument1 = tk.Label(root, text="Argument 1 and 2:")
    lbl_argument1.grid(row=3, column=1, padx=4, pady=4)
    ent_argument1 = tk.Entry(root, width=10)
    ent_argument1.grid(row=3, column=2, padx=4, pady=4)
    ent_argument2 = tk.Entry(root, width=10)
    ent_argument2.grid(row=3, column=3, padx=4, pady=4)


    # Choose Operation
    lbl_operation = tk.Label(root, text="Choose Operation:")
    lbl_operation.grid(row=4, column=1, padx=10, pady=10)

    options = [
        ("word_tokenize_latin", "Tokenize Latin text by words"),        
        ("sent_tokenize_latin", "Tokenize Latin text by sentences"),        
        ("kwic_analysis", "Perform KWIC analysis from your JSON word tokenized text"),
        ("freq_analysis", "Perform word frequency analysis from your JSON word tokenized text"),    
        ("build_corpus", "Build a dictionary and corpus from your JSON word tokenized text"),
        ("topic_modeling", "Perform Topic Modeling from your dictionary and corpus")
        ]

    def update_explanation(*args):
        explanations = {
            "Tokenize Latin text by words": "This operation will tokenize your Latin text by words, which is required for further word-based natural language processing, using CLTK.",
            "Tokenize Latin text by sentences": "This operation will tokenize your Latin text by sentences, which is useful for sentence-based natural language processing, using CLTK.",
            "Perform KWIC analysis from your JSON word tokenized text": "This operation will perform a Key Word in Context (KWIC) analysis, allowing you to see the occurrences of a word within the context of the text, using NLTK. Source must be a Word Tokenized text in JSON format.",
            "Perform word frequency analysis": "This operation will perform a Word Frequency Analysis, allowing you to see the number of times each word has been used in your target text, using NLTK. Source must be a Word Tokenized text in JSON format.",
            "Build a dictionary and corpus from your JSON word tokenized text": "This operation will build a dictionary and a corpus from your Word Tokenized text in JSON format using GenSim, for to source further operations.",
            "Perform Topic Modeling from your dictionary and corpus": "This operation will perform Topic Modeling using GenSim from your dictionary and corpus files. As Argument 1, pass the number of topics you want to try dig out from the text. As Argument 2, pass the number of passes to perform on the corpus."
        }

        selected_operation = var_operation.get()
        explanation = explanations.get(selected_operation, "No explanation available.")
        explanation_label.set(explanation)

    var_operation = tk.StringVar(root)
    var_operation.set(options[0][1])
    var_operation.trace("w", update_explanation)
    opt_operation = tk.OptionMenu(root, var_operation, *[option[1] for option in options])
    opt_operation.grid(row=4, column=2, padx=10, pady=10)

    explanation_label = tk.StringVar()
    explanation_label.set("This operation will tokenize your Latin text by words, which is required for further word-based natural language processing.")
    lbl_explanation = tk.Label(root, textvariable=explanation_label, wraplength=300)
    lbl_explanation.grid(row=4, column=3, padx=10, pady=10)

    # function to choose file and store the location in a variable
    def choose_file():
        global location_raw_sourcetext
        location_raw_sourcetext = filedialog.askopenfilename(title="Select a File", initialdir=os.path.dirname(os.path.abspath(__file__)))
        file_label.set(location_raw_sourcetext)
        print(f"File selected: {location_raw_sourcetext}")

    def choose_dictionary_file():
        global location_dictionary_file
        location_dictionary_file = filedialog.askopenfilename(title="Select a File", initialdir=os.path.dirname(os.path.abspath(__file__)))
        lbl_dictionarysourcetext.set(location_dictionary_file)
        print(f"File selected: {location_dictionary_file}")

    # function to choose output file and store the location in a variable
    def choose_output_file():
        global location_output
        location_output = filedialog.asksaveasfilename(title="Select output file location", defaultextension=".json", initialdir=os.path.dirname(os.path.abspath(__file__)))
        output_file_label.set(location_output)
        print(f"Output file selected: {location_output}")

    txt_terminal = tk.Text(root, height=20, width=1000)
    txt_terminal.configure(state='normal')  # Add this line to enable the state of the txt_terminal widget
    txt_terminal.grid(row=7, column=1, columnspan=3, padx=10, pady=10, sticky='nsew')
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(5, weight=1)
    sys.stdout = CustomTextRedirector(txt_terminal)
    sys.stderr = CustomTextRedirector(txt_terminal)
    

    #def run_script():
    #    global location_raw_sourcetext, location_output
    #    operation_name = [option[0] for option in options if option[1] == var_operation.get()][0]
    #    source_path = os.path.normpath(location_raw_sourcetext)
    #    destination_path = os.path.normpath(location_output)
    #    cli_command = ['lutherscripts-cli', '-o', operation_name, '-s', source_path, '-d', destination_path]

        # Run the run_script_async coroutine using the default event loop
     #   loop = asyncio.get_event_loop()
      #  loop.run_until_complete(run_script_async(cli_command))
    
    def update_image_label(lbl, frames):
        frame = frames.pop(0)
        frames.append(frame)
        lbl.config(image=frame)


    async def run_script_async():
        operation_name = [option[0] for option in options if option[1] == var_operation.get()][0]
        source_path = os.path.normpath(location_raw_sourcetext)
        destination_path = os.path.normpath(location_output)
        cli_command = ['lutherscripts-cli', '-o', operation_name, '-s', source_path, '-d', destination_path]
        # Add argument 1 and argument 2 for KWIC analysis
        if operation_name == "kwic_analysis":
            argument1 = ent_argument1.get()
            argument2 = ent_argument2.get()
            cli_command.extend(["-1", argument1, "-2", argument2])
        if operation_name == "topic_modeling":
            dictionary_path = os.path.normpath(location_dictionary_file)
            argument1 = ent_argument1.get()
            argument2 = ent_argument2.get()
            cli_command.extend(["-1", argument1, "-2", argument2, "-dc", dictionary_path])

        process = await asyncio.create_subprocess_exec(
            *cli_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        lbl_luther_image.config(image=gif1)
    
        output = ''
        while True:
            char = await process.stdout.read(1)
            if not char:
                break
            char = char.decode(errors='replace')

            if char == '\r':
                txt_terminal.configure(state='normal')
                txt_terminal.delete(f'{tk.END} -2c linestart', tk.END)
                txt_terminal.insert(tk.END, output)
                txt_terminal.see(tk.END)
                txt_terminal.configure(state='disabled')
                txt_terminal.update()
                output = ''
            else:
                output += char

        stderr_data = await process.stderr.read()
        if stderr_data:
            txt_terminal.configure(state='normal')
            txt_terminal.insert(tk.END, stderr_data.decode())
            txt_terminal.see(tk.END)
            txt_terminal.configure(state='disabled')
            txt_terminal.update()

    def animate_luther(stop_flag):
        while not stop_flag[0]:
            update_image_label(lbl_luther_image, frames)
            root.update()
            time.sleep(interval)


    def start_operation():
        # Check the selected operation and validate arguments for KWIC analysis
        operation_name = [option[0] for option in options if option[1] == var_operation.get()][0]
        if operation_name == "kwic_analysis":
            argument1 = ent_argument1.get()
            argument2 = ent_argument2.get()
            if not argument1 or not argument2:
                print("Please enter both Argument1 (Keyword) and argument2 (Context length, a number of words you want to see left and right of a keyword hit) for the KWIC analysis")
                return
        if operation_name == "topic_modeling":
            argument1 = ent_argument1.get()
            argument2 = ent_argument2.get()
            if not argument1 or not argument2:
                print("Please enter both Argument1 (Number of Topics) and argument2 (Number of Corpus Passes during LDA Training) ")
                return

        # Start the animation thread
        stop_flag[0] = False
        animation_thread = threading.Thread(target=animate_luther, args=(stop_flag,))
        animation_thread.daemon = True
        animation_thread.start()

        print("Starting operation...")
        print("Please wait, this might take couple of seconds...")

        btn_play.configure(state='disabled')

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Call the main function with the callback function
        loop.run_until_complete(run_script_async())
        loop.close()
        btn_play.configure(state='normal')
        stop_flag[0] = True
        
    # Start Operation! button
    btn_play = tk.Button(root, text="Start Operation!", command=start_operation)
    btn_play.grid(row=6, column=3, padx=10, pady=10)

    # Print a welcome message to the terminal
    print("Welcome to Lutherscripts!")
    print("Development version")

    # Print a message before redirecting stdout and stderr
    print("Starting GUI...")

    sys.stdout = CustomTextRedirector(txt_terminal)
    sys.stderr = CustomTextRedirector(txt_terminal)

    # Start the GUI
    root.mainloop()


if __name__ == '__main__':
    gui_main()





       

