import pandas as pd
import matplotlib.pyplot as plt
from base64 import b64encode
import io

def load_data():
    """Load and preprocess Quran dataset with surah names"""
    quran_english_with_surah = pd.read_csv('datasets/en.yusufali.csv')
    surah_names = pd.read_csv('datasets/surah_names_english.csv', names=['Surah', 'Surah Name'])
    surah_names["Surah Name"] = surah_names["Surah Name"].str[1:]
    quran_english_with_surah = quran_english_with_surah.merge(surah_names, on='Surah')
    quran_english_with_surah.index = pd.RangeIndex(start=1, stop=len(quran_english_with_surah) + 1)
    return quran_english_with_surah, surah_names

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