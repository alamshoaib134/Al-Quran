import gradio as gr
import os

def load_surah(surah_name_with_number, quran_data, arabic_data, urdu_data, hindi_data, bangla_data, tamil_data, malayalam_data):
    """
    Load verses and word cloud for a specific Surah in multiple languages.
    
    Args:
        surah_name_with_number (str): Format: "number. Surah Name"
        quran_data (pd.DataFrame): The English Quran dataset
        arabic_data (pd.DataFrame): The Arabic Quran dataset
        urdu_data (pd.DataFrame): The Urdu Quran dataset
        hindi_data (pd.DataFrame): The Hindi Quran dataset
        bangla_data (pd.DataFrame): The Bengali Quran dataset
        tamil_data (pd.DataFrame): The Tamil Quran dataset
        malayalam_data (pd.DataFrame): The Malayalam Quran dataset
        
    Returns:
        tuple: (dict of verses in different languages, word cloud image path)
    """
    surah_number = int(surah_name_with_number.split('.')[0])
    surah_name = surah_name_with_number.split('. ')[1]
    
    # Load verses in each language
    english_verses = quran_data[quran_data['Surah'] == surah_number]['Text'].tolist()
    arabic_verses = arabic_data[arabic_data['Surah'] == surah_number]['Text'].tolist()
    urdu_verses = urdu_data[urdu_data['Surah'] == surah_number]['Text'].tolist()
    hindi_verses = hindi_data[hindi_data['Surah'] == surah_number]['Text'].tolist()
    bangla_verses = bangla_data[bangla_data['Surah'] == surah_number]['Text'].tolist()
    tamil_verses = tamil_data[tamil_data['Surah'] == surah_number]['Text'].tolist()
    malayalam_verses = malayalam_data[malayalam_data['Surah'] == surah_number]['Text'].tolist()
    
    verses = {
        'english': english_verses,
        'arabic': arabic_verses,
        'urdu': urdu_verses,
        'hindi': hindi_verses,
        'bangla': bangla_verses,
        'tamil': tamil_verses,
        'malayalam': malayalam_verses
    }
    
    word_cloud_path = f"word_cloud/surah_{surah_number}_{surah_name}.png"
    return verses, word_cloud_path

def display_surah(surah_name_with_number, quran_data, arabic_data, urdu_data, hindi_data, bangla_data, tamil_data, malayalam_data):
    """
    Get the verses text in multiple languages and word cloud for display.
    
    Args:
        surah_name_with_number (str): Format: "number. Surah Name"
        quran_data (pd.DataFrame): The English Quran dataset
        arabic_data (pd.DataFrame): The Arabic Quran dataset
        urdu_data (pd.DataFrame): The Urdu Quran dataset
        hindi_data (pd.DataFrame): The Hindi Quran dataset
        bangla_data (pd.DataFrame): The Bengali Quran dataset
        tamil_data (pd.DataFrame): The Tamil Quran dataset
        malayalam_data (pd.DataFrame): The Malayalam Quran dataset
        
    Returns:
        tuple: (dict of verses text, word cloud image path)
    """
    verses, word_cloud_path = load_surah(surah_name_with_number, quran_data, arabic_data, urdu_data, hindi_data,
                                       bangla_data, tamil_data, malayalam_data)
    
    # Add verse numbers and join verses for each language
    verses_text = {}
    max_verses = max(len(verses[lang]) for lang in verses.keys())
    
    for lang in ['english', 'arabic', 'urdu', 'hindi', 'bangla', 'tamil', 'malayalam']:
        numbered_verses = []
        for i, verse in enumerate(verses[lang][:max_verses], 1):
            if lang == 'arabic':
                numbered_verses.append(f"{verse} [{i}]")
            elif lang in ['urdu', 'hindi', 'bangla', 'tamil', 'malayalam']:
                numbered_verses.append(f"[{i}] {verse}")
            else:  # english
                numbered_verses.append(f"[{i}] {verse}")
        verses_text[lang] = "\n\n".join(numbered_verses)
    
    return verses_text, word_cloud_path

def create_surah_tab(quran_data, arabic_data, urdu_data, hindi_data, bangla_data, tamil_data, malayalam_data, surah_names_list):
    """
    Create the Surah tab interface with multilingual display components.
    
    Args:
        quran_data (pd.DataFrame): The English Quran dataset
        arabic_data (pd.DataFrame): The Arabic Quran dataset
        urdu_data (pd.DataFrame): The Urdu Quran dataset
        hindi_data (pd.DataFrame): The Hindi Quran dataset
        bangla_data (pd.DataFrame): The Bengali Quran dataset
        tamil_data (pd.DataFrame): The Tamil Quran dataset
        malayalam_data (pd.DataFrame): The Malayalam Quran dataset
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
        - View translations in multiple languages simultaneously
        - See a visual word cloud representation of the Surah
        - Compare translations side by side
        
        Select a Surah and choose your preferred languages to begin exploring.
        </div>
        """)
        
        with gr.Row():
            surah_name_with_number = gr.Dropdown(
                label="Select a Surah",
                choices=surah_names_list,
                info="Choose a Surah to view its verses and word cloud"
            )
            
            languages = gr.Dropdown(
                choices=["English", "Arabic", "Urdu", "Hindi", "Bengali", "Tamil", "Malayalam"],
                value=["English"],
                multiselect=True,
                label="Select Languages",
                info="Choose one or more languages to display (English will be used if none selected)"
            )

        outputs_dict = {
            "English": lambda: gr.Textbox(
                label="English",
                lines=18,
                visible=False,
                elem_classes=["verses-output", "english-text"],
                show_label=True,
                container=True
            ),
            "Arabic": lambda: gr.Textbox(
                label="Arabic",
                lines=18,
                visible=False,
                elem_classes=["verses-output", "arabic-text"],
                rtl=True,
                show_label=True,
                container=True
            ),
            "Urdu": lambda: gr.Textbox(
                label="Urdu",
                lines=18,
                visible=False,
                elem_classes=["verses-output", "urdu-text"],
                show_label=True,
                container=True
            ),
            "Hindi": lambda: gr.Textbox(
                label="Hindi",
                lines=18,
                visible=False,
                elem_classes=["verses-output", "hindi-text"],
                show_label=True,
                container=True
            ),
            "Bengali": lambda: gr.Textbox(
                label="Bengali",
                lines=18,
                visible=False,
                elem_classes=["verses-output", "bangla-text"],
                show_label=True,
                container=True
            ),
            "Tamil": lambda: gr.Textbox(
                label="Tamil",
                lines=18,
                visible=False,
                elem_classes=["verses-output", "tamil-text"],
                show_label=True,
                container=True
            ),
            "Malayalam": lambda: gr.Textbox(
                label="Malayalam",
                lines=18,
                visible=False,
                elem_classes=["verses-output", "malayalam-text"],
                show_label=True,
                container=True
            )
        }
        
        # Define all supported languages
        ALL_LANGUAGES = ["English", "Arabic", "Urdu", "Hindi", "Bengali", "Tamil", "Malayalam"]
        
        # Create output components dynamically
        output_components = {}
        output_columns = {}
        with gr.Row() as output_row:
            for lang in ALL_LANGUAGES:
                with gr.Column(visible=lang == "English") as col:
                    output_components[lang] = outputs_dict[lang]()
                    output_columns[lang] = col
        
        # Add word cloud output after the language outputs
        word_cloud_output = gr.Image(
            label="Word Cloud Visualization",
            visible=False,
            elem_classes="word-cloud-output"
        )
        
        def update_visibility_and_load_surah(surah_name, selected_langs):
            if not surah_name:  # No surah selected yet
                # Each language component needs two updates: one for content, one for column
                all_updates = []
                for _ in ALL_LANGUAGES:
                    all_updates.extend([
                        gr.update(value="", visible=False),  # Textbox update
                        gr.update(visible=False)  # Column update
                    ])
                return all_updates + [gr.update(visible=False)]  # Word cloud update
            
            # Ensure at least English is selected
            selected_langs = selected_langs or ["English"]
            
            verses_text, word_cloud_path = display_surah(
                surah_name, quran_data, arabic_data, urdu_data, hindi_data,
                bangla_data, tamil_data, malayalam_data
            )
            
            # Calculate scale for visible columns
            num_visible = len(selected_langs)
            scale_value = int(12 / num_visible) if num_visible > 0 else 12
            
            # Create updates for all languages
            all_updates = []
            
            for lang in ALL_LANGUAGES:
                lang_map = {"Bengali": "bangla"}.get(lang, lang.lower())
                is_selected = lang in selected_langs
                
                # Add updates for both textbox and column
                all_updates.extend([
                    # Textbox update
                    gr.update(
                        value=verses_text[lang_map] if is_selected else "",
                        visible=is_selected
                    ),
                    # Column update
                    gr.update(
                        visible=is_selected,
                        scale=scale_value if is_selected else 0
                    )
                ])
            
            # Add word cloud update
            all_updates.append(gr.update(visible=True, value=word_cloud_path))
            return all_updates

        # Connect both dropdown changes to the update function
        for trigger in [surah_name_with_number, languages]:
            trigger.change(
                update_visibility_and_load_surah,
                inputs=[surah_name_with_number, languages],
                outputs=[
                    item for lang in ALL_LANGUAGES for item in [
                        output_components[lang],
                        output_columns[lang]
                    ]
                ] + [word_cloud_output]
            )
    
    return tab