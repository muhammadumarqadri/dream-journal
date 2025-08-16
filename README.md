# 🌙 Dream Journal Analyzer

A sophisticated AI-powered dream tracking and analysis application built with Streamlit. Track your dreams, analyze patterns, and gain insights into your subconscious mind through interactive visualizations and intelligent pattern recognition.

## ✨ Features

### Core Functionality
- **Dream Entry System**: Comprehensive dream logging with metadata tracking
- **Emotion Analysis**: Track and analyze emotional patterns in your dreams
- **AI-Powered Sentiment Analysis**: Automatic sentiment detection using TextBlob
- **Pattern Recognition**: Identify recurring themes, emotions, and sleep quality trends
- **Interactive Visualizations**: Dynamic charts and word clouds
- **Smart Search**: Full-text search across titles, descriptions, and tags
- **Data Export**: Export your analysis and insights

### Advanced Analytics
- **Sleep Quality Tracking**: Monitor sleep quality trends over time
- **Lucid Dream Statistics**: Track your lucid dreaming frequency and patterns
- **Emotional Timeline**: Visualize emotional patterns across your dream history
- **Word Cloud Generation**: See the most common themes in your dreams
- **Insight Generation**: AI-powered insights about your dream patterns
- **Statistical Analysis**: Comprehensive statistics about your dreaming patterns

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Start
1. **Clone or download the application**
   ```bash
   # If using git
   git clone <repository-url>
   cd dream-journal-analyzer
   
   # Or download and extract the files
   ```

2. **Install required dependencies**
   ```bash
   pip install streamlit matplotlib pandas textblob wordcloud
   ```

3. **Run the application**
   ```bash
   streamlit run dream_journal_streamlit.py
   ```

4. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:8501`
   - Start tracking your dreams!

### Alternative Installation
You can also install dependencies one by one:
```bash
pip install streamlit
pip install matplotlib
pip install pandas
pip install textblob
pip install wordcloud
```

## 📱 How to Use

### 1. New Dream Entry
- Navigate to the "New Dream Entry" tab
- Fill in your dream details:
  - **Title**: Give your dream a memorable title
  - **Description**: Write a detailed description of your dream
  - **Emotion**: Select the primary emotion you felt
  - **Lucid Dream**: Check if you were aware you were dreaming
  - **Tags**: Add comma-separated tags for themes or elements
  - **Sleep Quality**: Rate your sleep quality from 1-10
- Click "Save Dream" to store your entry

### 2. Dream Analysis
- View comprehensive statistics about your dreams
- See emotional patterns and sentiment analysis
- Review common themes and frequent words
- Get AI-powered insights about your dream patterns
- Export your analysis as a text file

### 3. Visualizations
Choose from three interactive visualizations:
- **Emotion Timeline**: See how your dream emotions change over time
- **Tag Cloud**: Visual representation of your most common dream themes
- **Sleep Quality Chart**: Track your sleep quality trends with average line

### 4. Search Dreams
- Use the search function to find specific dreams
- Search across titles, descriptions, and tags
- View all dreams in an organized, expandable format
- Filter and browse your entire dream collection

## 📊 Data Storage

- Dreams are automatically saved to `dreams.json` in the application directory
- Data persists between sessions
- Each dream entry includes:
  - Unique ID and timestamp
  - Title and description
  - Emotional and sentiment data
  - Sleep quality metrics
  - Tags and lucidity status
  - AI-analyzed sentiment scores

## 🎨 Features Deep Dive

### AI-Powered Sentiment Analysis
The application uses TextBlob to analyze the sentiment of your dream descriptions:
- **Positive**: Dreams with uplifting or pleasant content
- **Negative**: Dreams with concerning or unpleasant themes
- **Neutral**: Balanced or emotionally neutral dreams

### Smart Insights Generation
The system provides personalized insights based on your data:
- Lucid dreaming frequency analysis
- Sleep quality recommendations
- Emotional pattern recognition
- Trend identification over time

### Interactive Visualizations
- **Dark Theme**: Professional dark interface for comfortable viewing
- **Color-Coded Emotions**: Each emotion has its own color in charts
- **Responsive Charts**: Interactive matplotlib visualizations
- **Word Clouds**: Beautiful visual representation of dream themes

## 🔧 Customization

### Adding New Emotions
To add new emotion options, modify the `emotions` list in the New Dream Entry section:
```python
emotions = ['', 'Happy', 'Scared', 'Confused', 'Excited', 'Sad', 'Anxious', 
           'Peaceful', 'Angry', 'Curious', 'Nostalgic', 'Your_New_Emotion']
```

### Modifying Color Schemes
Update the `emotion_colors` dictionary in the visualization methods to change chart colors:
```python
emotion_colors = {
    'Happy': 'gold', 
    'Scared': 'red', 
    # Add your custom colors here
}
```

## 📈 Data Analysis Capabilities

### Statistical Metrics
- Total dreams recorded
- Lucid dream percentage
- Average sleep quality
- Most common emotions
- Sentiment distribution
- Tag frequency analysis
- Word frequency in descriptions

### Pattern Recognition
- Emotional trends over time
- Sleep quality correlations
- Recurring themes identification
- Seasonal pattern detection (with enough data)

## 🔒 Privacy & Security

- **Local Storage**: All data is stored locally on your device
- **No Cloud Sync**: Your dreams stay private and secure
- **No Data Collection**: The application doesn't collect or transmit personal data
- **Export Control**: You control when and how to export your data

## 🛠️ Troubleshooting

### Common Issues

**ModuleNotFoundError**
```bash
# Install missing packages
pip install [missing_package_name]
```

**Port Already in Use**
```bash
# Run on a different port
streamlit run dream_journal_streamlit.py --server.port 8502
```

**Charts Not Displaying**
- Ensure matplotlib is properly installed
- Check that you have dreams recorded for visualization

**File Permission Errors**
- Ensure write permissions in the application directory
- Run from a directory where you have full permissions

### Performance Tips
- For better performance with large datasets (500+ dreams), consider:
  - Limiting visualization date ranges
  - Using more specific search terms
  - Regularly exporting and archiving old data

## 🤝 Contributing

### Ways to Contribute
- Report bugs and issues
- Suggest new features
- Improve documentation
- Add new visualization types
- Enhance the AI analysis capabilities

### Feature Ideas
- Dream categories and classification
- Export to different formats (PDF, CSV)
- Dream sharing capabilities
- Advanced statistical analysis
- Integration with sleep tracking devices
- Mood correlation analysis

## 📚 Technical Details

### Architecture
- **Frontend**: Streamlit web interface
- **Backend**: Python with pandas for data manipulation
- **Visualization**: Matplotlib and WordCloud
- **NLP**: TextBlob for sentiment analysis
- **Storage**: JSON file-based persistence

### Dependencies
- `streamlit>=1.28.0`: Web application framework
- `matplotlib>=3.5.0`: Plotting and visualization
- `pandas>=1.3.0`: Data manipulation and analysis
- `textblob>=0.17.0`: Natural language processing
- `wordcloud>=1.8.0`: Word cloud generation

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (responsive design)

## 🎯 Roadmap

### Upcoming Features
- [ ] Dream category classification
- [ ] Advanced statistical models
- [ ] Correlation analysis between sleep and dreams
- [ ] Dream journal templates
- [ ] Multi-user support
- [ ] Data visualization enhancements
- [ ] Mobile app version
- [ ] Cloud synchronization (optional)

### Version History
- **v1.0**: Initial Streamlit release with full feature parity
- Core dream entry and analysis functionality
- Interactive visualizations
- Search and export capabilities

## 📞 Support

### Getting Help
- Check the troubleshooting section above
- Review the installation steps
- Ensure all dependencies are properly installed
- Verify Python version compatibility

### Feedback
Your feedback helps improve the Dream Journal Analyzer! Share your experience, suggestions, and feature requests.

---

**Happy Dream Journaling!** 🌟

Start your journey into dream analysis today and unlock the patterns hidden in your subconscious mind.
