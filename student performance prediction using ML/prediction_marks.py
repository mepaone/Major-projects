import numpy as np
import pandas as pd 
import joblib
from math import *
from flask import render_template , request , Flask

def marks(n,m,x):
    result = (((n)/(m)) * 100)
    if x>=result:
        return x-result
    return x-result


app = Flask(__name__)

model = joblib.load('Student_Marks_Prediction_Model.pkl')
df = pd.DataFrame()


@app.route('/')
def index():
    return render_template('Marks.html')


@app.route('/predict',methods=['GET','POST'])
def predict():
    if (request.method) =='POST':
        global df
        data1 = []
        data = request.form.get('mark')
        my_marks = int(request.form.get('my_marks'))
        tot_marks = int(request.form.get('tot_marks'))
        # result=(((my_marks)/(tot_marks))*100)
        y=""
        # print(x)

        print(f"Data = {data}")
        # data = int(data)

        if int(data) >= 1 and int(data) <=24:

            data1.append(int(data))

            features = np.array(data1)
            output = model.predict( [features] )[0][0].round(2)
            #----------------------------------------------------------------------------------------------------------------------
            x = marks(my_marks, tot_marks, int(output))
            if x!=0 and x>0:
                y = "There might be chance of increase of {}% of marks".format(x)
            else:
                if x==0:
                    y = "There might There might be No chance in marks"
                else:
                    y = "There might be chance of decrease of {}% from previous state".format(abs(x))
            #------------------------------------------------------------------------------------------------------------------------
            if output <= 100:

                df = pd.concat( [df , pd.DataFrame( {'Study Hours' : data , 'Predicted Marks ' : [output]} )] ,ignore_index=True )
                print(df)
                df.to_csv('Predicted_data.csv')

                return render_template('Marks.html',predict = f'If You study {data} hours then You can get {output}%', my_tot=y)
            else:
                return render_template('Marks.html',predict = f'If You study {data} hours then You can get 100% Marks')
        else:
            return render_template('Marks.html',predict = 'Please Enter hours between 1-24')



app.run(debug=True)

