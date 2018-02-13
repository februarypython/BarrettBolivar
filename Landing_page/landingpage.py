from flask import Flask, render_template, request, redirect
app = Flask(__name__)
# our index route will handle rendering our form
@app.route('/')
def index():
  return render_template("index.html")

@app.route('/ninja')
def ninja():
   return render_template("ninjas.html")

@app.route('/dojos/new')
def dojo_new():
   return render_template("dojos.html")

@app.route('/users', methods=['POST'])
def usercreation():
    name = request.form['name']
    email = request.form['email']
    return redirect('/')

app.run(debug=True)