import pandas as pd
import numpy as np
from flask import Flask,render_template,flash, redirect,url_for,redirect, request, Response, send_from_directory, jsonify
import os, time, random,datetime
import json

app = Flask(__name__)

@app.route("/bzrules")
def show_tables():
	df = pd.read_excel('static/dummy_data1.xlsx')
	df.set_index(['DR_ID'], inplace=True)
	df.index.name=None
	if request.method == 'GET':
		subarealist = df['Subject_Area'].unique().tolist()
		# Accuracy = df.loc[df.DQ_Dimension=='Accuracy']
		# Completeness = df.loc[df.DQ_Dimension=='Completeness']
		# Consistency = df.loc[df.DQ_Dimension=='Consistency']
		Commercial = df.loc[df['Subject_Area']=='Commercial']
		# Commercial = pd.reset_index()
		TradedUpstream = df.loc[df['Subject_Area']=='TradedUpstream']
		Wholesale_Bond = df.loc[df['Subject_Area']=='Wholesale_Bond']
		search_key = request.args.get('subjectarea')
		dfrows = df.loc[df['Subject_Area']==search_key]
		return render_template('indext.html',subarealist=subarealist,tables=[Commercial.to_html(classes='Commercial'), TradedUpstream.to_html(classes='TradedUpstream'),Wholesale_Bond.to_html(classes='Consistency')],titles = ['na','Commercial', 'TradedUpstream','Wholesale_Bond'])
		# return render_template('indext.html',subarealist=subarealist,tables=[Commercial.to_html(classes='Commercial',bold_rows = 'True')])


if __name__ == "__main__":
	app.run(debug=True)
