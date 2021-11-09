import pandas as pd

df = pd.read_csv("Pegasus_activity.csv")

final_list = []

for i in range(0,len(df)):
    print ("ITEration -- ",i)
    temp_list = []
    temp_list = (df.iloc[i]).tolist()
    print(temp_list)
    print ("-------")
    temp_list = list(set(temp_list))
    print (temp_list)
    final_list = final_list + temp_list

final_list = list(set(final_list))

with open("Activity_final.txt", 'w') as output:
    for row in final_list:
        output.write(str(row) + '\n')