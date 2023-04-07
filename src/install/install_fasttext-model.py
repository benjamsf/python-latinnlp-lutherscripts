import os
import urllib.request

def download_fasttext_model():
    print("Downloading Fasttext model for Latin...")

    model_url = "https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.la.vec"
    cltk_data_dir = os.path.join(os.path.expanduser("~"), "cltk_data", "lat", "embeddings", "fasttext")
    os.makedirs(cltk_data_dir, exist_ok=True)
    model_file_path = os.path.join(cltk_data_dir, "wiki.la.vec")

    urllib.request.urlretrieve(model_url, model_file_path)

    print("Fasttext model downloaded successfully.")

if __name__ == "__main__":
    download_fasttext_model()
