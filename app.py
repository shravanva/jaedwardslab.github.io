from flask import Flask, render_template, request, jsonify, url_for
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)

# Ensure directories for uploads and static files exist
os.makedirs('uploads', exist_ok=True)
os.makedirs('static', exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Retrieve uploaded files
            phenotype_file = request.files.get('phenotype_file')
            allele_file = request.files.get('allele_file')
            
            if not phenotype_file or not allele_file:
                return jsonify({'success': False, 'error': 'Both files are required!'})

            # Save files temporarily
            phenotype_filepath = os.path.join("uploads", phenotype_file.filename)
            allele_filepath = os.path.join("uploads", allele_file.filename)
            phenotype_file.save(phenotype_filepath)
            allele_file.save(allele_filepath)

            # Load data using pandas
            pheno = pd.read_csv(phenotype_filepath, sep="\t")
            allele_data = pd.read_csv(allele_filepath, sep=",", quotechar='"')

            # Data processing and plotting code
            allele_data.rename(columns={'strain': 'Accession_ID', 'alt': 'alt'}, inplace=True)
            snp_pheno = pd.merge(pheno, allele_data[['Accession_ID', 'alt']], on='Accession_ID', how='left')
            snp_pheno['allele'] = np.where(snp_pheno['alt'] == 'C', 'minor', 'major')
            snp_pheno['allele'].fillna('major', inplace=True)
            snp_pheno['treatment'] = pd.Categorical(snp_pheno['treatment'], categories=['Mock', 'ABA'], ordered=True)

            # Plotting code
            plt.figure(figsize=(10, 6))
            sns.violinplot(data=snp_pheno, x='treatment', y='Ave_RLN', hue='treatment', split=True, inner=None)
            sns.boxplot(data=snp_pheno, x='treatment', y='Ave_RLN', width=0.05, showcaps=False,
                        boxprops={'facecolor': 'white', 'edgecolor': 'black', 'linewidth': 2},
                        meanprops={'color': 'red', 'linewidth': 2},
                        palette={'Mock': 'orange', 'ABA': 'skyblue'})

            plot_path = os.path.join('static', 'plot1.jpg')
            plt.savefig(plot_path, format='jpeg')
            plt.close()

            return jsonify({'success': True, 'image_url': url_for('static', filename='plot1.jpg')})

        except Exception as e:
            return jsonify({'success': False, 'error': f'Error processing files: {str(e)}'})

    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)
