import pandas as pd
import matplotlib.pyplot as plt
from base64 import b64encode
import io

def load_data():
    """Load and preprocess Quran datasets with translations"""
    # Load English translation and Surah names
    quran_english_with_surah = pd.read_csv('datasets/en.yusufali.csv')
    surah_names = pd.read_csv('datasets/surah_names_english.csv', names=['Surah', 'Surah Name'])
    surah_names["Surah Name"] = surah_names["Surah Name"].str[1:]
    
    # Load multilingual datasets with proper data types
    quran_arabic = pd.read_csv('datasets/Arabic-Original.csv',
                               names=['Surah', 'Verse', 'Text'],
                               encoding='utf-8-sig',
                               sep='|',
                               dtype={'Surah': int, 'Verse': int, 'Text': str})
    
    quran_urdu = pd.read_csv('datasets/Urdu.csv',
                             names=['Surah', 'Verse', 'Text'],
                             encoding='utf-8-sig',
                             sep='|',
                             dtype={'Surah': int, 'Verse': int, 'Text': str})
    
    # Load Hindi text file using the same format, with error handling
    try:
        quran_hindi = pd.read_csv('datasets/hindi.txt',
                                 names=['Surah', 'Verse', 'Text'],
                                 encoding='utf-8-sig',
                                 sep='|',
                                 comment='#',  # Skip lines starting with #
                                 skip_blank_lines=True,
                                 dtype={'Surah': str, 'Verse': str, 'Text': str})  # Load as strings first
        
        # Convert Surah and Verse to integers after loading
        quran_hindi['Surah'] = pd.to_numeric(quran_hindi['Surah'], errors='coerce')
        quran_hindi['Verse'] = pd.to_numeric(quran_hindi['Verse'], errors='coerce')
        
        # Remove any rows with invalid data
        quran_hindi = quran_hindi.dropna(subset=['Surah', 'Verse'])
        quran_hindi['Surah'] = quran_hindi['Surah'].astype(int)
        quran_hindi['Verse'] = quran_hindi['Verse'].astype(int)
    except Exception as e:
        print(f"Error loading Hindi dataset: {e}")
        # Create empty DataFrame with same structure if loading fails
        quran_hindi = pd.DataFrame(columns=['Surah', 'Verse', 'Text'])
    
    # Merge English translation with Surah names
    quran_english_with_surah = quran_english_with_surah.merge(surah_names, on='Surah')
    quran_english_with_surah.index = pd.RangeIndex(start=1, stop=len(quran_english_with_surah) + 1)
    
    return quran_english_with_surah, quran_arabic, quran_urdu, quran_hindi, surah_names

def plt_to_html(plt):
    """Convert matplotlib plot to HTML img tag"""
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = b64encode(buf.read()).decode('utf-8')
    plt.close()
    return f'<img src="data:image/png;base64,{img_str}"/>'

def get_surah_names_list(surah_names):
    """Create a formatted list of surah names with numbers"""
    return [f"{row['Surah']}. {row['Surah Name']}" for _, row in surah_names.iterrows()]

def load_css():
    """Load CSS styles from file"""
    with open('src/styles/styles.css', 'r') as f:
        return f.read()