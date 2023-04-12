input_file = "stopwords.txt"
output_file = "extrastopwords.py"

stopwords = []

# Read the stopword file and add each stopword to the list
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        stopwords.append(line.strip())

# Write the stopword list to the output file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("extrastopwords_lat = [\n")
    for word in stopwords:
        f.write(f"    '{word}',\n")
    f.write("]\n")

