### Installing thrax compiler if not installed before
Install thrax using `conda - conda install -c conda-forge thrax`

### Run these commands to generate the sentences

1)`thraxmakedep covid.grm`

2)`make`

3)`thraxrandom-generator --far=covid.far --rule=random_sentence --noutput = 1000000 > covid_symptom.txt`

### Cleaning the file
Run `fix_txt.py` on covid_symptom.txt to to get covid_symptom_cleaned.txt file which has the cleaned sentences.
