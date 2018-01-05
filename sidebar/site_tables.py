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


app = Flask(__name__)

@app.route("/bzrules")
def show_tables():
	rules = pd.read_excel('static/dummy_data.xlsx')
	# rules = pd.read_excel('static/Book1.xlsx')
	rules.set_index(['DR_ID'], inplace=True)
	rules.index.name=None
	if request.method == 'GET':
		datasource = rules['Data_Source'].unique().tolist()
		search_key = request.args.get('datasource')

		subarealist2 = rules[['Data_Source','Subject_Area']]
		subarealist1=subarealist2['Subject_Area'].loc[subarealist2['Data_Source']==search_key]
		subarealist =subarealist1.unique()
		search_key = request.args.get('subjectarea')
		dfrows = rules.loc[rules['Subject_Area']==search_key]
		# allfields3=rules.loc[rules['DQ_Dimension']=='Accuracy']
		# allfields2 = allfields3[['Subject_Area','Field_Name']]
		allfields2 = rules[['Subject_Area','Field_Name']]
		allfields1=allfields2['Field_Name'].loc[allfields2['Subject_Area']==search_key]
		allfields1=allfields1.unique()
		showHeader = 'false'
		if len(dfrows['Rule']) > 0:
			showHeader = 'true'

		return render_template('indext.html', datasource=datasource,showHeader=showHeader,allfields1=allfields1,subarealist=subarealist,bzrules1=[dfrows.to_html()])

@app.route('/pygalexample/')
def pygalexample():
		dt=pd.read_excel('C:/Users/goz544/Desktop/DQA_2/DQA/static/Commercial_source_090716.xls')
		df = pd.read_excel('C:/Users/goz544/Desktop/dqt/sidebar/sidebar/static/Book1.xlsx')

		rules = pd.read_excel('static/dummy_data.xlsx')
		for key in request.args:
			search_key = key
		allfields3=rules.loc[rules['DQ_Dimension']=='Accuracy']
		allfields2 = allfields3[['Subject_Area','Field_Name']]
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
					if rule == 'Valid Value Check':
						data=dt.groupby(search_key).size().order(ascending=False)
						chart_type = pygal.Bar(legend_at_bottom=True,human_readable=True) # Create a Pygalbar graph object
						chart_type.title = "Portfolio counts (in %)" # Give the graph a title
						for k,v in data.items():
							chart_type.add(k,v)
						graph_data = chart_type.render_data_uri()
						return render_template("graphing.html", graph_data = graph_data)



@app.route('/postfields')
def postfields():
	#df1 = pd.read_excel('static/rules.xls')
	rules = pd.read_excel('static/dummy_data.xlsx')
	df = pd.read_excel('static/Book1.xlsx')
	#df=df1.loc[df1['DQ_Dimension']=='Accuracy']

	for key in request.args:
		search_key = key

	allfields3=rules.loc[rules['DQ_Dimension']=='Accuracy']
	allfields2 = allfields3[['Subject_Area','Field_Name']]
	allfields1=allfields2['Field_Name'].loc[allfields2['Subject_Area']==search_key]

	if search_key in ["Facility_Number","BorrowerName","BorrowerID","BorrowerName","TTC_PD","Downturn_LGD","Downturn_EC_EAD","Outstanding","Default_Indicator","Sub_sub_portfolio","Sub_Portfolio","PortfolioName","Sub_Portfolio1","BorrowerNAICS","CRE_Property_Type_Moodys","RF_MSA","BorrowerState","Maturity_Date","MRA_TotalAssets","MRA_NetSales","InstrumentType","BaselAssetClass","MCE","PublicobligorID"] :
		dt=pd.read_excel('static/Commercial_source_090716.xlsx')
	elif search_key in ["CONTRACTREFERENCE","COUNTERPARTYNEW","COUNTERPARTYNEWDESC","PDNEW","RWA","LGD",'EAD',"OUTSTAND","ACRUED_INTEREST","BALANCE_SHEET_AMOUNT","INCORPORATIONCOUNTRY_NEW","SCURT_PROD_CD","KMATURITY"]:
		dt=pd.read_excel('static/wholesale_bond_source_data.xls')
	elif search_key in ["TRADEID","COUNTERPARTYID","COUNTERPARTY.NEW.DESC","TTC PD","DOWNSTREAMLGD","DOWNSTREAMEAD","MARKETVALUE","DEALNOTIONAL","RESIDUALMATURITY","CUSTOMER_TYPE","VALID_CPY_PERIMETER","CONSO_PERIMETER","INTERCO","TRANCHECOLLATERALTYPE"]:
		dt=pd.read_excel('static/tradeddownstream_input_data.xls')
	else:
		dt=pd.read_excel('static/tradedupstream_input_data.xls')
	#return search_key
	allfields = df['Field_Name'].unique().tolist()
	if request.method == 'GET':
		dtrows = []
		for key in request.args:
			search_key = key
			Describe_res =dt[search_key].describe()
			total_rows=len(dt[search_key])
			null_rows = dt[search_key].isnull().sum()
			dfrows = df.loc[df['Field_Name']==search_key]
			all_counts = {}
			Accuracy={}
			Complete={}
			Rule_Type = df['Rule_Type'][df['Field_Name'] == search_key]
			Rule_Type = Rule_Type.iloc[0]
			all_rules = df['Rule_Type'].unique().tolist()
			l = []
			l.append(Rule_Type)
			all_rules = l


			for rule in all_rules:
				if rule == 'Distinct Value Check':
					unique_rows= len(dt[search_key].unique())
					all_counts[rule] = unique_rows
					Accuracy[rule]=(unique_rows/total_rows)*100
					Complete[rule]=((total_rows-null_rows)/total_rows)*100
				elif rule == 'Valid Range Check':
					df2=df[['Field_Name','DQ_Dimension','MIN_VAL','MAX_VAL']][df.Field_Name==search_key]
					df3=df2[['Field_Name','MIN_VAL','MAX_VAL']][df2.DQ_Dimension=='Accuracy']
					min_val = float(df3.iloc[0]['MIN_VAL'])
					max_val = float(df3.iloc[0]['MAX_VAL'])
					range=dt[(dt[search_key]>=min_val)&(dt[search_key]<=max_val)]
					range_count=len(range)
					Accuracy[rule]=(range_count/total_rows)*100
					Complete[rule]=((total_rows-null_rows)/total_rows)*100
					all_counts[rule] = range_count
				elif rule == 'Valid Length Check':
					df2=df[['Field_Name','DQ_Dimension','MIN_VAL','MAX_VAL']][df.Field_Name==search_key]
					df3=df2[['Field_Name','MIN_VAL','MAX_VAL']][df2.DQ_Dimension=='Accuracy']
					min_val = df3.iloc[0]['MIN_VAL']
					max_val = df3.iloc[0]['MAX_VAL']
					dt[search_key]=dt[search_key].astype('str')
					range=((dt[search_key].str.len()>=min_val)&(dt[search_key].str.len()<=max_val))
					range_count=len(dt.loc[range])
					Accuracy[rule]=(range_count/total_rows)*100
					Complete[rule]=((total_rows-null_rows)/total_rows)*100
					all_counts[rule]=range_count
				elif rule=='Valid Date Check':
					df2=df[['Field_Name','DQ_Dimension','MIN_VAL','MAX_VAL']][df.Field_Name==search_key]
					df3=df2[['Field_Name','MIN_VAL','MAX_VAL']][df2.DQ_Dimension=='Accuracy']
					min_val = df3.iloc[0]['MIN_VAL']
					max_val = df3.iloc[0]['MAX_VAL']
					dt[search_key] = pd.to_datetime(dt[search_key],errors='coerce')
					range=((dt[search_key] >= min_val)&(dt[search_key] <= max_val))
					range_count=len(dt.loc[range])
					Accuracy[rule]=(range_count/total_rows)*100
					Complete[rule]=((total_rows-null_rows)/total_rows)*100
					all_counts[rule] = 	range_count
				elif rule=='Valid Value Check':
					df2=df[['Field_Name','DQ_Dimension','DQ_VALID_VALUE']][df.Field_Name==search_key]
					df3=df2[['Field_Name','DQ_VALID_VALUE']][df2.DQ_Dimension=='Accuracy']
					val=df3.iloc[0]['DQ_VALID_VALUE']
					val = val.strip()
					Value=val.split(',')
					if search_key == 'Default_Indicator':
						Value[0] = int(Value[0])
						Value[1] = int(Value[1])
					range_count =len(dt[search_key][dt[search_key].isin(Value)==True])
					Accuracy[rule]=(range_count/total_rows)*100
					Complete[rule]=((total_rows-null_rows)/total_rows)*100
					all_counts[rule] = range_count
			dtrows.append(pd.DataFrame([[search_key,dfrows['Rule'],dfrows['Rule_Type'],total_rows,all_counts[rule],null_rows,np.round(Accuracy[rule], 2),np.round(Complete[rule], 2),Describe_res]]))
			# dtrows.append(pd.DataFrame([[search_key,dfrows['Rule'],dfrows['Rule_Type'],total_rows,all_counts[rule],null_rows,Accuracy[rule],Complete[rule]]]))
			print(request.form.values)

		showHeader = 'false'
		if len(dfrows['Rule']) > 0:
			showHeader = 'true'

		return render_template('indext.html',showHeader=showHeader,allfields=allfields,rules=dfrows[['Rule','Rule_Type']].to_html(header=False),all_counts=dtrows,search_key=search_key)


if __name__ == "__main__":
	app.run(debug=True)
