import gradio as gr
import time
import re
from utils.transcript import extract_youtube_url, get_transcript_from_url
from utils.llm import detect_intent, detect_language, process_with_gemini
import config

def get_css():
    """Reads the CSS file and returns its content as a string."""
    try:
        with open("ui/styles.css", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("Warning: ui/styles.css not found. UI will have default styling.")
        return ""

def assistant_process_stream(request, url):
    """
    Orchestrates the backend process and yields status updates.
    Accepts request and url as separate arguments.
    """
    if not config.GEMINI_API_KEY:
        yield ("<p style='color: red;'>Error: Gemini API key not found. Please set it in your .env file.</p>", "")
        return

    # Combine request and url for intent detection
    user_message = (request or "") + " " + (url or "")
    url_extracted = extract_youtube_url(user_message)
    if not url_extracted:
        yield ("<p style='color: red;'>Error: Please include a valid YouTube URL.</p>", "")
        return

    # 2. Yield status while fetching transcript
    yield ("<div class='loader'></div> Fetching transcript from YouTube...", "")
    transcript = get_transcript_from_url(url_extracted)
    if not transcript:
        yield ("<p style='color: red;'>Error: Could not retrieve transcript. The video may not have one available.</p>", "")
        return

    # 3. Yield status while processing with AI
    yield ("<div class='loader'></div> Analyzing request and processing with Gemini...", "")
    try:
        intent = detect_intent(user_message)
        language = None
        if intent == 'translate':
            language = detect_language(user_message)
        
        # 4. Get final result from LLM
        final_result = process_with_gemini(transcript, user_message, intent, language)
        
        # 5. Yield final result and hide status
        yield ("", final_result)
    except Exception as e:
        yield (f"<p style='color: red;'>An unexpected error occurred: {e}</p>", "")

def create_interface():
    """Creates and returns the enhanced Gradio Blocks interface."""
    
    # --- GRADIO BLOCKS LAYOUT ---
    # The 'head' parameter is used to inject custom HTML, including script tags, into the app's head.
    with gr.Blocks(
        css=get_css(), 
        title="ToolTube - YouTube Assistant",
        head='<script src="file=ui/scripts.js"></script>'
    ) as demo:
        gr.HTML(
            value="""<style>.loader{border: 4px solid #f3f3f3; border-top: 4px solid var(--yt-red); border-radius: 50%; width: 20px; height: 20px; animation: spin 1s linear infinite; display: inline-block; margin-right: 10px; vertical-align: middle;} @keyframes spin {0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }</style>""",
            visible=False
        )

        # --- Header ---
        with gr.Row(elem_id="header-container"):
            gr.HTML("""
                <h1 id="logo"><span class="tool">Tool</span><span class="tube">Tube</span></h1>
                <p id="description">Your intelligent assistant for YouTube. Get summaries, translations, or answers about any video in seconds.</p>
            """)
        
        # --- UI Sections ---
        with gr.Column(elem_id="content-wrapper"):
            
            with gr.Group(elem_classes=["card"]):
                gr.Markdown("<h2 class='card-header'>1. Provide Your Request</h2>")
                with gr.Row():
                    request_box = gr.Textbox(lines=3, placeholder="e.g., 'Summarize this video'", label=None, elem_id="request-box")
                    url_box = gr.Textbox(lines=3, placeholder="e.g., https://www.youtube.com/watch?v=...", label=None, elem_id="url-box")

            submit_btn = gr.Button("Process Request", elem_id="submit-button")
            status_html = gr.HTML("", elem_id="status-area")

            with gr.Group(elem_classes=["card"]):
                gr.Markdown("<h2 class='card-header'>2. Assistant Response</h2>")
                output_box = gr.Textbox(lines=12, interactive=False, label=None, elem_id="output-box")

        reset_btn = gr.Button("🔄", elem_id="reset-button")

        # --- Event Handling Logic ---
        submit_btn.click(
            fn=assistant_process_stream,
            inputs=[request_box, url_box],
            outputs=[status_html, output_box]
        )

        def clear_all():
            return "", "", "", ""
        
        reset_btn.click(
            fn=clear_all,
            inputs=None,
            outputs=[request_box, url_box, output_box, status_html]
        )

    return demo