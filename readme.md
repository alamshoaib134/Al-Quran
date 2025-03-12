# Quran Explorer Application

A user-friendly application for exploring the Holy Quran through its English translation, built with Python and Gradio.

## Features

- **Keyword Search**: Search for specific words or phrases across the entire Quran
- **Statistical Analysis**: View visualizations and statistics about Quran's structure
- **Surah Explorer**: Read complete Surahs with word cloud visualizations

## Project Structure

```
.
├── datasets/               # Dataset files
│   ├── en.yusufali.csv    # English translation
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
- Application development: [Your Team/Organization]