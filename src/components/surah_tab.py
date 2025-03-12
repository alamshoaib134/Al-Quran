import gradio as gr
import os

def load_surah(surah_name_with_number, quran_data):
    """
    Load verses and word cloud for a specific Surah.
    
    Args:
        surah_name_with_number (str): Format: "number. Surah Name"
        quran_data (pd.DataFrame): The Quran dataset
        
    Returns:
        tuple: (list of verses, word cloud image path)
    """
    surah_number = int(surah_name_with_number.split('.')[0])
    surah_name = surah_name_with_number.split('. ')[1]
    surah_verses = quran_data[quran_data['Surah'] == surah_number]['Text'].tolist()
    word_cloud_path = f"word_cloud/surah_{surah_number}_{surah_name}.png"
    return surah_verses, word_cloud_path

def display_surah(surah_name_with_number, quran_data):
    """
    Get the verses text and word cloud for display.
    
    Args:
        surah_name_with_number (str): Format: "number. Surah Name"
        quran_data (pd.DataFrame): The Quran dataset
        
    Returns:
        tuple: (verses text, word cloud image path)
    """
    verses, word_cloud_path = load_surah(surah_name_with_number, quran_data)
    verses_text = "\n".join(verses)
    return verses_text, word_cloud_path

def create_surah_tab(quran_data, surah_names_list):
    """
    Create the Surah tab interface with description and display components.
    
    Args:
        quran_data (pd.DataFrame): The Quran dataset
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
        - View the complete English translation
        - See a visual word cloud representation of the Surah
        - Understand the most frequently used terms in each chapter
        
        Select a Surah from the dropdown menu to begin exploring.
        </div>
        """)
        
        surah_name_with_number = gr.Dropdown(
            label="Select a Surah",
            choices=surah_names_list,
            info="Choose a Surah to view its verses and word cloud"
        )
        
        with gr.Row():
            verses_output = gr.Textbox(
                label="Verses",
                lines=18,
                visible=False,
                elem_classes="verses-output"
            )
            word_cloud_output = gr.Image(
                label="Word Cloud Visualization",
                visible=False,
                elem_classes="word-cloud-output"
            )
        
        def update_visibility_and_load_surah(surah_name):
            verses_text, word_cloud_path = display_surah(surah_name, quran_data)
            return gr.update(visible=True, value=verses_text), gr.update(visible=True, value=word_cloud_path)
        
        surah_name_with_number.change(
            update_visibility_and_load_surah,
            inputs=[surah_name_with_number],
            outputs=[verses_output, word_cloud_output]
        )
    
    return tab