import random
from io import BytesIO
import pandas as pd
# from StringIO import StringIO  # python 2.7x

from flask import Flask, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


app = Flask(__name__)

@app.route('/plot.png')
def plot():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    dt=pd.read_excel('C:/Users/goz544/Desktop/DQA_2/DQA/static/Commercial_source_090716.xls')
    xs=dt.groupby('PortfolioName').size().order(ascending=False)
    
    # xs = range(100)
    # ys = [random.randint(1, 50) for x in xs]
    # dt['Maturity_Date']=dt['Maturity_Date'].apply(lambda x: pin_date(x))
    # dt['Maturity_Date']=pd.to_datetime(dt['Maturity_Date'])
    # plot1=dt['Maturity_Date'].value_counts()
    # xs=plot
    # ys=dt['Maturity_Date']
    # axis.plot(xs,kind='pie')
    axis.plot(xs)
    # axis.plot(xs,ys)
    canvas = FigureCanvas(fig)
    output = BytesIO()
    # output = StringIO()  # python 2.7x
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


if __name__ == '__main__':
    app.run(debug=True)
