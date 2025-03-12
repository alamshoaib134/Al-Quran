import gradio as gr
import re
from collections import defaultdict

def create_inverted_index(dataframe):
    """
    Create an inverted index from the Quran dataset for efficient word searching.
    
    Args:
        dataframe (pd.DataFrame): The Quran dataset with Text column
        
    Returns:
        defaultdict: A dictionary mapping words to their locations (surah, ayah)
    """
    inverted_index = defaultdict(list)
    for index, row in dataframe.iterrows():
        words = row['Text'].split()
        for word in words:
            word = re.sub(r'\W+', '', word).lower()
            if word:
                inverted_index[word].append((row['Surah'], row['Ayah']))
    return inverted_index

def search_quran(keyword, quran_data, inverted_index):
    """
    Search for a keyword in the Quran and return formatted results.
    
    Args:
        keyword (str): The word to search for
        quran_data (pd.DataFrame): The Quran dataset
        inverted_index (defaultdict): The inverted index for word searching
        
    Returns:
        str: HTML formatted search results
    """
    results = []
    if not keyword or keyword.lower() not in inverted_index:
        return f"No occurrences found for '{keyword}'"
    
    verse_ids = inverted_index[keyword.lower()]
    for verse_id in verse_ids:
        surah_num, verse_num = verse_id
        verse_data = quran_data[(quran_data['Surah'] == surah_num) & 
                              (quran_data['Ayah'] == verse_num)]
        surah_name = verse_data['Surah Name'].iloc[0]
        verse_text = verse_data['Text'].iloc[0]
        highlighted_text = re.sub(
            f"(?i)({keyword})", 
            r'<mark style="background-color: yellow; color: black;">\1</mark>', 
            verse_text
        )
        results.append(
            f"<div style='padding: 10px; border-bottom: 1px solid #ccc;'>"
            f"<strong>Surah:</strong> {surah_name}<br>"
            f"<strong>Reference:</strong> {surah_num}:{verse_num}<br>"
            f"<strong>Occurrences in verse:</strong> {verse_text.lower().count(keyword.lower())}<br>"
            f"<strong>Text:</strong> {highlighted_text}</div>"
        )
    return '<div style="max-height: 500px; overflow-y: auto; width: 100%; font-size: 18px;">' + ''.join(results) + '</div>'

def create_search_tab(quran_data):
    """
    Create the search tab interface with description and functionality.
    
    Args:
        quran_data (pd.DataFrame): The Quran dataset
        
    Returns:
        gr.Tab: The configured search tab
    """
    inverted_index = create_inverted_index(quran_data)
    
    with gr.Tab("Search") as tab:
        gr.Markdown("# Quran Keyword Search")
        gr.Markdown("""
        <div class='tab-description'>
        Welcome to the Quran Search tool! This feature allows you to:
        - Search for any word or phrase in the English translation
        - See highlighted matches in their original context
        - View Surah name and verse references for each result
        - Track the number of occurrences in each verse
        </div>
        """)
        
        keyword_input = gr.Textbox(
            label="Enter a keyword",
            placeholder="Type a word to search in the Quran"
        )
        search_results = gr.HTML(label="Search Results")
        search_button = gr.Button("Search")
        
        def search_wrapper(keyword):
            return search_quran(keyword, quran_data, inverted_index)
        
        search_button.click(
            search_wrapper,
            inputs=keyword_input,
            outputs=search_results
        )
    
    return tab