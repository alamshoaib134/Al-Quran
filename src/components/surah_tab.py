import gradio as gr
import os

def load_surah(surah_name_with_number, quran_data, arabic_data, urdu_data):
    """
    Load verses and word cloud for a specific Surah in multiple languages.
    
    Args:
        surah_name_with_number (str): Format: "number. Surah Name"
        quran_data (pd.DataFrame): The English Quran dataset
        arabic_data (pd.DataFrame): The Arabic Quran dataset
        urdu_data (pd.DataFrame): The Urdu Quran dataset
        
    Returns:
        tuple: (dict of verses in different languages, word cloud image path)
    """
    surah_number = int(surah_name_with_number.split('.')[0])
    surah_name = surah_name_with_number.split('. ')[1]
    
    # Load verses in each language
    english_verses = quran_data[quran_data['Surah'] == surah_number]['Text'].tolist()
    arabic_verses = arabic_data[arabic_data['Surah'] == surah_number]['Text'].tolist()
    urdu_verses = urdu_data[urdu_data['Surah'] == surah_number]['Text'].tolist()
    
    verses = {
        'english': english_verses,
        'arabic': arabic_verses,
        'urdu': urdu_verses
    }
    
    word_cloud_path = f"word_cloud/surah_{surah_number}_{surah_name}.png"
    return verses, word_cloud_path

def display_surah(surah_name_with_number, quran_data, arabic_data, urdu_data):
    """
    Get the verses text in multiple languages and word cloud for display.
    
    Args:
        surah_name_with_number (str): Format: "number. Surah Name"
        quran_data (pd.DataFrame): The English Quran dataset
        arabic_data (pd.DataFrame): The Arabic Quran dataset
        urdu_data (pd.DataFrame): The Urdu Quran dataset
        
    Returns:
        tuple: (dict of verses text, word cloud image path)
    """
    verses, word_cloud_path = load_surah(surah_name_with_number, quran_data, arabic_data, urdu_data)
    
    # Add verse numbers and join verses for each language
    verses_text = {}
    max_verses = max(len(verses['english']), len(verses['arabic']), len(verses['urdu']))
    
    # Language-specific verse formatting
    for lang in ['english', 'arabic', 'urdu']:
        numbered_verses = []
        for i, verse in enumerate(verses[lang][:max_verses], 1):
            if lang == 'arabic':
                numbered_verses.append(f"{verse} ﴿{i}﴾")
            elif lang == 'urdu':
                numbered_verses.append(f"[{i}] {verse}")
            else:
                numbered_verses.append(f"{i}. {verse}")
        verses_text[lang] = "\n\n".join(numbered_verses)
    
    return verses_text, word_cloud_path

def create_surah_tab(quran_data, arabic_data, urdu_data, surah_names_list):
    """
    Create the Surah tab interface with multilingual display components.
    
    Args:
        quran_data (pd.DataFrame): The English Quran dataset
        arabic_data (pd.DataFrame): The Arabic Quran dataset
        urdu_data (pd.DataFrame): The Urdu Quran dataset
        surah_names_list (list): List of formatted Surah names
        
    Returns:
        gr.Tab: The configured Surah tab
    """
    with gr.Tab("Surah") as tab:
        gr.Markdown("# Surah Explorer")
        gr.Markdown("""
        <div class='tab-description'>
        Welcome to the Surah Explorer! This tool allows you to:
        - Select and read any Surah from the Quran
        - View the complete text in Arabic, Urdu, and English
        - See a visual word cloud representation of the Surah
        - Compare translations side by side
        
        Select a Surah from the dropdown menu to begin exploring.
        </div>
        """)
        
        surah_name_with_number = gr.Dropdown(
            label="Select a Surah",
            choices=surah_names_list,
            info="Choose a Surah to view its verses and word cloud"
        )
        
        with gr.Row():
            # Create three equal columns for different languages
            with gr.Column(scale=1):
                arabic_output = gr.Textbox(
                    label="Arabic",
                    lines=18,
                    visible=False,
                    elem_classes=["verses-output", "arabic-text"],
                    rtl=True,
                    show_label=True,
                    container=True
                )
            with gr.Column(scale=1):
                urdu_output = gr.Textbox(
                    label="Urdu",
                    lines=18,
                    visible=False,
                    elem_classes=["verses-output", "urdu-text"],
                    show_label=True,
                    container=True
                )
            with gr.Column(scale=1):
                english_output = gr.Textbox(
                    label="English",
                    lines=18,
                    visible=False,
                    elem_classes=["verses-output", "english-text"],
                    show_label=True,
                    container=True
                )
            
        with gr.Row():
            word_cloud_output = gr.Image(
                label="Word Cloud Visualization",
                visible=False,
                elem_classes="word-cloud-output"
            )
        
        def update_visibility_and_load_surah(surah_name):
            verses_text, word_cloud_path = display_surah(surah_name, quran_data, arabic_data, urdu_data)
            return (
                gr.update(visible=True, value=verses_text['arabic']),
                gr.update(visible=True, value=verses_text['urdu']),
                gr.update(visible=True, value=verses_text['english']),
                gr.update(visible=True, value=word_cloud_path)
            )
        
        surah_name_with_number.change(
            update_visibility_and_load_surah,
            inputs=[surah_name_with_number],
            outputs=[arabic_output, urdu_output, english_output, word_cloud_output]
        )
    
    return tab