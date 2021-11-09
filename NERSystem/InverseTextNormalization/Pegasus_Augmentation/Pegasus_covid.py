#Importing the PEGASUS Transformer model
import torch
import pandas as pd
import time
import num2words
import re
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
 
model_name = 'tuner007/pegasus_paraphrase'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)
 
#setting up the model
def get_response(input_text,num_return_sequences):
  batch = tokenizer.prepare_seq2seq_batch([input_text],truncation=True,padding='longest',max_length=60, return_tensors="pt").to(torch_device)
  translated = model.generate(**batch,max_length=60,num_beams=10, num_return_sequences=num_return_sequences, temperature=1.5)
  tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
  return tgt_text

def create_df(fileName):
  crimefile = open(fileName, 'r')
  text_list = [((line.split(','))[0])[:-1] for line in crimefile.readlines()]
  df = pd.DataFrame(columns=["Original_Text","T1","T2","T3","T4","T5"])
  df["Original_Text"] = text_list

  return df


df_covid = create_df("symptoms_cleaned.txt")
df_local = create_df("local_adress_cleaned.txt")
df_country = create_df("place_country_cleaned.txt")
df_activity = create_df("activity_cleaned.txt")

t1 = time.time()

for i in range(0,len(df_activity)):
  t3 = time.time()
  # sentence1 = df_covid.at[i,"Original_Text"]
  # sentence2 = df_local.at[i,"Original_Text"]
  # sentence3 = df_country.at[i,"Original_Text"]
  # sentence4 = df_activity.at[i,"Original_Text"]

  final_outputs1 = get_response(df_covid.at[i,"Original_Text"], 5)
  final_outputs2 = get_response(df_local.at[i,"Original_Text"], 5)
  final_outputs3 = get_response(df_country.at[i,"Original_Text"], 5)
  final_outputs4 = get_response(df_activity.at[i,"Original_Text"], 5)


  try:
    df_covid.at[i,"T1"] = final_outputs1[0]
    df_local.at[i,"T1"] = final_outputs2[0]
    df_country.at[i,"T1"] = final_outputs3[0]
    df_activity.at[i,"T1"] = final_outputs4[0]
  except:
    df_covid.at[i,"T1"] = ""
    df_local.at[i,"T1"] = ""
    df_country.at[i,"T1"] = ""
    df_activity.at[i,"T1"] = ""
  try:
    df_covid.at[i,"T2"] = final_outputs1[1]
    df_local.at[i,"T2"] = final_outputs2[1]
    df_country.at[i,"T2"] = final_outputs3[1]
    df_activity.at[i,"T2"] = final_outputs4[1]
  except:
    df_covid.at[i,"T2"] = ""
    df_local.at[i,"T2"] = ""
    df_country.at[i,"T2"] = ""
    df_activity.at[i,"T2"] = ""
  try:
    df_covid.at[i,"T3"] = final_outputs1[2]
    df_local.at[i,"T3"] = final_outputs2[2]
    df_country.at[i,"T3"] = final_outputs3[2]
    df_activity.at[i,"T3"] = final_outputs4[2]
  except:
    df_covid.at[i,"T3"] = ""
    df_local.at[i,"T3"] = ""
    df_country.at[i,"T3"] = ""
    df_activity.at[i,"T3"] = ""
  try:
    df_covid.at[i,"T4"] = final_outputs1[3]
    df_local.at[i,"T4"] = final_outputs2[3]
    df_country.at[i,"T4"] = final_outputs3[3]
    df_activity.at[i,"T4"] = final_outputs4[3]
  except:
    df_covid.at[i,"T4"] = ""
    df_local.at[i,"T4"] = ""
    df_country.at[i,"T4"] = ""
    df_activity.at[i,"T4"] = ""
  try:
    df_covid.at[i,"T5"] = final_outputs1[4]
    df_local.at[i,"T5"] = final_outputs2[4]
    df_country.at[i,"T5"] = final_outputs3[4]
    df_activity.at[i,"T5"] = final_outputs4[4]
  except:
    df_covid.at[i,"T5"] = ""
    df_local.at[i,"T5"] = ""
    df_country.at[i,"T5"] = ""
    df_activity.at[i,"T5"] = ""

  # df.at[i,"T2"] = final_outputs[1]
  # df.at[i,"T3"] = final_outputs[2]
  # df.at[i,"T4"] = final_outputs[3]
  # df.at[i,"T5"] = final_outputs[4]


  print ("ITERATION - ",i)
  print (time.time()-t3)

t2 = time.time()

def clean_df(df):

  columns_list = list(df.columns)

  for i in df.index:
    for column in columns_list:
      item = df.at[i,column]
      item2 = re.sub(r"(\d+)", lambda x: num2words.num2words(int(x.group(0))), str(item))
      df.at[i,column] = item2
      print ("ITERATION - ",i)

  return df

df_covid_clean = clean_df(df_covid)
df_local_clean = clean_df(df_local)
df_country_clean = clean_df(df_country)
df_activity_clean = clean_df(df_activity)

df_covid_clean.to_csv("Pegasus_symptoms.csv",index=False)
df_local_clean.to_csv("Pegasus_local.csv",index=False)
df_country_clean.to_csv("Pegasus_country.csv",index=False)
df_activity_clean.to_csv("Pegasus_activity.csv",index=False)

