from flask import *
from flask import render_template,flash, redirect,url_for,redirect, request, Response, send_from_directory, jsonify
import pandas as pd
from pandas import DataFrame
import numpy as np
import os, time, random,datetime,re
from forms import *

app = Flask(__name__)
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = "jk3k43l"

MAX_UID = 1
DATASETS = [] # Stores DataFrames for multiuser mode
while len(DATASETS) <= MAX_UID:
    DATASETS.append(DataFrame())
uid = 0

@app.route("/table")
def table():
    global uid
    if uid != None:
        if DATASETS[uid].shape[1] > 0:
            return DATASETS[uid].head(50).to_html(classes=['main_table'])
        else:
            return ""
    else:
        return ""

@app.route("/")
def index():
    if uid is None:
        redirect("/login")
    return render_template("indext.html")

@app.route("/upload", methods=["GET","POST"])
def upload():
    global uid, DATASETS
    form = CSVForm()
    fnm = ""
    if form.validate_on_submit():
        try:
            fileid = "C:/Users/goz544/Desktop/dqt/Web-CSV-master/Web-CSV-master/examples/csv-%s.csv" % (time.time()+random.randint(1,100))
            form.csvf.data.save(fileid)
            if form.rewrite.data == False and DATASETS[uid].shape[0] != 0:
                tmp = pd.read_csv(fileid, engine='c')
                if form.join_cols.data == False:
                    if len(tmp.columns) == len(DATASETS[uid].columns):
                        DATASETS[uid] = pd.concat([DATASETS[uid], tmp])
                else:
                        DATASETS[uid] = pd.concat([DATASETS[uid], tmp], axis=1)
            else:
                DATASETS[uid] = pd.read_csv(fileid)
            os.remove(fileid)
            fnm = "Uploaded!"
        except Exception as e:
            fnm = "Wrong file content! Error: %s" % str(e)
    return render_template("upload.html", form=form, filename=fnm)

if __name__ == "__main__":
	app.run(debug=True)
