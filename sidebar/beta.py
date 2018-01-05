from flask import Flask
import pandas as pd
import datetime
from flask import request
import numpy as np
from flask import render_template,flash, redirect,url_for
app = Flask(__name__)

@app.route('/postfields')
def postfields():
	df1 = pd.read_excel('static/rules.xls')
	df=df1.loc[df1['DQ_Dimension']=='Accuracy']
	dt=pd.read_excel('static/Commercial_source_090716.xls')
	allfields = df['Field_Name'].unique().tolist()
	if request.method == 'GET':
		dtrows = []
		for key in request.args:
			search_key = key
			total_rows=len(dt[search_key])
			null_rows = dt[search_key].isnull().sum()
			dfrows = df.loc[df['Field_Name']==search_key]
			all_counts = {}
			Accuracy={}
			Complete={}
			Rule_Type = df1['Rule_Type'][df['Variable_Name']==search_key]
			Rule_Type = Rule_Type.iloc[0]
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
					#min_date = datetime.date(min_val[6:],min_val[:2],min_val[3:5])
					#max_date = datetime.date(max_val[6:],max_val[:2],max_val[3:5])
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
					#w=pd.Series([val],name='val')
					#Value=w.tolist()
					if search_key == 'Default_Indicator':
						Value[0] = int(Value[0])
						Value[1] = int(Value[1])

					range_count =len(dt[search_key][dt[search_key].isin(Value)==True])
					Accuracy[rule]=(range_count/total_rows)*100
					Complete[rule]=((total_rows-null_rows)/total_rows)*100
					all_counts[rule] = range_count
			dtrows.append(pd.DataFrame([[search_key,dfrows['Rule'],dfrows['Rule_Type'],total_rows,all_counts[rule],null_rows,Accuracy[rule],Complete[rule]]]))
			print(request.form.values)
		return render_template('index.html',allfields=allfields)
		# return render_template('index.html',allfields=allfields,rules=dfrows[['Rule','Rule_Type']].to_html(),all_counts=dtrows,search_key=search_key)

if __name__ == '__main__':
    app.run(debug=True)
