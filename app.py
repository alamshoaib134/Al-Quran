import gradio as gr
import os

# ...existing code...

def load_surah(surah_name, surah_number):
    # Load the verses from a file or a predefined dictionary
    # For simplicity, let's assume we have a dictionary `surah_verses`
    surah_verses = {
        "Al-Kahf": ["Verse 1", "Verse 2", "Verse 3", "..."]
        # Add other surahs here
    }
    verses = surah_verses.get(surah_name, [])
    
    # Load the word cloud image path
    word_cloud_path = f"plots/{surah_name} word cloud.png"
    
    return verses, word_cloud_path

def display_surah(surah_name, surah_number):
    verses, word_cloud_path = load_surah(surah_name, surah_number)
    verses_text = "\n".join(verses)
    return verses_text, word_cloud_path

# Create a list of surah names and numbers
surah_names = ["Al-Kahf", "Another Surah"]  # Add all surah names here
surah_numbers = list(range(1, 115))  # Surah numbers from 1 to 114

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("Word Cloud"):
            # ...existing code for word cloud tab...
            pass
        
        with gr.TabItem("Surah Viewer"):
            surah_name = gr.Dropdown(label="Surah Name", choices=surah_names)
            surah_number = gr.Dropdown(label="Surah Number", choices=surah_numbers)
            verses_output = gr.Textbox(label="Verses", lines=20)
            word_cloud_output = gr.Image(label="Word Cloud")
            
            gr.Button("Load Surah").click(
                display_surah, 
                inputs=[surah_name, surah_number], 
                outputs=[verses_output, word_cloud_output]
            )

demo.launch()
