import pandas as pd
import numpy as np
from flask import Flask,render_template,flash, redirect,url_for,redirect, request, Response, send_from_directory, jsonify
import os, time, random,datetime
import json
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import seaborn as sns
import numpy as np
import pygal
from pygal.style import LightStyle

import plotly
import plotly.plotly as py
from plotly import tools
import plotly.graph_objs as go
from plotly.graph_objs import Figure
from plotly.graph_objs import Layout
from json import encoder

def pin_date(d):
	try:
		if int(d[5:])>2050:
			return "01JAN2050"
		else:
			return '01' + d[2:]
	except:
		return d

def get_stats(group):
	return {'00.obs': group.size,
			'01.mean': group.mean(),
			'02.std': group.std(),
			'03.miss': group.isnull().mean(),
			'04.zero': (group == 0).astype(int).mean(),
			'1.min': group.min(),
			'2.p_1':group.quantile(0.01),
			'3.p_10':group.quantile(0.10),
			'4.p_25':group.quantile(0.25),
			'5.median': group.median(),
			'6.p_75': group.quantile(0.75),
			'7.p_90': group.quantile(0.90),
			'8.p_99': group.quantile(0.99),
			'9.max': group.max()
			}

def get_miss(group):
	return {'miss': group.isnull().mean()}

def get_mean(group):
	return {'mean': group.mean()}

def get_zero(group):
	return {'zero': (group == 0).astype(int).mean()}

def get_size(group):
	return {'size': group.size}

def get_value(group):
	return {'value': group.value_counts()}

def lookup(s):
	"""
	This is an extremely fast approach to datetime parsing.
	For large data, the same dates are often repeated. Rather than
	re-parse these, we store all unique dates, parse them, and
	use a lookup to convert all dates.
	"""
	dates = {date:pd.to_datetime(date) for date in s.unique()}
	return s.map(dates)






app = Flask(__name__)

@app.route("/bzrules")
def show_tables():
	rules = pd.read_excel('static/rulespresheet.xlsx')
	rules.set_index(['DR_ID'], inplace=True)
	rules.index.name=None
	if request.method == 'GET':
		subarealist = rules['Subject_Area'].unique().tolist()
		search_key = request.args.get('subjectarea')
		dfrows = rules.loc[rules['Subject_Area']==search_key]
		allfields2 = rules[['Subject_Area','Field_Name']]
		allfields1=allfields2['Field_Name'].loc[allfields2['Subject_Area']==search_key]
		allfields1=allfields1.unique()
		showHeader = 'false'
		if len(dfrows['Subject_Area']) > 0:
			showHeader = 'true'
		return render_template('plotly123.html', showHeader=showHeader,allfields1=allfields1,subarealist=subarealist,bzrules1=[dfrows.to_html()])


# @app.route("/bzrules")
# def show_tables():
# 	rules = pd.read_excel('static/dummy_data.xlsx')
# 	rules.set_index(['DR_ID'], inplace=True)
# 	rules.index.name=None
# 	if request.method == 'GET':
# 		subarealist = rules['Subject_Area'].unique().tolist()
# 		search_key = request.args.get('subjectarea')
# 		dfrows = rules.loc[rules['Subject_Area']==search_key]
# 		allfields2 = rules[['Subject_Area','Field_Name']]
# 		allfields1=allfields2['Field_Name'].loc[allfields2['Subject_Area']==search_key]
# 		allfields1=allfields1.unique()
# 		showHeader = 'false'
# 		if len(dfrows['Rule']) > 0:
# 			showHeader = 'true'
# 		return render_template('plotly123.html', showHeader=showHeader,allfields1=allfields1,subarealist=subarealist,bzrules1=[dfrows.to_html()])
#


@app.route('/plotlyexample/')
def plotlyexample():
	dt=pd.read_csv('static/auction_data_core.csv')
	dt['monthend'] = lookup(dt['monthend'])
	df = pd.read_excel('static/rulespresheet.xlsx')
	rules = pd.read_excel('static/rulespresheet.xlsx')
	for key in request.args:
		search_key = key
	# allfields3=rules.loc[rules['DQ_Dimension']=='Accuracy']
	allfields2 = rules[['Subject_Area','Field_Name']]
	allfields1=allfields2['Field_Name'].loc[allfields2['Subject_Area']==search_key]
	allfields1=allfields1.unique()
	if request.method == 'GET':
		dtrows = []
		for key in request.args:
			search_key = key
			Rule_Type = df['Rule_Type'][df['Field_Name'] == search_key]
			Rule_Type = Rule_Type.iloc[0]
			all_rules = df['Rule_Type'].unique().tolist()
			for rule in all_rules:

				if rule == 'Numerical_check':
					df1=dt.groupby(['monthend'])[search_key].apply(get_miss).unstack()
					df2=dt.groupby(['monthend'])[search_key].apply(get_mean).unstack()
					df3=dt.groupby(['monthend'])[search_key].apply(get_zero).unstack()
					df4=dt.groupby(['monthend'])[search_key].apply(get_size).unstack()
					graphs = [
							dict(data=[
									dict(x = df1.index,
										y = df1['miss'],
										mode = 'Bar',
										name='missing',
										type='scatter'	)],
								layout=dict(title='get_miss graph')),
							dict(data=[
									dict(x = df2.index,
										y = df2['mean'],
										mode = 'Bar',
										name='mean',
										type='scatter'),],
								layout=dict(title='get_mean graph')),
							dict(data=[
									dict(x = df3.index,
										y = df3['zero'],
										mode = 'Bar',
										name='zero',
										type='scatter'),],
								layout=dict(title='get_zero graph',	domain=[0.55, 1])),
							dict(data=[
									dict(
										x = df4.index,
										y = df4['size'],
										mode = 'Bar',
										name='size',
										type='scatter'),],
								layout=dict(title='get_size graph')),
							]


				# # Add "ids" to each of the graphs to pass up to the client
				# # for templating
				ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
				#
				# # Convert the figures to JSON
				# # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
				# # objects to their JSON equivalents
				graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
				return render_template('plotly123.html',
									   ids=ids,
									   graphJSON=graphJSON)


if __name__ == "__main__":
	app.run(debug=True)



	#
	#
	# if rule == 'categorical_Check':
	# 	# df5=dt.groupby(['monthend'])[search_key].value_counts(dropna=False, normalize=True).unstack()
	# 	df2=dt.set_index(['monthend'])
	# 	trace1 = go.Scatter(
	# 		x = df2.index,
	# 		y = df2[].count(),
	# 		name = df5.columns,
	# 		mode='area'
	# 			 )
	# 	graphs = [
	# 			dict(
	# 				data = [df5.to_json()],
	# 				layout = go.Layout(
	# 						title= "Collisions and Deaths per day",
	# 						yaxis=dict(
	# 							title='collisions',
	# 							titlefont=dict(
	# 								color='#9467bd'
	# 							),
	# 							tickfont=dict(
	# 								color='#9467bd'
	# 							)
	# 						))
	# 				)]
