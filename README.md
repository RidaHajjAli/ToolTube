# ToolTube

ToolTube is a simple intelligent YouTube assistant that helps the user process video content through an interactive web interface. Get summaries, translations, sentiment analysis, or ask questions about any YouTube video with available transcripts.

## Features

- **Video Transcript Processing**: Automatically fetches transcripts from YouTube videos
- **Multiple Processing Options**:
  - Summarize video content
  - Translate transcripts to different languages
  - Analyze sentiment
  - Ask specific questions about the video content
- **User-Friendly Interface**: Clean, responsive web interface powered by Gradio

## Requirements

- Python 3.x
- Required packages (install via pip):
  - gradio>=5.29.0
  - google-generativeai>=0.8.5
  - python-dotenv>=1.1.0
  - youtube-transcript-api>=1.1.0

## Setup

1. Clone the repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

1. Run the application:
   ```
   python app.py
   ```
2. Open your web browser and navigate to the provided local URL
3. Enter your request (e.g., "Summarize this video") and paste a YouTube URL
4. Click "Process Request" to get your results

## Project Structure

```
.
├── app.py              # Main application entry point
├── config.py           # Configuration and environment variables
├── ui/                 # User interface components
│   ├── interface.py    # Gradio interface definition
│   ├── scripts.js      # Frontend JavaScript
│   └── styles.css      # Custom styling
└── utils/             # Utility functions
    ├── llm.py         # AI model integration
    └── transcript.py  # YouTube transcript handling
```