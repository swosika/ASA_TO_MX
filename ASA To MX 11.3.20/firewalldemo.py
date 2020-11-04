import asaparser as ap
import meraki_messenger as mm
from flask import Flask, render_template, request
import json 
import os 
import time

start_time = time.time()

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'uploads'

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      ORG_ID = request.form['Organization ID']
      API_KEY = request.form['API Key']
      uploaded_file = request.files['Converting From']
      if uploaded_file.filename != '':
         uploaded_file.save(uploaded_file.filename)
      FNAME = uploaded_file.filename
      print(FNAME)
      # uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], uploaded_file))
      object_groups = ap.gather_data(FNAME)
      #print (ORG_ID, API_KEY, "ME")
      #mm.me(API_KEY,ORG_ID)
      mm.delete_all_network_groups(API_KEY,ORG_ID)
      mm.delete_all_network_objects(API_KEY,ORG_ID)
      #uncomment below to run the create groups
      mm.create_network_groups(object_groups,ORG_ID,API_KEY)
      end_time = time.time()
      print(round(end_time - start_time, 2))
   return render_template('result.html',result = result)

if __name__ == '__main__':
   app.run(debug = True)


   


