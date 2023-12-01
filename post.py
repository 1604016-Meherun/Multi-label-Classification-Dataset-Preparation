#post list showing
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
        infile = open('suspicious_model','rb')
        model = joblib.load(infile)
        for i in range(0,len(newlist)):
            data=[newlist[i]]
            vecct=cv.transform(data).toarray()
            
            _prediction = int(model.predict(vecct))
            print('Prediction by Joblib: ',_prediction,"string is: ",newlist[i])
app = Flask(__name__)
@app.route('/post_list',methods=['GET'])
def post_table():
    # newlist=['আমাদের তথাকথিত জাগ্রত ভাইদের মধ্যে পোস্ট পড়ে তারা যা দেখছে তা না দেখা পর্যন্ত ইহুদিরা আমাদের কতটা বোকা মনে করে তাতে আমি অপমানিত','পশ্চিমা সভ্যতার ইহুদিবাদী-ইঞ্জিনিয়ার্ড ইচ্ছাকৃত ধ্বংসের উপর একটি রঙিন চিত্রিত একশো বত্রিশ পৃষ্ঠার ই-বুক বিনামূল্যে ডাউনলোডের জন্য নীচে ক্লিক করুন','বর্তমান সময়ে টিকে থাকা প্রচুর কঠিন','আমি এই পেজটি খুলেছি কিছু নতুন করে শিক্ষার আশায়']
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
    return render_template('post_list.php',newlist=d)
if __name__=='__main__':
    #get_prediction()
    app.run(debug=True)