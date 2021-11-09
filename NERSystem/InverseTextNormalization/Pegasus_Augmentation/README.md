#Installing dependencies

pip install sentence-splitter
pip install transformers
pip install SentencePiece
pip install num2words

## Run these commands to perform text augmentation
1) Once you generate the covid_cleaned.txt file, run the Pegasus_covid.py file on it and get the augmented csv file.

2) Run the remove_duplicates.py file to remove duplicate augmentations and get the final output.