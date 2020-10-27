import asaparser as ap
import meraki_messenger as mm
from flask import Flask, render_template, request
import json 

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      ORG_ID = request.form['Organization ID']
      API_KEY = request.form['API Key']
      #FNAME = request.form['Converting From']
      #print (ORG_ID, API_KEY, "ME")
      #mm.me(API_KEY,ORG_ID)
      mm.delete_all_network_groups(API_KEY,ORG_ID)
      mm.delete_all_network_objects(API_KEY,ORG_ID)
   return render_template('result.html',result = result)

if __name__ == '__main__':
   app.run(debug = True)

