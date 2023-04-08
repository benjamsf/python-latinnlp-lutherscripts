import sys
from lutherscripts.gui import gui_main
from lutherscripts.cli import cli_main

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        sys.argv.pop(1)
        cli_main()
    else:
        gui_main()
