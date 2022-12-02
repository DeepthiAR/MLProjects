from flask import render_template, Flask, request
import pandas as pd
from models.model import Recommendation

recommend = Recommendation()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def home():
    flag = False 
    data = ""
    user = ""
    if not "clear" in request.form:
        if request.method == 'POST':
            user = request.form["userid"]
            if(user):
                flag = True
                data=recommend.getTopProducts(user.lower())
    return render_template('index.html', data=data, flag=flag, userid=user)


if __name__ == '__main__':
    app.run(debug=True)
