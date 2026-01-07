import streamlit as st
import google.generativeai as genai
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import json
import os
import tempfile
from pathlib import Path
import yt_dlp
import time

# Page Configuration
st.set_page_config(
    page_title="Korewole Onire - Premium Content Repurposing",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Premium Branding
st.markdown("""
<style>
    /* Main Theme Colors */
    :root {
        --navy: #0A1929;
        --gold: #D4AF37;
        --light-navy: #1A2942;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #0A1929 0%, #1A2942 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        border: 2px solid #D4AF37;
        box-shadow: 0 8px 32px rgba(212, 175, 55, 0.2);
    }
    
    .main-title {
        color: #D4AF37;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        color: #ffffff;
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Card Styling */
    .content-card {
        background: #1A2942;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #D4AF37;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #F4D03F 100%);
        color: #0A1929;
        font-weight: 700;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(212, 175, 55, 0.4);
    }
    
    /* Input Styling */
    .stTextInput>div>div>input {
        background-color: #0A1929;
        color: white;
        border: 2px solid #D4AF37;
        border-radius: 8px;
    }
    
    /* File Uploader */
    .uploadedFile {
        background-color: #1A2942;
        border: 2px solid #D4AF37;
        border-radius: 8px;
    }
    
    /* Success/Info Messages */
    .stSuccess, .stInfo {
        background-color: #1A2942;
        color: white;
        border-left: 4px solid #D4AF37;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #1A2942;
        color: #D4AF37;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">✨ Korewole Onire ✨</h1>
    <p class="subtitle">Premium Content Repurposing Service</p>
</div>
""", unsafe_allow_html=True)

# Initialize Session State
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = None
if 'video_title' not in st.session_state:
    st.session_state.video_title = None

# API Configuration
def initialize_apis():
    """Initialize Google Gemini and Drive APIs"""
    try:
        # Gemini API
        gemini_key = os.getenv('GEMINI_API_KEY')
        if gemini_key:
            genai.configure(api_key=gemini_key)
        
        # Google Drive API
        drive_creds_json = os.getenv('GOOGLE_DRIVE_CREDENTIALS')
        if drive_creds_json:
            creds_dict = json.loads(drive_creds_json)
            credentials = service_account.Credentials.from_service_account_info(
                creds_dict,
                scopes=['https://www.googleapis.com/auth/drive.file']
            )
            drive_service = build('drive', 'v3', credentials=credentials)
            return drive_service
        return None
    except Exception as e:
        st.error(f"API Initialization Error: {str(e)}")
        return None

def download_youtube_video(url):
    """Download YouTube video and extract audio"""
    try:
        with st.spinner("📥 Downloading video from YouTube..."):
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': tempfile.gettempdir() + '/%(id)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }],
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_id = info['id']
                video_title = info['title']
                audio_file = os.path.join(tempfile.gettempdir(), f"{video_id}.mp3")
                
                return audio_file, video_title
    except Exception as e:
        st.error(f"YouTube Download Error: {str(e)}")
        return None, None

def transcribe_and_generate(video_path, video_title):
    """Transcribe video and generate content using Gemini"""
    try:
        with st.spinner("🤖 AI is analyzing your content..."):
            # Upload video to Gemini
            video_file = genai.upload_file(path=video_path)
            
            # Wait for processing
            while video_file.state.name == "PROCESSING":
                time.sleep(2)
                video_file = genai.get_file(video_file.name)
            
            if video_file.state.name == "FAILED":
                raise ValueError("Video processing failed")
            
            # Generate content
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Analyze this video titled "{video_title}" and create:
            
            1. A VIRAL LINKEDIN POST:
            - Start with an attention-grabbing hook
            - Use engaging storytelling
            - Include relevant emojis naturally
            - End with a call-to-action
            - Keep it between 150-250 words
            
            2. KEY TAKEAWAYS (5 points):
            - List 5 main insights from the video
            - Make each point actionable and clear
            - Use bullet points
            
            Format your response clearly with section headers.
            """
            
            response = model.generate_content([video_file, prompt])
            
            # Clean up
            genai.delete_file(video_file.name)
            
            return response.text
    
    except Exception as e:
        st.error(f"AI Generation Error: {str(e)}")
        return None

def export_to_drive(content, video_title, drive_service):
    """Export generated content to Google Drive"""
    try:
        with st.spinner("📤 Delivering to your Google Drive..."):
            # Create Google Doc content
            doc_content = f"""Korewole Onire - Content Repurposing
Video: {video_title}
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

{content}
"""
            
            # Create temporary text file
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8')
            temp_file.write(doc_content)
            temp_file.close()
            
            # Upload to Drive
            file_metadata = {
                'name': f'Korewole_Onire_{video_title[:50]}_{int(time.time())}.txt',
                'mimeType': 'text/plain'
            }
            
            media = MediaFileUpload(temp_file.name, mimetype='text/plain')
            
            file = drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()
            
            # Clean up
            os.unlink(temp_file.name)
            
            return file.get('webViewLink')
    
    except Exception as e:
        st.error(f"Google Drive Export Error: {str(e)}")
        return None

# Main Application Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📹 Input Your Content")
    
    input_method = st.radio(
        "Choose input method:",
        ["YouTube URL", "Upload Video File"],
        label_visibility="collapsed"
    )
    
    video_file_path = None
    video_title = None
    
    if input_method == "YouTube URL":
        youtube_url = st.text_input(
            "Enter YouTube URL:",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Paste a valid YouTube video URL"
        )
        
        if st.button("🚀 Process Video", use_container_width=True):
            if youtube_url:
                video_file_path, video_title = download_youtube_video(youtube_url)
            else:
                st.warning("Please enter a YouTube URL")
    
    else:
        uploaded_file = st.file_uploader(
            "Upload your video file",
            type=['mp4', 'mov', 'avi', 'mkv'],
            help="Maximum file size: 200MB"
        )
        
        if st.button("🚀 Process Video", use_container_width=True):
            if uploaded_file:
                if uploaded_file.size > 200 * 1024 * 1024:
                    st.error("File size exceeds 200MB limit")
                else:
                    # Save uploaded file
                    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix)
                    temp_video.write(uploaded_file.read())
                    temp_video.close()
                    
                    video_file_path = temp_video.name
                    video_title = uploaded_file.name
            else:
                st.warning("Please upload a video file")
    
    # Process video if available
    if video_file_path and video_title:
        st.session_state.video_title = video_title
        generated = transcribe_and_generate(video_file_path, video_title)
        
        if generated:
            st.session_state.generated_content = generated
            st.success("✅ Content generated successfully!")
            
            # Clean up temp file
            try:
                os.unlink(video_file_path)
            except:
                pass

with col2:
    st.markdown("### 📄 Generated Content")
    
    if st.session_state.generated_content:
        with st.expander("📝 View Generated Content", expanded=True):
            st.markdown(st.session_state.generated_content)
        
        # Google Drive Export Button
        st.markdown("---")
        if st.button("📁 Deliver to my Google Drive", use_container_width=True, type="primary"):
            drive_service = initialize_apis()
            
            if drive_service:
                drive_link = export_to_drive(
                    st.session_state.generated_content,
                    st.session_state.video_title,
                    drive_service
                )
                
                if drive_link:
                    st.success(f"✅ Successfully delivered to Google Drive!")
                    st.markdown(f"[🔗 Open in Google Drive]({drive_link})")
            else:
                st.error("Google Drive API not configured. Please set up credentials.")
        
        # Download button
        st.download_button(
            label="💾 Download as Text File",
            data=st.session_state.generated_content,
            file_name=f"korewole_onire_{int(time.time())}.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.info("👈 Process a video to see generated content here")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #D4AF37; padding: 1rem;'>
    <p><strong>Korewole Onire</strong> - Transforming Content into Engagement</p>
    <p style='font-size: 0.9rem; color: #ffffff;'>Powered by Google Gemini AI</p>
</div>
""", unsafe_allow_html=True)
