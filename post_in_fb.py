from flask import Flask,render_template,url_for,request
import pandas as pd 
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import facebook
#from sklearn.externals import joblib


app = Flask(__name__)

@app.route('/text')
def home():
	return render_template('homesus.html')

@app.route('/predict',methods=['POST'])
def predict():
    df=pd.read_csv("Dataset_SE_Bangla.csv")
    X=df['Text']
    cv=TfidfVectorizer()
    X=cv.fit_transform(X)
    if request.method=='POST':
        message=request.form['message']
        data=['message']
        vect=cv.transform(data).toarray()
        infile=open('suspicious_model','rb')
        model=joblib.load(infile)
        _prediction=int(model.predict(vect))

        page_access_token = 'EAAJBlNIzKkQBAJfkNomm69xK93o5QGUVrqSkSqfXIKCUfrKZCRFZBoU0GnLEALm9lARUzIpQ6GguNoGy8xg5kR8NvRJtwLTwimn3EZCWkHPVhyHjBQqkVnCVRCDwGF1LXyfKpcZCKaZBwZCJAWpbsVzDoxSaF2ZCDKuvYzhLg2v9z9iBcUtrvqnq6AZA2xO6zJQeF6XDybTCD88F5u4vwV0oSuQ9osIBFcMZD'
        graph = facebook.GraphAPI(page_access_token)
        facebook_page_id = '101432762410121'
        graph.put_object(facebook_page_id, "feed", message=message)
        return render_template('homesus.html',message=message,prediction=_prediction)
if __name__ == '__main__':
	app.run(debug=True)