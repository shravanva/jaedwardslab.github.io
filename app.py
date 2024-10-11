from flask import Flask, request, jsonify, render_template
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)

# Folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_files():
    if 'phenotype_file' not in request.files or 'allele_file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})

    phenotype_file = request.files['phenotype_file']
    allele_file = request.files['allele_file']

    if phenotype_file.filename == '' or allele_file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})

    # Save the uploaded files
    pheno_path = os.path.join(UPLOAD_FOLDER, phenotype_file.filename)
    allele_path = os.path.join(UPLOAD_FOLDER, allele_file.filename)
    phenotype_file.save(pheno_path)
    allele_file.save(allele_path)

    # Call your existing data processing code
    try:
        pheno = pd.read_csv(pheno_path, sep="\t")
        allele_data = pd.read_csv(allele_path, sep=",", quotechar='"')

        # Your data processing code goes here
        # (Make sure to modify paths for saving plots)
        
        # Example of generating a plot and saving it
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=pheno, x='treatment', y='Ave_RLN')  # Simplified example
        result_image_path = os.path.join(RESULT_FOLDER, 'result_plot.jpeg')
        plt.savefig(result_image_path)  # Save plot as JPEG
        plt.close()

        return jsonify({'success': True, 'image_url': result_image_path})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
