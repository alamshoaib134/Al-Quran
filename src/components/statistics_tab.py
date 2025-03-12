import gradio as gr
import matplotlib.pyplot as plt
import seaborn as sns
from .utils import plt_to_html

def generate_plots_and_tables(quran_data):
    """
    Generate visualization plots and statistics tables for the Quran data.
    
    Args:
        quran_data (pd.DataFrame): The Quran dataset
        
    Returns:
        str: HTML formatted plots and tables
    """
    # Plot 1: Number of verses in each chapter
    plt.figure(figsize=(30, 10))
    sns.set_style('whitegrid')
    value_counts = quran_data['Surah Name'].value_counts()
    ax = sns.barplot(
        x=value_counts.index,
        y=value_counts.values,
        hue=value_counts.index,
        palette='viridis',
        legend=False
    )
    
    # Add value labels on bars
    for container in ax.containers:
        ax.bar_label(container, size=10, padding=2)
    
    # Customize plot
    ax.set_title('Number of Verses in Each Chapter', fontweight='bold', fontsize=14)
    ax.set_ylabel('Number of Verses', fontweight='bold')
    ax.set_xlabel('Surah Name', fontweight='bold')
    plt.xticks(rotation=90)
    plt.tight_layout()
    
    # Convert plot to HTML
    plot1_html = plt_to_html(plt)
    
    # Generate statistics table
    surah_counts = quran_data['Surah Name'].value_counts().reset_index()
    surah_counts.columns = ['Surah Name', 'Ayah Count']
    table_html = surah_counts.to_html(
        index=False, 
        classes='table table-striped table-hover'
    )
    table_html = f'<div style="max-height: 300px; overflow-y: auto;">{table_html}</div>'
    
    return plot1_html + table_html

def create_statistics_tab(quran_data):
    """
    Create the statistics tab interface with description and visualizations.
    
    Args:
        quran_data (pd.DataFrame): The Quran dataset
        
    Returns:
        gr.Tab: The configured statistics tab
    """
    with gr.Tab("Statistics") as tab:
        gr.Markdown("# Quran Statistics")
        gr.Markdown("""
        <div class='tab-description'>
        This section provides statistical insights about the Quran:
        - Visual representation of verses distribution across chapters
        - Interactive bar chart showing the number of verses in each Surah
        - Detailed table with verse counts for each chapter
        - Color-coded visualization for easy comparison
        
        The statistics help understand the structure and composition of the Quran.
        </div>
        """)
        
        stats_output = gr.HTML(value=generate_plots_and_tables(quran_data))
    
    return tab