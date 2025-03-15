import gradio as gr
from components.utils import load_data, load_css, get_surah_names_list
from components.search_tab import create_search_tab
from components.statistics_tab import create_statistics_tab
from components.surah_tab import create_surah_tab
from components.verse_locator_tab import create_verse_locator_tab

def main():
    """
    Main function to create and launch the Quran Explorer application.
    The app provides three main features:
    1. Keyword search across the Quran
    2. Statistical analysis and visualizations
    3. Surah-wise exploration with word clouds
    """
    # Load data
    quran_data, surah_names = load_data()
    surah_names_list = get_surah_names_list(surah_names)
    
    # Create the Gradio interface
    with gr.Blocks(css=load_css()) as iface:
        gr.Markdown("""
        # Quran Explorer
        Welcome to the Quran Explorer application. This tool provides multiple ways to explore 
        and understand the Holy Quran through its English translation. Use the tabs below to:
        - Search for specific words or phrases
        - View statistical insights and visualizations
        - Read complete Surahs with word cloud visualizations
        """)
        
        # Create tabs
        search_tab = create_search_tab(quran_data)
        statistics_tab = create_statistics_tab(quran_data)
        surah_tab = create_surah_tab(quran_data, surah_names_list)
        surah_counts = quran_data['Surah Name'].value_counts().reset_index()
        surah_counts.columns = ['Surah Name', 'Ayah Count']
        verse_locator_tab = create_verse_locator_tab(quran_data, surah_names_list, surah_counts)
    
    # Launch the interface
    iface.launch(share=True)

if __name__ == "__main__":
    main()