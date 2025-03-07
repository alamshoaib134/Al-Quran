# Al-Quran Analysis and Interactive Application

This repository contains an exploratory data analysis of the Quran's English translations and an interactive Gradio web application for exploring Quranic verses.

## Dataset Files

- `en.yusufali.csv` - Yusuf Ali's English translation of the Quran
- `English.csv` - English translation dataset
- `surah_names_english.csv` - Names of Surahs (chapters) in English
![Descriptive Statistics of Ayah Count per Surah](https://github.com/user-attachments/assets/d2b31335-abd4-4349-836c-c29f80979f01)
![Uploading Quran Word Cloud.png…]()

## Project Components

- `al-quran-english-exploratory-data-analysis.ipynb` - Jupyter notebook containing EDA of the Quran translations
- `al_quran_gradio.py` - Core functionality for the Quran exploration application
- `gradio_app.py` - Gradio web interface implementation

## Setup and Installation

1. Clone this repository
2. Install the required dependencies:
```sh
pip install gradio pandas numpy
```

## Usage

To run the Gradio web application:

```sh
python gradio_app.py
```

The application will start locally and provide a URL to access the interface in your web browser.

## Data Analysis

The exploratory data analysis notebook (`al-quran-english-exploratory-data-analysis.ipynb`) examines patterns and insights from the Quranic translations. Open it in Jupyter Notebook or Jupyter Lab to view the analysis.

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

This project is available under the MIT License.
