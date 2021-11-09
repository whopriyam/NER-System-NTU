import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from simpletransformers.ner import NERModel,NERArgs

data = pd.read_csv("symptoms_ner.csv")

data =data.fillna(method ="ffill")
data["Sentence_Num"] = LabelEncoder().fit_transform(data["Sentence_Num"])

data.rename(columns={"Sentence_Num":"sentence_id","Word":"words","Tag":"labels"}, inplace =True)
data["labels"] = data["labels"].str.upper()

X= data[["sentence_id","words"]]
Y =data["labels"]

x_train, x_test, y_train, y_test = train_test_split(X,Y, test_size =0.2)

#building up train data and test data
train_data = pd.DataFrame({"sentence_id":x_train["sentence_id"],"words":x_train["words"],"labels":y_train})
test_data = pd.DataFrame({"sentence_id":x_test["sentence_id"],"words":x_test["words"],"labels":y_test})

label = data["labels"].unique().tolist()


args = NERArgs()
args.num_train_epochs = 3
args.learning_rate = 1e-4
args.overwrite_output_dir =True
args.train_batch_size = 32
args.eval_batch_size = 32

#Use the model you want by un-commenting that line

# model = NERModel('bert', 'bert-base-uncased',labels=label,args =args)
# model = NERModel('xlnet', 'xlnet-base-cased',labels=label,args =args)
# model = NERModel('roberta', 'roberta-base',labels=label,args =args)
# model = NERModel('distilbert', 'distilbert-base-uncased',labels=label,args =args)
model = NERModel('albert', 'albert-base-v1',labels=label,args =args)
# model = NERModel('electra', 'google/electra-small-discriminator',labels=label,args =args)

model.train_model(train_data,eval_data = test_data,acc=accuracy_score)

result, model_outputs, preds_list = model.eval_model(test_data)

prediction1, model_output1 = model.predict(["I have come down with cold and fatigue since yesterday after meeting Jung Shen"])
prediction2, model_output2 = model.predict(["I have come down with pneumonia and fatigue since yesterday after meeting Jung Shen"])
prediction3, model_output3 = model.predict(["I have come down with building and fatigue since yesterday after meeting Jung Shen"])
prediction4, model_output4 = model.predict(["I have come down with building and food since yesterday after meeting Jung Shen"])

print (prediction1)
print (prediction2)
print (prediction3)
print (prediction4)\
