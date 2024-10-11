from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pheno_file = request.files['phenotype']
        allele_file = request.files['allele']

        if pheno_file and allele_file:
            pheno_path = os.path.join(UPLOAD_FOLDER, pheno_file.filename)
            allele_path = os.path.join(UPLOAD_FOLDER, allele_file.filename)

            pheno_file.save(pheno_path)
            allele_file.save(allele_path)

            # Run the analysis and plot generation
            plot_path1 = generate_plots(pheno_path, allele_path)

            return render_template('result.html', plot1=plot_path1)

    return render_template('index.html')

def generate_plots(pheno_file, allele_file):
    # Load phenotype and allele data
    pheno = pd.read_csv(pheno_file, sep="\t")
    allele_data = pd.read_csv(allele_file, sep=",", quotechar='"')

    # Rename columns and merge data
    allele_data.rename(columns={'strain': 'Accession_ID', 'alt': 'alt'}, inplace=True)
    snp_pheno = pd.merge(pheno, allele_data[['Accession_ID', 'alt']], on='Accession_ID', how='left')
    snp_pheno['allele'] = np.where(snp_pheno['alt'] == 'C', 'minor', 'major')
    snp_pheno['allele'].fillna('major', inplace=True)
    snp_pheno['treatment'] = pd.Categorical(snp_pheno['treatment'], categories=['Mock', 'ABA'], ordered=True)

    # Plotting Half Violin Plot
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=snp_pheno, x='treatment', y='Ave_RLN', hue='treatment', split=True, inner=None)
    sns.boxplot(data=snp_pheno, x='treatment', y='Ave_RLN', width=0.05, showcaps=False,
                boxprops={'facecolor': 'white', 'edgecolor': 'black', 'linewidth': 2},
                meanprops={'color': 'red', 'linewidth': 2},
                palette={'Mock': 'orange', 'ABA': 'skyblue'})

    for _, group_data in snp_pheno.groupby('Accession_ID'):
        plt.plot(group_data['treatment'], group_data['Ave_RLN'], color='grey', alpha=0.3)

    plt.title('Half Violin Plot of Ave_RLN by Treatment')
    violin_plot_path = os.path.join('static', 'violin_plot.jpg')
    plt.savefig(violin_plot_path, format='jpeg')
    plt.close()

    return violin_plot_path

if __name__ == '__main__':
    app.run(debug=True)
