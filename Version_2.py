import streamlit as st
from datetime import datetime
import random
import base64
from pathlib import Path
import os
import mimetypes

# Function to load local images
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def verify_audio_file():
    audio_path = os.path.abspath("background_music.mp3")
    if os.path.exists(audio_path):
        file_size = os.path.getsize(audio_path)
        mime_type, _ = mimetypes.guess_type(audio_path)
        st.success(f"Audio file found: {audio_path}")
        st.info(f"File size: {file_size} bytes")
        st.info(f"MIME type: {mime_type}")
        
        # Try to open and read the file
        try:
            with open(audio_path, 'rb') as f:
                audio_bytes = f.read()
            st.success("Successfully read audio file")
            return audio_bytes
        except Exception as e:
            st.error(f"Error reading audio file: {str(e)}")
    else:
        st.error(f"Audio file not found: {audio_path}")
        st.info(f"Current working directory: {os.getcwd()}")
        st.info(f"Files in Assets directory: {os.listdir('Assets') if os.path.exists('Assets') else 'Assets directory not found'}")
    return None

# Function to display image
def display_image(image_path):
    st.image(image_path, use_column_width=True)

# Set page configuration
st.set_page_config(page_title="Endgame Countdown", layout="wide")

# Set background image
set_png_as_page_bg('taylor_swift_bg.jpeg')

# Verify and load audio file
audio_bytes = verify_audio_file()

# Display audio player if file is loaded successfully
if audio_bytes:
    st.audio(audio_bytes, format='audio/mp3')
else:
    st.error("Failed to load audio file")

# Custom CSS for styling and animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    body {
        font-family: 'Roboto', sans-serif;
    }
    .big-font {
        font-size: 40px !important;
        font-weight: bold;
        color: #FF69B4;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        animation: pulse 2s infinite;
    }
    .medium-font {
        font-size: 24px !important;
        font-weight: bold;
        color: #FF1493;
        text-align: center;
    }
    .word-button {
        background-color: #FFB6C1;
        color: #000;
        border: none;
        padding: 10px 20px;
        margin: 5px;
        border-radius: 20px;
        font-size: 18px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .word-button:hover {
        background-color: #FF69B4;
        transform: scale(1.1);
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    .floating-heart {
        position: fixed;
        font-size: 24px;
        animation: float 3s ease-in-out infinite;
    }
    </style>
    """, unsafe_allow_html=True)

# Floating hearts animation
def create_floating_hearts():
    hearts = "❤️💖💕💗💓"
    for i in range(10):
        left = random.randint(0, 100)
        top = random.randint(0, 100)
        delay = random.random() * 3
        st.markdown(f"""
            <div class="floating-heart" style="left: {left}vw; top: {top}vh; animation-delay: {delay}s;">
                {random.choice(hearts)}
            </div>
        """, unsafe_allow_html=True)

create_floating_hearts()

# Header
st.markdown('<p class="big-font">I now know we are endgame</p>', unsafe_allow_html=True)

# Countdown function
def update_countdown():
    current_date = datetime.now()
    engagement_date = datetime(2024, 9, 5)
    wedding_date = datetime(2024, 11, 17)
    
    days_to_engagement = max(0, (engagement_date - current_date).days)
    days_to_wedding = max(0, (wedding_date - current_date).days)
    
    st.markdown(f'<p class="medium-font">Days until Engagement: {days_to_engagement}<br>Are you Ready For It?</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="medium-font">Days until Wedding: {days_to_wedding}<br>Our Love Story: The Long Game</p>', unsafe_allow_html=True)

# Main content
update_countdown()

# Footer
st.markdown('<p class="medium-font">First date: Sweet like Chocolate Room</p>', unsafe_allow_html=True)

# Initialize session state
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
    st.session_state.score = 0
    st.session_state.current_sentence = 0
    st.session_state.sentences = [
        "Travelling with you is the best gift",
        "The bridge of Kheri is our best kiss ever",
        "You make my heart skip a beat with your hugs.",
        "The Crepes when high is our best breakfast",
        "The day I knew I wanted you for life"
    ]
    st.session_state.images = [
        "image1.jpg",
        "image2.jpeg",
        "image3.jpeg",
        "image4.jpeg",
        "image5.jpg"
    ]
    st.session_state.selected_words = []
    st.session_state.scrambled_words = []
    st.session_state.show_image = False

# Game section
st.markdown("---")
st.markdown('<p class="medium-font">Love Letter Puzzle</p>', unsafe_allow_html=True)

# Function to initialize or reset the game
def init_game():
    st.session_state.game_active = True
    st.session_state.score = 0
    st.session_state.current_sentence = 0
    st.session_state.selected_words = []
    st.session_state.scrambled_words = st.session_state.sentences[0].split()
    random.shuffle(st.session_state.scrambled_words)
    st.session_state.show_image = False

# Start game button
if not st.session_state.game_active:
    if st.button("Start Love Letter Puzzle", key="start_game"):
        init_game()

# Game logic
if st.session_state.game_active:
    st.write(f"Score: {st.session_state.score}")
    
    if not st.session_state.show_image:
        # Display scrambled sentence
        sentence = st.session_state.sentences[st.session_state.current_sentence]
        
        st.write("Reconstruct the love letter by selecting words in the correct order:")
        
        # Display selected words
        st.write(" ".join(st.session_state.selected_words))
        
        # Display word buttons
        if st.session_state.scrambled_words:
            cols = st.columns(len(st.session_state.scrambled_words))
            for i, word in enumerate(st.session_state.scrambled_words):
                if cols[i].button(word, key=f"word_{i}", help="Click to select this word"):
                    st.session_state.selected_words.append(word)
                    st.session_state.scrambled_words.remove(word)
                    st.rerun()
        else:
            st.write("All words have been selected. Click 'Check Answer' to verify.")
        
        # Check answer button
        if st.button("Check Answer"):
            if " ".join(st.session_state.selected_words) == sentence:
                st.success("Correct! You've pieced together the love letter!")
                st.session_state.score += 10
                st.session_state.show_image = True
                st.rerun()
            else:
                st.error("That's not quite right. Try rearranging the words!")
                st.session_state.selected_words = []
                st.session_state.scrambled_words = sentence.split()
                random.shuffle(st.session_state.scrambled_words)
                st.rerun()
    
    else:  # Display image after completing a puzzle
        display_image(st.session_state.images[st.session_state.current_sentence])
        if st.button("Continue to Next Puzzle"):
            st.session_state.show_image = False
            st.session_state.current_sentence += 1
            st.session_state.selected_words = []
            if st.session_state.current_sentence >= len(st.session_state.sentences):
                st.balloons()
                st.success(f"Game Over! You've completed all love letters! Your love score: {st.session_state.score}")
                st.session_state.game_active = False
            else:
                st.session_state.scrambled_words = st.session_state.sentences[st.session_state.current_sentence].split()
                random.shuffle(st.session_state.scrambled_words)
            st.rerun()

    # Reset button
    if st.button("Reset Current Puzzle"):
        st.session_state.selected_words = []
        st.session_state.scrambled_words = st.session_state.sentences[st.session_state.current_sentence].split()
        random.shuffle(st.session_state.scrambled_words)
        st.session_state.show_image = False
        st.rerun()

    # End game button
    if st.button("End Game"):
        st.write(f"Game Over! You completed {st.session_state.current_sentence} love letters!")
        st.write(f"Your final love score: {st.session_state.score}")
        st.session_state.game_active = False

# Restart game option
if not st.session_state.game_active and st.session_state.current_sentence > 0:
    if st.button("Play Again"):
        init_game()
        st.rerun()
