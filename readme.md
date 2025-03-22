# Al-Quran Repository
A user-friendly application for exploring the Holy Quran through its English translation, built with Python and Gradio.


## Features

- **Keyword Search**: Search for specific words or phrases across the entire Quran
- **Statistical Analysis**: View visualizations and statistics about Quran's structure
- **Multilingual Surah Explorer**:
  - Read complete Surahs in Arabic, Urdu, and English
  - Side-by-side translation comparison
  - Word cloud visualizations
  - RTL support for Arabic text

### 1. Quranic Analysis (Jupyter Notebooks)
A collection of interactive notebooks providing statistical insights about the Quran:
- Word frequency distributions
- Verse length analysis
- Surah-wise statistics
- Pattern analysis
- Visualization of Quranic data
![Quran Word Cloud](https://github.com/user-attachments/assets/f4cb7157-fcda-4e9a-b6fb-6d9d1aaeca29)
![Descriptive Statistics of Ayah Count per Surah](https://github.com/user-attachments/assets/bce97fb9-15fe-4e73-ab78-bf7e8ce4e3e4)

### 2. Verse Search Interface (Gradio App)
An intuitive web interface for searching Quranic verses:
- Search by keywords
- Find specific verses and their translations
- Get verse context and metadata
- User-friendly interface powered by Gradio
<img width="2056" alt="Screenshot 2025-03-08 at 3 53 52 AM" src="https://github.com/user-attachments/assets/7903305f-5b01-4866-8541-ef6a73b887e8" />

<img width="2056" alt="Screenshot 2025-03-08 at 3 54 09 AM" src="https://github.com/user-attachments/assets/ea1732e7-656b-43fe-9eb5-59ed98b3a3ca" />



## Project Structure

```
.
├── datasets/               # Dataset files
│   ├── en.yusufali.csv    # English translation
│   ├── Arabic-Original.csv # Original Arabic text
│   ├── Urdu.csv           # Urdu translation
│   └── surah_names_english.csv
├── src/                   # Source code
│   ├── components/        # Modular components
│   │   ├── search_tab.py  # Search functionality
│   │   ├── statistics_tab.py # Statistics and visualizations
│   │   ├── surah_tab.py   # Surah display
│   │   └── utils.py       # Shared utilities
│   ├── styles/           # Styling
│   │   └── styles.css     # CSS styles
│   └── gradio_app.py     # Main application
└── word_cloud/           # Word cloud images for each Surah
```

## Dependencies

- Python 3.7+
- gradio
- pandas
- matplotlib
- seaborn
- re

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install gradio pandas matplotlib seaborn
```

## Running the Application

Navigate to the project directory and run:

```bash
python src/gradio_app.py
```

The application will be available at `http://localhost:7860` by default.

## Contributing

### Adding New Features

1. Create new components in the `src/components/` directory
2. Update styles in `src/styles/styles.css`
3. Import and integrate components in `src/gradio_app.py`

### Code Structure

- Each tab's functionality is contained in a separate module
- Shared utilities are in `utils.py`
- CSS styling is centralized in `styles.css`

### Guidelines

- Follow the existing code structure
- Add appropriate documentation
- Test new features thoroughly
- Update README.md when adding new features

## License

Open source under MIT License

## Credits

- Quran translation: Yusuf Ali
- Application development: alamshoaib134@gmail.com
