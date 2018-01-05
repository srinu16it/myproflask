# @app.route('/pygalexample/')
# def pygalexample():
# 		dt=pd.read_excel('C:/Users/goz544/Desktop/DQA_2/DQA/static/Commercial_source_090716.xls')
# 		df = pd.read_excel('C:/Users/goz544/Desktop/dqt/sidebar/sidebar/static/Book1.xlsx')
# 		if request.method == 'GET':
# 			dtrows = []
# 			for key in request.args:
# 				search_key = key
# 				Rule_Type = df['Rule_Type'][df['Field_Name'] == search_key]
# 				Rule_Type = Rule_Type.iloc[0]
# 				all_rules = df['Rule_Type'].unique().tolist()
# 				for rule in all_rules:
# 					if rule == 'Valid Value Check':
# 						data=dt.groupby(search_key).size().order(ascending=False)
# 						chart_type = pygal.Pie() # Create a Pygalbar graph object
# 						chart_type.title = "Portfolio counts (in %)" # Give the graph a title
# 						for k,v in data.items():
# 							chart_type.add(k,v)
# 						graph_data = chart_type.render_data_uri()
# 		return render_template("graphing.html", graph_data = graph_data)
