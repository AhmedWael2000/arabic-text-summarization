from flask import Flask, jsonify,render_template,request,redirect,url_for, flash
from datetime import datetime
from sqlalchemy import Column, DateTime, func,Float,desc
from dotenv import load_dotenv
import pypyodbc as odbc
import os
import pandas as pd
import numpy as np
import re
import models
from sentimentAnalysis import sentiment


# import urllib3 as urllib
# params = urllib.parse.quote_plus(os.environ["CONNECTION_STRING"])
# app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
load_dotenv('.env')
domain_= os.getenv('DOMAIN')
username_= os.getenv('DBUSERNAME')
password_= os.getenv('MYPASSWORD')
database_= os.getenv('MYDATABASE')
# connection_string= os.getenv('CONNECTION_STRING')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username_}:{password_}@{domain_}/{database_}'

# conn= odbc.connect(connection_string)
# server= os.getenv('server')
# database= os.getenv('database')
# user= os.getenv('user')
# password= os.getenv('password')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://your_username:your_password@your_server.database.windows.net/your_database'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://{user}:{password}@{server}.database.windows.net/{database}?driver=ODBC+Driver+18+for+SQL+Server'

app.app_context().push()
db = SQLAlchemy(app)

class Complaints(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(80))
    national_id=db.Column(db.String(14))
    governorate= db.Column(db.String(80))
    phone=db.Column(db.String(80))
    Complaint=db.Column(db.String(1000),  nullable=False)
    summary=db.Column(db.String(1000))
    complaint_time=db.Column(db.DateTime,default=func.now())
    email= db.Column(db.String(120))
    file= db.Column(db.String(80),  nullable=True)
    tfidf = db.Column(db.Integer)
    positive = db.Column(db.Float)
    neutral = db.Column(db.Float)
    negative = db.Column(db.Float)
    sentiment_type = db.Column(db.Integer)
    def __repr__(self):
        return f'<Complaint {self.id}>'




@app.route('/',methods=['GET','POST'])
def index():
   if request.method =='GET':
        return render_template('index.html')
   else:
       name=request.form["fullname"]
       email=request.form["email"]
       phone= request.form["phone"]
       feedback=request.form["feedback"]
       gov=request.form["gov"]
       national_id= request.form["nationalID"]
       result = models.make_a_classification(feedback)
       tfidf=3
       if len(result)==1 and result in ['0','1','2']:
             tfidf=int(result)
       positive,neutral,negative,sentiment_type= sentiment(feedback)
       new_complaint = Complaints(  name=name,
                                    national_id=national_id,
                                    governorate=gov,
                                    phone=phone,
                                    Complaint=feedback,
                                    email=email,
                                    tfidf=tfidf,
                                    positive=positive,
                                    neutral=neutral,
                                    negative=negative,
                                    sentiment_type=sentiment_type)
       try:
        db.session.add(new_complaint)
        db.session.commit()
        return render_template('success.html')
       except:
           return "something went wrong in database"



@app.route('/transports',methods=['GET'])
def transports():
   quaries= Complaints.query.filter(Complaints.tfidf==0).order_by(desc(Complaints.negative)).all()
   print('*'*100,request.url)

   return render_template('transports.html',quaries=quaries,name="شكاوى وزارة النقل",title="وزارة النقل")

@app.route('/health',methods=['GET'])
def health():
   quaries= Complaints.query.filter(Complaints.tfidf==1).order_by(desc(Complaints.negative)).all()
   return render_template('transports.html',quaries=quaries,name="شكاوى وزارة الصحه",title="وزارة الصحه")

@app.route('/waterandelec',methods=['GET'])
def waterandelec():
   quaries= Complaints.query.filter(Complaints.tfidf==2).order_by(desc(Complaints.negative)).all()
   return render_template('transports.html',quaries=quaries,name="شكاوى وزارة الكهرباء و الماء",title="وزارة الكهرباء و الماء")

@app.route('/not_classified',methods=['GET'])
def not_classified():
   quaries= Complaints.query.filter(Complaints.tfidf==3).order_by(desc(Complaints.negative)).all()
   return render_template('transports.html',quaries=quaries,name="شكاوى غير مصنفه",title="غير مصنفه")
 
@app.route('/stat', methods=['GET'])
def stat():
    return render_template('stat.html', title="احصائيات")
  
@app.route('/delete/<int:id>')
def delete_handler(id):
    complaint = Complaints.query.get_or_404(id)
    try:
        db.session.delete(complaint)
        db.session.commit()
        previous_url = request.referrer
        
        return redirect(previous_url)
    except:
        return "something went wrong while deleting"
   
@app.route('/view/<int:id>')
def view_handler(id):
    complaint = Complaints.query.get_or_404(id)
    return render_template('view_complaint.html',complaint=complaint)

@app.route('/uedit_misclassification/<int:id>', methods=['POST'])
def edit_misclassification(id):
    complaint = Complaints.query.get_or_404(id)
    edit_classification = request.form['new_value']
    complaint.tfidf = int(edit_classification)
    db.session.commit()
    return redirect(url_for('view_handler', id=id))

@app.route('/sentiment-data',methods=['GET'])
def sentiment_data():
    textClasses=['Transports','Health','Electricity and water',"others"]
    sentimentClasses=['Positive','Neutral','Negative']
    query = db.session.query(Complaints.tfidf, Complaints.sentiment_type, func.count(Complaints.sentiment_type)).group_by(Complaints.tfidf, Complaints.sentiment_type)
    processed = {}
    for tfidf,sentiment_type, count in query:
        if textClasses[tfidf] not in processed:
            processed[textClasses[tfidf]] = {}
        processed[textClasses[tfidf]][sentimentClasses[sentiment_type]] = count

    return jsonify(processed)

@app.route('/count-data', methods=['GET'])
def count_data():
    counts = db.session.query(Complaints.tfidf, db.func.count()).group_by(Complaints.tfidf).all()
    data = [0, 0, 0, 0]
    for value, count in counts:
        if value in [0, 1, 2, 3]:
            data[value] = count
    labels = ['وزارة النقل', 'وزارة الصحه','وزارة الكهرباء و الماء',  'غير مصنفه']
    
    chart_data = {
        'labels': labels,
        'data': data,
    }
    
    return jsonify(chart_data)


@app.route('/summarize/<int:id>', methods=['POST'])
def summarize(id):
    complaint = Complaints.query.get_or_404(id)
    if complaint.summary ==None:
        complaint.summary = models.make_a_summary(complaint.Complaint)
        db.session.commit()

          
    return jsonify({'summary': complaint.summary})

if __name__ == "__main__":
    

    app.run(host='0.0.0.0',debug=True)
