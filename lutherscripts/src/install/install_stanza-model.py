import stanza

__author__ = "benjamsf"
__license__ = "MIT"

def download_stanza_model():
    print("Downloading Stanza model for Latin...")
    stanza.download('la')
    print("Stanza model downloaded successfully.")

if __name__ == "__main__":
    download_stanza_model()
