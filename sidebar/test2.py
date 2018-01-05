import pygal
import pandas as pd
from flask import Flask,render_template,flash, redirect,url_for,redirect, request, Response, send_from_directory, jsonify
from pygal.style import LightStyle

import json # Used to load and parse json data

app = Flask(__name__)

@app.route('/pygalexample/')
def pygalexample():
		# Open data.json and convert string input to floating point numbers for pygal.
		dt=pd.read_excel('C:/Users/goz544/Desktop/DQA_2/DQA/static/Commercial_source_090716.xls')
		dt1=dt.groupby('PortfolioName')['Outstanding'].sum().order(ascending=False)
		dt2=dt1.to_dict()
		# dt = dt.sort('Outstanding',ascending=False)[:2]
		chart_type = pygal.Bar(style=LightStyle, width=800, height=600,legend_at_bottom=True,
		human_readable=True,title='MN Capital Budget - 2014')
		chart_type.title = "Portfolio counts (in %)" # Give the graph a title
		for k,v in dt2.items():
			chart_type.add(k,v)
		graph_data = chart_type.render_data_uri()
		return render_template("graphing.html", graph_data = graph_data)



if __name__ == '__main__':
    app.run(debug=True)
