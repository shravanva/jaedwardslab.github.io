from flask import Flask, render_template, request, jsonify, url_for
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phenotype_file = request.files.get('phenotype_file')
        allele_file = request.files.get('allele_file')
        
        if not phenotype_file or not allele_file:
            return jsonify({'success': False, 'error': 'Please upload both files!'})

        try:
            # Save files temporarily
            phenotype_filepath = os.path.join("uploads", phenotype_file.filename)
            allele_filepath = os.path.join("uploads", allele_file.filename)
            phenotype_file.save(phenotype_filepath)
            allele_file.save(allele_filepath)

            # Load data using pandas
            pheno = pd.read_csv(phenotype_filepath, sep="\t")
            allele_data = pd.read_csv(allele_filepath, sep=",", quotechar='"')

            # Data processing and plotting code...
            plt.figure(figsize=(10, 6))
            sns.violinplot(data=pheno, x='some_column', y='another_column')
            plt.savefig('static/plot1.jpg', format='jpeg')

            return jsonify({'success': True, 'image_url': url_for('static', filename='plot1.jpg')})

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
