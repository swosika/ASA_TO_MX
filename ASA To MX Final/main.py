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
      json_object_dump = json.dumps(result, indent = 4) 
      json_object = json.loads(json_object_dump)
      ORG_ID = (json_object["Organization ID"])
      API_KEY = (json_object["API Key"])
      FNAME = (json_object["Converting From"])
      print (ORG_ID,API_KEY,FNAME)

      return render_template("result.html",result = result)


if __name__ == '__main__':
   app.run(debug = True)
