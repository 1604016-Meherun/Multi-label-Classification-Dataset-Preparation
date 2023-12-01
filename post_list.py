#this file is creating the model file and predicting
from flask import Flask,render_template,url_for,request
import pandas as pd 
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
#from sklearn.externals import joblib
app = Flask(__name__)
def predict():
    df=pd.read_csv("dataset_SE_Bangla.csv")
    X=df["Text"]
    y=df["Category"]
    cv=TfidfVectorizer()
    X=cv.fit_transform(X)
    from sklearn.model_selection import train_test_split
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.33,random_state=42)
    from sklearn.naive_bayes import MultinomialNB
    clf = MultinomialNB()
    clf.fit(X_train,y_train)
    clf.score(X_test,y_test)
    message='আমি এই পেজটি খুলেছি কিছু নতুন করে শিক্ষার আশায়'
    data=[message]
    vecct=cv.transform(data).toarray()
    my_predict=clf.predict(vecct)
    print(my_predict)
    #predict_from_file with joblib
    #joblib.dump(clf, 'suspicious_model')
    infile = open('suspicious_model','rb')
    model = joblib.load(infile)
    _prediction = int(model.predict(vecct))
    print('Prediction by Joblib: ',_prediction)

if __name__ == '__main__':
    predict()