from flask import Flask, request, render_template,jsonify

app = Flask(__name__)

def do_something(text1,text2):
   text1 = text1.upper()
   text2 = text2.upper()
   output = text1
   return output

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/join', methods=['GET','POST'])
def my_form_post():
    text1 = request.form['text1']
    word = request.args.get('text1')
    text2 = request.form['text2']
    text3 = request.form['text3']
    output = do_something(text1)
    result = {
        "output": output
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)

