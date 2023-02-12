import subprocess
import sys
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods= ["GET", "POST"])
def index():
   return render_template('index.html')

@app.route('/my_link', methods = ["GET", "POST"])
def my_link():
  singer= request.form.get('sname')
  noofvideos= request.form.get('video')
  duration= request.form.get('duration')
  email= request.form.get('mail')

  #sys.argv= ['102017070_form.py', data , weights, impacts, email]
  s2_out= subprocess.check_output([sys.executable, "102017070_form.py", singer , noofvideos, duration, email])

  #print(s2_out)
  return s2_out

if __name__ == '__main__':
  app.run(debug=True)