import gradio as gr
import pandas as pd

def load_verse(surah_number, verse_number, quran_data, surah_counts):
    """
    Load a specific verse from a Surah.

    Args:
        surah_number (int): The Surah number.
        verse_number (int): The verse number.
        quran_data (pd.DataFrame): The Quran dataset.

    Returns:
        str: The verse text or an error message if the verse is not found.
    """
    surah_data = quran_data[quran_data['Surah'] == surah_number].reset_index(drop=True)
    surah_data.index += 1
    max_verse_number = surah_counts[surah_counts['Surah Name'] == surah_data['Surah Name'].iloc[0]]['Ayah Count'].values[0]
    try:
        if verse_number <= max_verse_number:
            return surah_data.loc[verse_number, 'Text']
        else:
            return f"Verse number {verse_number} not found in Surah {surah_number}. Maximum verse number is {max_verse_number}."
    except KeyError:
        return f"Verse number {verse_number} not found in Surah {surah_number}."

def create_verse_locator_tab(quran_data, surah_names_list, surah_counts):
    """
    Create the Verse Locator tab interface with input and display components.

    Args:
        quran_data (pd.DataFrame): The Quran dataset.
        surah_names_list (list): List of formatted Surah names.

    Returns:
        gr.Tab: The configured Verse Locator tab.
    """
    with gr.Tab("Verse Locator") as tab:
        gr.Markdown("# Verse Locator")
        gr.Markdown("""
        <div class='tab-description'>
        Welcome to the Verse Locator! This tool allows you to:
        - Select a Surah from the dropdown menu
        - Enter a verse number to view the specific verse
        - Ensure fault tolerance for invalid verse numbers
        </div>
        """)

        surah_name_with_number = gr.Dropdown(
            label="Select a Surah",
            choices=surah_names_list,
            info="Choose a Surah to view its verses"
        )

        verse_number_input = gr.Number(
            label="Enter Verse Number",
            value=1,
            precision=0,
            elem_classes="verse-number-input"
        )

        verse_output = gr.Textbox(
            label="Verse",
            lines=5,
            visible=False,
            elem_classes="verse-output"
        )

        def update_verse_output(surah_name, verse_number):
            surah_number = int(surah_name.split('.')[0])
            verse_text = load_verse(surah_number, int(verse_number), quran_data, surah_counts)
            return gr.update(visible=True, value=verse_text)

        verse_number_input.submit(
            update_verse_output,
            inputs=[surah_name_with_number, verse_number_input],
            outputs=[verse_output]
        )

    return tab