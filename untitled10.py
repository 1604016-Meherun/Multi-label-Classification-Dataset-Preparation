# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 19:10:26 2021

@author: ASUS
"""

import facebook
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask,render_template,url_for,request
token='EAAJBlNIzKkQBACQC8Y0EFKDl7CQ2tfOgMkr8yNFK36ZAlGfkebUOKjqwOF0CP1ZBWwZCxgpAZAXSF945IwTIGn1rmcZAux5Q5hb2wMQqmO8nizGaLeLIsBlO3XT76QmwBtzn43iU6wiP0vdtZB7zTd4YCtlCntdhgkLvj1cUvsZCf5FvlkDkrph6GDWZAnCqI2UZD'

def get_text_of_post():
    try:
        graph=facebook.GraphAPI(access_token=token,version=3.1)
        posts=graph.request('101432762410121/posts')['data']
        newlist=[]
        for dic in posts:
            newlist.append(dic['message'])
        return newlist
    except Exception as e:
        return 0
def get_prediction():
    newlist=get_text_of_post()
    if newlist==0:
        print("check the facebook access")
    else:
        df=pd.read_csv("dataset_SE_Bangla.csv")
        X=df["Text"]
        cv=TfidfVectorizer()
        X=cv.fit_transform(X)
        #predict_from_file with joblib
        #joblib.dump(clf, 'suspicious_model')
        d={}
        infile = open('suspicious_model','rb')
        model = joblib.load(infile)
        for i in range(0,len(newlist)):
            li=[]
            data=[newlist[i]]
            li.append(newlist[i])
            vecct=cv.transform(data).toarray()
            
            _prediction = int(model.predict(vecct))
            print('Prediction by Joblib: ',_prediction,"string is: ",newlist[i])
            li.append(_prediction)
            print(li)
            d[i]=li
        print(d)
        print("This is:",d[0][0])
if __name__=='__main__':
    get_prediction()