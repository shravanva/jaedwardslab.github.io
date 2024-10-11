from flask import Flask, render_template, request, jsonify, url_for
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)

# Ensure the uploads directory exists
os.makedirs('uploads', exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Retrieve the uploaded files
            phenotype_file = request.files.get('phenotype_file')
            allele_file = request.files.get('allele_file')
            
            if not phenotype_file or not allele_file:
                return jsonify({'success': False, 'error': 'Both files are required!'})

            # Save files temporarily
            phenotype_filepath = os.path.join("uploads", phenotype_file.filename)
            allele_filepath = os.path.join("uploads", allele_file.filename)
            phenotype_file.save(phenotype_filepath)
            allele_file.save(allele_filepath)

            # Debug: Check if the files were saved correctly
            print(f"Phenotype file saved at: {phenotype_filepath}")
            print(f"Allele file saved at: {allele_filepath}")

            # Load data using pandas
            pheno = pd.read_csv(phenotype_filepath, sep="\t")
            allele_data = pd.read_csv(allele_filepath, sep=",", quotechar='"')

            # Debug: Print some of the data to verify it's loaded
            print("Phenotype Data Sample:")
            print(pheno.head())
            print("Allele Data Sample:")
            print(allele_data.head())

            # Data processing and plotting code (simplified for testing)
            plt.figure(figsize=(10, 6))
            sns.violinplot(data=pheno, x=pheno.columns[0], y=pheno.columns[1])
            plot_path = os.path.join('static', 'plot1.jpg')
            plt.savefig(plot_path, format='jpeg')

            # Debug: Check if the image was saved correctly
            print(f"Plot saved at: {plot_path}")

            return jsonify({'success': True, 'image_url': url_for('static', filename='plot1.jpg')})

        except Exception as e:
            # Debug: Print exception details
            print(f"Error: {e}")
            return jsonify({'success': False, 'error': f'Error processing files: {str(e)}'})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
