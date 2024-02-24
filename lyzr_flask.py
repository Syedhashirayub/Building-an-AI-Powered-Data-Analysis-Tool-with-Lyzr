from flask import Flask, request, render_template, redirect, url_for
import os
import pandas as pd
from lyzr import DataConnector, DataAnalyzr
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = '/Volumes/Hardisc/lyzr/UPLOAD_FOLDER'

# Ensure the folder for uploads exists

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return redirect(url_for('analyze', filename=filename))
    return render_template('upload.html')

@app.route('/analyze/<filename>')
def analyze(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    df = DataConnector().fetch_dataframe_from_csv(file_path)

    # Initialize a DataAnalyzr instance with the obtained DataFrame and OPEN API key                           
    data_analyzr = DataAnalyzr(df=df, api_key='OPEN_API_KEY')      

    description = data_analyzr.dataset_description()
    analysis = data_analyzr.analysis_insights(user_input=" give analysis insights of the data ")
    queries = data_analyzr.ai_queries_df()
    analysis_recommendation = data_analyzr.analysis_recommendation()


    # Prepare the report
    report = {
        'description': description,
        'analysis': analysis,
        'queries': queries,
        'analysis_recommendation': analysis_recommendation

    }

    return render_template('report.html', report=report)


if __name__ == '__main__':
    app.run(debug=True)
