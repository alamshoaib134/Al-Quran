import pandas as pd
import re
import gradio as gr
from collections import defaultdict

# Load the dataset
quran_english_with_surah = pd.read_csv('/Users/salam9/Desktop/quran/en.yusufali.csv')
surah_names = pd.read_csv('/Users/salam9/Desktop/quran/surah_names_english.csv', names=['Surah', 'Surah Name'])
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

# Create the Gradio interface with a modern theme
css = """
body {
    font-family: 'Arial', sans-serif;
    background-color: #f4f4f9;
    color: #333;
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
}
.gradio-description {
    font-size: 1.2em;
    margin-bottom: 20px;
}
"""

iface = gr.Interface(
    fn=search_quran,
    inputs=gr.Textbox(label="Enter a keyword"),
    outputs=gr.HTML(label="Search Results"),
    title='Quran Keyword Search',
    description='Enter a keyword to search in the Quran',
    css=css
)
iface.launch(share=True)
