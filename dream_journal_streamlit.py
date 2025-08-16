"""
Personal Dream Journal with AI-Powered Insights
A sophisticated application that tracks dreams, analyzes patterns, and provides insights.

Features:
- Dream entry with emotion tracking
- Pattern analysis (themes, emotions, frequency)
- Data visualization with charts
- Dream statistics and insights
- Export functionality
- Search and filter capabilities

Required installations:
pip install streamlit matplotlib pandas textblob wordcloud
"""

import streamlit as st
import json
import datetime
from collections import Counter, defaultdict
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import re
import io


class DreamJournal:
    def __init__(self):
        # Initialize session state
        if 'dreams' not in st.session_state:
            st.session_state.dreams = self.load_dreams()
        
        self.dreams = st.session_state.dreams
        
    def load_dreams(self):
        """Load dreams from JSON file"""
        try:
            with open('dreams.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
            
    def save_dreams(self):
        """Save dreams to JSON file"""
        try:
            with open('dreams.json', 'w') as f:
                json.dump(self.dreams, f, indent=2)
            st.session_state.dreams = self.dreams
        except Exception as e:
            st.error(f"Failed to save dreams: {str(e)}")

    def analyze_sentiment(self, text):
        """Analyze sentiment of dream description using TextBlob"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            if polarity > 0.1:
                return 'positive'
            elif polarity < -0.1:
                return 'negative'
            else:
                return 'neutral'
        except:
            return 'neutral'

    def save_dream(self, title, description, emotion, lucid, tags, sleep_quality):
        """Save a new dream entry"""
        # Validate input
        if not title.strip():
            st.error("Please enter a dream title")
            return False
        
        if not description.strip():
            st.error("Please enter a dream description")
            return False
        
        # Create dream entry
        dream = {
            'id': len(self.dreams) + 1,
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'title': title.strip(),
            'description': description.strip(),
            'emotion': emotion,
            'lucid': lucid,
            'tags': [tag.strip() for tag in tags.split(',') if tag.strip()],
            'sleep_quality': int(sleep_quality),
            'sentiment': self.analyze_sentiment(description.strip())
        }
        
        # Add to dreams list
        self.dreams.append(dream)
        
        # Save to file
        self.save_dreams()
        
        st.success("Dream saved successfully!")
        return True

    def format_counter(self, counter_dict, indent=0):
        """Format a counter dictionary for display"""
        if not counter_dict:
            return "  None"
        
        formatted = []
        for item, count in counter_dict.items():
            formatted.append(f"{'  ' * indent}• {item}: {count}")
        return '\n'.join(formatted)
        
    def generate_insights(self):
        """Generate insights based on dream patterns"""
        if not self.dreams:
            return "Not enough data for insights."
            
        insights = []
        
        # Lucid dreaming insight
        lucid_percentage = sum(1 for dream in self.dreams if dream.get('lucid', False)) / len(self.dreams) * 100
        if lucid_percentage > 20:
            insights.append("• You have a high rate of lucid dreaming! This suggests good dream awareness.")
        elif lucid_percentage < 5:
            insights.append("• Consider practicing lucid dreaming techniques to increase awareness.")
            
        # Sleep quality insight
        avg_quality = sum(dream.get('sleep_quality', 0) for dream in self.dreams) / len(self.dreams)
        if avg_quality < 5:
            insights.append("• Your sleep quality could be improved. Consider sleep hygiene practices.")
        elif avg_quality > 7:
            insights.append("• You maintain good sleep quality! Keep up the healthy habits.")
            
        # Sentiment insight
        sentiments = [dream.get('sentiment', 'neutral') for dream in self.dreams]
        positive_ratio = sentiments.count('positive') / len(sentiments) * 100
        if positive_ratio > 60:
            insights.append("• Your dreams tend to be positive! This may reflect good mental wellbeing.")
        elif positive_ratio < 30:
            insights.append("• Consider activities that promote positive thoughts before bed.")
            
        return '\n'.join(insights) if insights else "Keep recording dreams to unlock more insights!"

    def get_analysis(self):
        """Get complete analysis of dreams"""
        if not self.dreams:
            return "No dreams recorded yet. Start by adding some dreams!"
            
        # Calculate statistics
        total_dreams = len(self.dreams)
        lucid_dreams = sum(1 for dream in self.dreams if dream.get('lucid', False))
        avg_sleep_quality = sum(dream.get('sleep_quality', 0) for dream in self.dreams) / total_dreams
        
        # Emotion analysis
        emotions = [dream.get('emotion', 'Unknown') for dream in self.dreams]
        emotion_counts = Counter(emotions)
        most_common_emotion = emotion_counts.most_common(1)[0] if emotion_counts else ('None', 0)
        
        # Sentiment analysis
        sentiments = [dream.get('sentiment', 'neutral') for dream in self.dreams]
        sentiment_counts = Counter(sentiments)
        
        # Tag analysis
        all_tags = []
        for dream in self.dreams:
            all_tags.extend(dream.get('tags', []))
        tag_counts = Counter(all_tags)
        common_tags = tag_counts.most_common(5)
        
        # Recent dreams analysis
        recent_dreams = sorted(self.dreams, key=lambda x: x.get('date', ''), reverse=True)[:5]
        
        # Word frequency analysis
        all_text = ' '.join([dream.get('description', '') for dream in self.dreams])
        words = re.findall(r'\b\w+\b', all_text.lower())
        common_words = Counter(words).most_common(10)
        
        # Build analysis text
        analysis = f"""
DREAM JOURNAL ANALYSIS
{'='*50}

BASIC STATISTICS:
• Total Dreams Recorded: {total_dreams}
• Lucid Dreams: {lucid_dreams} ({lucid_dreams/total_dreams*100:.1f}%)
• Average Sleep Quality: {avg_sleep_quality:.1f}/10

EMOTIONAL PATTERNS:
• Most Common Emotion: {most_common_emotion[0]} ({most_common_emotion[1]} times)
• Emotion Distribution:
{self.format_counter(emotion_counts, 2)}

SENTIMENT ANALYSIS:
• Positive Dreams: {sentiment_counts.get('positive', 0)}
• Negative Dreams: {sentiment_counts.get('negative', 0)}
• Neutral Dreams: {sentiment_counts.get('neutral', 0)}

COMMON THEMES (Tags):
{self.format_counter(dict(common_tags), 2) if common_tags else '  No tags found'}

FREQUENT WORDS IN DREAMS:
{self.format_counter(dict(common_words), 2)}

RECENT DREAM TITLES:
{chr(10).join([f"• {dream.get('title', 'Untitled')} ({dream.get('date', 'Unknown date')[:10]})" for dream in recent_dreams[:5]])}

INSIGHTS:
{self.generate_insights()}
        """
        
        return analysis

    def show_emotion_timeline(self):
        """Show emotion timeline chart"""
        if not self.dreams:
            st.info("No dreams to visualize yet!")
            return None
            
        # Prepare data
        dates = [datetime.datetime.strptime(dream['date'][:10], '%Y-%m-%d') for dream in self.dreams]
        emotions = [dream.get('emotion', 'Unknown') for dream in self.dreams]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#2c3e50')
        ax.set_facecolor('#34495e')
        
        # Color mapping for emotions
        emotion_colors = {
            'Happy': 'gold', 'Scared': 'red', 'Confused': 'orange', 
            'Excited': 'lime', 'Sad': 'blue', 'Anxious': 'purple',
            'Peaceful': 'lightblue', 'Angry': 'darkred', 'Curious': 'green',
            'Nostalgic': 'pink', 'Unknown': 'gray'
        }
        
        colors = [emotion_colors.get(emotion, 'gray') for emotion in emotions]
        
        # Create scatter plot
        ax.scatter(dates, emotions, c=colors, s=100, alpha=0.7)
        ax.set_xlabel('Date', color='white')
        ax.set_ylabel('Emotion', color='white')
        ax.set_title('Dream Emotions Over Time', color='white', fontsize=14, fontweight='bold')
        
        # Style the plot
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
        
    def show_word_cloud(self):
        """Show word cloud of dream tags and descriptions"""
        if not self.dreams:
            st.info("No dreams to visualize yet!")
            return None
            
        # Prepare text data
        all_text = []
        for dream in self.dreams:
            all_text.append(dream.get('title', ''))
            all_text.append(dream.get('description', ''))
            all_text.extend(dream.get('tags', []))
            
        text = ' '.join(all_text)
        
        if not text.strip():
            st.info("No text data available for word cloud!")
            return None
            
        # Create word cloud
        try:
            wordcloud = WordCloud(width=800, height=400, 
                                background_color='#2c3e50',
                                colormap='viridis',
                                max_words=100).generate(text)
            
            # Create figure
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor('#2c3e50')
            
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            ax.set_title('Dream Themes Word Cloud', color='white', 
                        fontsize=14, fontweight='bold', pad=20)
            
            plt.tight_layout()
            
            return fig
            
        except Exception as e:
            st.error(f"Could not generate word cloud: {str(e)}")
            return None
            
    def show_quality_chart(self):
        """Show sleep quality over time chart"""
        if not self.dreams:
            st.info("No dreams to visualize yet!")
            return None
            
        # Prepare data
        dates = [datetime.datetime.strptime(dream['date'][:10], '%Y-%m-%d') for dream in self.dreams]
        qualities = [dream.get('sleep_quality', 0) for dream in self.dreams]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#2c3e50')
        ax.set_facecolor('#34495e')
        
        # Create line plot
        ax.plot(dates, qualities, marker='o', linewidth=2, markersize=8, 
               color='cyan', markerfacecolor='orange')
        
        ax.set_xlabel('Date', color='white')
        ax.set_ylabel('Sleep Quality (1-10)', color='white')
        ax.set_title('Sleep Quality Over Time', color='white', 
                    fontsize=14, fontweight='bold')
        
        # Add average line
        avg_quality = sum(qualities) / len(qualities)
        ax.axhline(y=avg_quality, color='red', linestyle='--', alpha=0.7, 
                  label=f'Average: {avg_quality:.1f}')
        
        # Style the plot
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.legend(facecolor='#34495e', edgecolor='white', labelcolor='white')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig

    def search_dreams(self, query):
        """Search dreams based on query"""
        if not query:
            return []
            
        query = query.lower()
        results = []
        for dream in self.dreams:
            # Search in title, description, and tags
            if (query in dream.get('title', '').lower() or
                query in dream.get('description', '').lower() or
                any(query in tag.lower() for tag in dream.get('tags', []))):
                results.append(dream)
                
        return results

    def display_dreams(self, dreams, header="Dreams:"):
        """Display dreams in a formatted way"""
        if not dreams:
            st.write(f"**{header}**\n\nNo dreams found.")
        else:
            st.write(f"**{header}**\n")
            for i, dream in enumerate(dreams, 1):
                with st.expander(f"{i}. {dream.get('title', 'Untitled')} - {dream.get('date', 'Unknown')[:10]}"):
                    st.write(f"**Date:** {dream.get('date', 'Unknown')[:10]}")
                    st.write(f"**Emotion:** {dream.get('emotion', 'Unknown')}")
                    st.write(f"**Tags:** {', '.join(dream.get('tags', ['None']))}")
                    st.write(f"**Sleep Quality:** {dream.get('sleep_quality', 'Unknown')}/10")
                    st.write(f"**Lucid:** {'Yes' if dream.get('lucid', False) else 'No'}")
                    st.write(f"**Description:** {dream.get('description', '')}")

    def export_analysis(self):
        """Export analysis to a text file"""
        if not self.dreams:
            st.info("No dreams to export!")
            return None
            
        try:
            analysis_text = self.get_analysis()
            
            export_content = f"""DREAM JOURNAL ANALYSIS EXPORT
Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 60}

{analysis_text}"""
            
            return export_content
            
        except Exception as e:
            st.error(f"Failed to export analysis: {str(e)}")
            return None


def main():
    """Main function to run the Dream Journal application"""
    st.set_page_config(
        page_title="Dream Journal Analyzer",
        page_icon="🌙",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for dark theme similar to tkinter version
    st.markdown("""
    <style>
    .main {
        background-color: #2c3e50;
    }
    .stApp {
        background-color: #2c3e50;
    }
    .stTextInput > div > div > input {
        background-color: #34495e;
        color: white;
    }
    .stTextArea > div > div > textarea {
        background-color: #34495e;
        color: white;
    }
    .stSelectbox > div > div > select {
        background-color: #34495e;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🌙 Dream Journal Analyzer")
    
    # Initialize the dream journal
    dream_journal = DreamJournal()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    tab = st.sidebar.radio("Choose a section:", 
                          ["New Dream Entry", "Dream Analysis", "Visualizations", "Search Dreams"])
    
    if tab == "New Dream Entry":
        st.header("Dream Journal Entry")
        
        with st.form("dream_entry_form"):
            # Dream title
            title = st.text_input("Dream Title:", key="dream_title")
            
            # Dream description
            description = st.text_area("Dream Description:", height=200, key="dream_desc")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Emotion selection
                emotions = ['', 'Happy', 'Scared', 'Confused', 'Excited', 'Sad', 'Anxious', 
                           'Peaceful', 'Angry', 'Curious', 'Nostalgic']
                emotion = st.selectbox("Primary Emotion:", emotions, key="dream_emotion")
                
                # Lucidity checkbox
                lucid = st.checkbox("Lucid Dream", key="dream_lucid")
            
            with col2:
                # Tags
                tags = st.text_input("Tags (comma-separated):", key="dream_tags")
                
                # Sleep quality
                sleep_quality = st.slider("Sleep Quality (1-10):", 1, 10, 5, key="dream_quality")
            
            # Save button
            submitted = st.form_submit_button("Save Dream")
            
            if submitted:
                if dream_journal.save_dream(title, description, emotion, lucid, tags, sleep_quality):
                    st.balloons()
                    # Clear form by rerunning
                    st.experimental_rerun()
    
    elif tab == "Dream Analysis":
        st.header("Dream Pattern Analysis")
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("Refresh Analysis"):
                st.experimental_rerun()
            
            # Export analysis
            export_content = dream_journal.export_analysis()
            if export_content:
                st.download_button(
                    label="Export Analysis",
                    data=export_content,
                    file_name=f"dream_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        with col1:
            st.subheader("Dream Statistics")
            analysis = dream_journal.get_analysis()
            st.text(analysis)
    
    elif tab == "Visualizations":
        st.header("Dream Data Visualizations")
        
        viz_type = st.selectbox("Choose visualization:", 
                               ["Emotion Timeline", "Tag Cloud", "Sleep Quality Chart"])
        
        if viz_type == "Emotion Timeline":
            fig = dream_journal.show_emotion_timeline()
            if fig:
                st.pyplot(fig)
                
        elif viz_type == "Tag Cloud":
            fig = dream_journal.show_word_cloud()
            if fig:
                st.pyplot(fig)
                
        elif viz_type == "Sleep Quality Chart":
            fig = dream_journal.show_quality_chart()
            if fig:
                st.pyplot(fig)
    
    elif tab == "Search Dreams":
        st.header("Search & Browse Dreams")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_query = st.text_input("Search:", key="search_input")
        
        with col2:
            search_button = st.button("Search")
        
        with col3:
            show_all_button = st.button("Show All")
        
        if search_button and search_query:
            results = dream_journal.search_dreams(search_query)
            dream_journal.display_dreams(results, f"Search results for '{search_query}':")
        
        elif show_all_button:
            dream_journal.display_dreams(dream_journal.dreams, "All Dreams:")
        
        # Show all dreams by default when page loads
        elif 'search_performed' not in st.session_state:
            dream_journal.display_dreams(dream_journal.dreams, "All Dreams:")
            st.session_state.search_performed = True


if __name__ == "__main__":
    main()