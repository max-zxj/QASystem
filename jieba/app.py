from flask import Flask
from flask import render_template
from flask import request
from get_answear import get_answear

app = Flask(__name__)

@app.route('/')
def home_page():
        str1 = request.args.get('wd')
        answear = '  '
        hint = ''
        if str1 == None:
                return render_template('search.html',str1="   ",answear = answear)
        else:
                g_answear,hint = get_answear(str1)
                if len(hint) >1:
                        answear = g_answear + '\n'+'(  '+ hint + '  )'
                else:
                        answear = g_answear
                # print(str1,answear)
                return render_template('search.html',str1=str1,answear = answear)
       

app.run()