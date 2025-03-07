import pandas as pd
import re
import gradio as gr
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
quran_english_with_surah = pd.read_csv('datasets/en.yusufali.csv')
surah_names = pd.read_csv('datasets/surah_names_english.csv', names=['Surah', 'Surah Name'])
surah_names["Surah Name"] = surah_names["Surah Name"].str[1:]
quran_english_with_surah = quran_english_with_surah.merge(surah_names, on='Surah')
quran_english_with_surah.index = pd.RangeIndex(start=1, stop=len(quran_english_with_surah) + 1)

# Create the inverted index
def create_inverted_index(dataframe):
    inverted_index = defaultdict(list)
    for index, row in dataframe.iterrows():
        words = row['Text'].split()
        for word in words:
            word = re.sub(r'\W+', '', word).lower()
            if word:
                inverted_index[word].append((row['Surah'], row['Ayah']))
    return inverted_index

inverted_index = create_inverted_index(quran_english_with_surah)

# Define the search function
def search_quran(keyword):
    results = []
    if keyword.lower() not in inverted_index:
        return f"No occurrences found for '{keyword}'"
    
    verse_ids = inverted_index[keyword.lower()]
    for verse_id in verse_ids:
        surah_num, verse_num = verse_id
        verse_data = quran_english_with_surah[(quran_english_with_surah['Surah'] == surah_num) & 
                             (quran_english_with_surah['Ayah'] == verse_num)]
        surah_name = verse_data['Surah Name'].iloc[0]
        verse_text = verse_data['Text'].iloc[0]
        highlighted_text = re.sub(f"(?i)({keyword})", r'<mark style="background-color: yellow; color: black;">\1</mark>', verse_text)
        results.append(f"<div style='padding: 10px; border-bottom: 1px solid #ccc;'>"
                       f"<strong>Surah:</strong> {surah_name}<br>"
                       f"<strong>Reference:</strong> {surah_num}:{verse_num}<br>"
                       f"<strong>Occurrences in verse:</strong> {verse_text.lower().count(keyword.lower())}<br>"
                       f"<strong>Text:</strong> {highlighted_text}</div>")
    return '<div style="max-height: 500px; overflow-y: auto; width: 100%; font-size: 18px;">' + ''.join(results) + '</div>'

# Function to generate and return the plots and tables as HTML
def generate_plots_and_tables():
    # Plot 1: Number of verses in each chapter
    plt.figure(figsize=(30, 10))
    sns.set_style('whitegrid')
    ax = sns.barplot(x=quran_english_with_surah['Surah Name'].value_counts().index, 
                     y=quran_english_with_surah['Surah Name'].value_counts().values, 
                     palette='viridis')
    for container in ax.containers:
        ax.bar_label(container, size=10, padding=2)
    ax.set_title('Number of Verses in Each Chapter', fontweight='bold', fontsize=14)
    ax.set_ylabel('Number of Verses', fontweight='bold')
    ax.set_xlabel('Surah Name', fontweight='bold')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plot1_html = plt_to_html(plt)

    # Table: Surah names and their counts
    surah_counts = quran_english_with_surah['Surah Name'].value_counts().reset_index()
    surah_counts.columns = ['Surah Name', 'Ayah Count']
    table_html = surah_counts.to_html(index=False, classes='table table-striped table-hover')
    table_html = f'<div style="max-height: 300px; overflow-y: auto;">{table_html}</div>'

    return plot1_html + table_html

# Helper function to convert matplotlib plot to HTML
def plt_to_html(plt):
    import io
    from base64 import b64encode
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = b64encode(buf.read()).decode('utf-8')
    plt.close()
    return f'<img src="data:image/png;base64,{img_str}"/>'

# Create the Gradio interface with a modern theme
css = """
body {
    font-family: 'Arial', sans-serif;
    background-color: #FFF2F2;
    color: #2D336B;
    margin: 0;
    padding: 0;
}
.gradio-container {
    max-width: 100%;
    margin: 0 auto;
    padding: 20px;
}
.gradio-input, .gradio-output {
    width: 100%;
}
.gradio-title {
    font-size: 2em;
    font-weight: bold;
    margin-bottom: 20px;
    color: #2D336B;
}
.gradio-description {
    font-size: 1.2em;
    margin-bottom: 20px;
    color: #2D336B;
}
.table {
    width: 100%;
    border-collapse: collapse;
    background-color: #A9B5DF;
}
.table th, .table td {
    padding: 8px 12px;
    border: 1px solid #2D336B;
}
.table th {
    background-color: #7886C7;
    font-weight: bold;
    color: #FFF2F2;
}
.table-striped tbody tr:nth-of-type(odd) {
    background-color: #A9B5DF;
}
.table-hover tbody tr:hover {
    background-color: #7886C7;
    color: #FFF2F2;
}
"""

# Define the Gradio interface with tabs
with gr.Blocks(css=css) as iface:
    with gr.Tab("Search"):
        gr.Markdown("# Quran Keyword Search")
        keyword_input = gr.Textbox(label="Enter a keyword")
        search_results = gr.HTML(label="Search Results")
        search_button = gr.Button("Search")
        search_button.click(search_quran, inputs=keyword_input, outputs=search_results)
    
    with gr.Tab("Statistics"):
        gr.Markdown("# Quran Statistics")
        stats_output = gr.HTML(value=generate_plots_and_tables())

iface.launch(share=True)
