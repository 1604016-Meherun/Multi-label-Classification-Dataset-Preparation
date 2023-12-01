#import libraries
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import warnings
import pickle
warnings.filterwarnings("ignore")
#import dataset
#from google.colab import files
#uploaded=files.upload()
# Read The CSV File
data=pd.read_csv('Dataset_SE_Bangla.csv')
print(data.head(15))
data['Category'].value_counts()
data.drop_duplicates(inplace=True)
data['Category'].value_counts()
data.isnull().sum()   #Category and Text e kono null value nai.
#data.head(15)
# print some unprocessed reviews
#sample_data = [0,3,9,14]
#for i in sample_data:
#      print(data.Text[i],'\n','Category:-- ',data.Category[i],'\n')
# Data cleaning function
import re
def process_comments(Comment): 
    Comment = re.sub('[^\u0980-\u09FF]',' ',str(Comment)) #removing unnecessary punctuation
    return Comment
# Apply the function into the dataframe
data['cleaned'] = data['Text'].apply(process_comments)  

# print some cleaned reviews from the dataset
#sample_data = [0,3,9,14]
#for i in sample_data:
#     print('Original:\n',data.Text[i],'\nCleaned:\n',
#           data.cleaned[i],'\n','Category:-- ',data.Category[i],'\n')
input_feature=data.Text.values
output=data.Category.values
#print(input_feature)
#print(output)
# split the dataset into training and test set
input_feature_train,input_feature_test,output_train,output_test=train_test_split(input_feature,output,test_size=0.2,random_state=42)
feature_extract=TfidfVectorizer()
x_train=feature_extract.fit_transform(input_feature_train)
x_train.toarray()
# train the model by training dataset
from sklearn.naive_bayes import MultinomialNB
model=MultinomialNB()
model.fit(x_train,output_train)
x_test=feature_extract.transform(input_feature_test)
x_test.toarray()
#output_test
# predict the test set results
output_pred=model.predict(x_test)
print(output_pred)
# evaluate the model
from sklearn.metrics import r2_score
print(r2_score(output_test,output_pred))
text=['তোদের মতো কুত্তার বাচ্চারা সোনিকার মতো মেয়েরা পাইলে শিওর গ্যাংব্যাং দিবি','আমি ভালো আছি']
feature_extract_text=feature_extract.transform(text)
print(model.predict(feature_extract_text))
pickle.dump(model,open('model.pkl','wb'))
model=pickle.load(open('model.pkl','rb'))