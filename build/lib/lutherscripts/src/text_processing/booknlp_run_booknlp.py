from booknlp.booknlp import BookNLP

__author__ = "benjamsf"
__license__ = "MIT"

model_params={
		"pipeline":"entity,quote,supersense,event,coref", 
		"model":"big"
	}
	
booknlp=BookNLP("en", model_params)

# Define locations
script_path = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_path, '../output/dsa_en.txt')
output_directory = os.path.join(script_path, '../output/')


# File within this directory will be named ${book_id}.entities, ${book_id}.tokens, etc.
book_id="englishdsa"

booknlp.process(input_file, output_directory, book_id)