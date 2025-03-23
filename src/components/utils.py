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
    
    def load_translation(file_path, name):
        """Helper function to load translation datasets with error handling"""
        try:
            df = pd.read_csv(file_path,
                           names=['Surah', 'Verse', 'Text'],
                           encoding='utf-8-sig',
                           sep='|',
                           comment='#',
                           skip_blank_lines=True,
                           dtype={'Surah': str, 'Verse': str, 'Text': str})
            
            # Convert Surah and Verse to integers
            df['Surah'] = pd.to_numeric(df['Surah'], errors='coerce')
            df['Verse'] = pd.to_numeric(df['Verse'], errors='coerce')
            
            # Remove any rows with invalid data
            df = df.dropna(subset=['Surah', 'Verse'])
            df['Surah'] = df['Surah'].astype(int)
            df['Verse'] = df['Verse'].astype(int)
            return df
        except Exception as e:
            print(f"Error loading {name} dataset: {e}")
            return pd.DataFrame(columns=['Surah', 'Verse', 'Text'])

    # Load translations using helper function
    quran_hindi = load_translation('datasets/hindi.txt', 'Hindi')
    quran_bangla = load_translation('datasets/Bangla.csv', 'Bengali')
    quran_tamil = load_translation('datasets/Tamil.csv', 'Tamil')
    quran_malayalam = load_translation('datasets/Malayalam.csv', 'Malayalam')
    
    # Merge English translation with Surah names
    quran_english_with_surah = quran_english_with_surah.merge(surah_names, on='Surah')
    quran_english_with_surah.index = pd.RangeIndex(start=1, stop=len(quran_english_with_surah) + 1)
    
    return (quran_english_with_surah, quran_arabic, quran_urdu, quran_hindi,
            quran_bangla, quran_tamil, quran_malayalam, surah_names)

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