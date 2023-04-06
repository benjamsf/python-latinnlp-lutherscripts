# Python script to prepare Luther's Werke im WWW text to form usable in NLP
# Stage 2, tokenize prepared text
# (c) Benjam Bröijer, licensed under the MIT License

from cltk.core.data_types import Doc, Word
from cltk.tokenizers.lat import LatinTokenizationPipeline
from cltk.languages.example_texts import get_example_text

# Download Latin models
from cltk.languages.utils import get_lang
from cltk.nlp import NLP

# Load the Latin models
lang = get_lang("lat")
nlp = NLP(language=lang)
