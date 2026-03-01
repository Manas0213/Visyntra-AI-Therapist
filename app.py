import streamlit as st
import speech_recognition as sr
from groq import Groq
import edge_tts
import asyncio
import base64
import time
import os

# ==========================================
# 1. Page Configuration & Custom UI (VISYNTRA)
# ==========================================
st.set_page_config(page_title="Visyntra", page_icon="✨", layout="centered", initial_sidebar_state="expanded")

# Custom CSS for Premium Aesthetic, Slide-Up Animation & UI Fixes
st.markdown("""
    <style>
        /* HIDE STREAMLIT BRANDING COMPLETELY */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Premium Background for Main App */
        .stApp {
            background-color: #F8FAFC !important;
        }

        /* =========================================
           ✨ SIDEBAR FIXES (PERFECT VISIBILITY)
           ========================================= */
        [data-testid="stSidebar"] {
            background-color: #0F172A !important; 
        }
        [data-testid="stSidebar"] * {
            color: #F8FAFC !important; 
        }

        /* =========================================
           ✨ MAIN CHAT AREA TEXT FIXES (THE ULTIMATE FIX)
           ========================================= */
        /* Forces ALL text inside the chat bubbles to be dark, even during streaming */
        [data-testid="stChatMessageContent"], 
        [data-testid="stChatMessageContent"] * {
            color: #0F172A !important; 
            font-size: 1.05rem !important;
            line-height: 1.6 !important;
        }
        
        [data-testid="stChatMessage"]:nth-child(even) {
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            padding: 10px;
        }

        .main h1 { color: #0F172A !important; font-weight: 700; }
        
        /* Visyntra Main Button Styling */
        div.stButton > button {
            background-color: #0F172A !important; 
            border-radius: 30px;
            border: none;
            padding: 12px 28px;
            box-shadow: 0 4px 10px rgba(15, 23, 42, 0.15);
            transition: all 0.3s ease;
            display: block;
            margin: 0 auto; 
        }
        div.stButton > button p {
            color: #F8FAFC !important;
            font-size: 16px !important;
            font-weight: 500 !important;
        }
        div.stButton > button:hover {
            background-color: #1E293B !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(15, 23, 42, 0.2);
        }

        /* PREMIUM HERO SECTION & ANIMATION */
        @keyframes slideUpFade {
            0% { opacity: 0; transform: translateY(60px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        
        .hero-container {
            text-align: center;
            padding: 60px 0 30px 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            animation: slideUpFade 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        }
        
        .hero-title {
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #F59E0B, #10B981);
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            margin-bottom: 5px !important;
            position: relative;
            z-index: 1;
        }
        
        .hero-title::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 140%;
            height: 140%;
            background: radial-gradient(circle, rgba(16,185,129,0.15) 0%, rgba(245,158,11,0.05) 40%, transparent 70%);
            transform: translate(-50%, -50%);
            z-index: -1;
            filter: blur(20px);
            animation: pulseGlow 4s infinite alternate;
        }
        
        .hero-subtitle {
            color: #64748B !important;
            font-size: 1.2rem;
            margin-bottom: 35px;
            font-weight: 500;
        }
        
        .chip-container {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            justify-content: center;
            margin-bottom: 25px;
        }
        
        .suggestion-chip {
            background-color: transparent;
            color: #10B981 !important;
            border: 1.5px solid rgba(16, 185, 129, 0.4);
            border-radius: 25px;
            padding: 10px 22px;
            font-size: 0.95rem;
            font-weight: 600;
            box-shadow: 0 2px 5px rgba(16, 185, 129, 0.05);
            transition: all 0.3s ease;
        }
        
        @keyframes pulseGlow {
            from { opacity: 0.6; transform: translate(-50%, -50%) scale(0.95); }
            to { opacity: 1; transform: translate(-50%, -50%) scale(1.05); }
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.title("✨ Visyntra Settings")
st.sidebar.write("Choose your interaction mode:")

app_mode = st.sidebar.radio(
    "",
    ["🗣️ Spoken Audio", "⌨️ Written Journal"]
)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 End Session & Clear"):
    st.session_state.chat_history = []
    st.rerun()

# ==========================================
# 2. State Management & Header UI Logic
# ==========================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# API Initialization
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

system_prompt = """You are Visyntra, a highly empathetic, patient, and grounding AI Clinical Psychologist. 
STRICT THERAPEUTIC GUIDELINES:
1. EMPATHY FIRST: Always start by acknowledging the user's feelings. Make them feel heard, validated, and safe before offering any advice.
2. CONVERSATIONAL TONE: Speak in a warm, soft, and natural human voice. 
3. CONDITIONAL FORMATTING: Use natural, flowing paragraphs for emotional support. ONLY use bullet points when providing specific coping strategies or actionable steps. 
4. STRICT BULLET POINT RULES: When you DO use bullet points, you MUST use proper Markdown formatting. EVERY single bullet point MUST start on a completely NEW LINE. NEVER put multiple bullet points on the same line.
5. PACING & LENGTH: Ask gentle, open-ended questions. Keep responses concise.
6. STRICT LANGUAGE RULE: YOU MUST RESPOND EXCLUSIVELY IN ENGLISH. DO NOT USE HINDI OR ANY OTHER LANGUAGE UNDER ANY CIRCUMSTANCES."""

# Dynamic Header
if len(st.session_state.chat_history) > 0:
    st.markdown("<h1 style='text-align: center;'>✨ Visyntra</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B;'>Your calming space for clarity, focus, and mindful processing.</p>", unsafe_allow_html=True)
    st.markdown("---")
else:
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">✨ Visyntra</h1>
            <p class="hero-subtitle">Your quiet harbor in the storm. Talk. Journal. Find Clarity.</p>
            <div class="chip-container">
                <div class="suggestion-chip">🌿 Help with Exam Stress</div>
                <div class="suggestion-chip">✍️ I just need someone to listen</div>
                <div class="suggestion-chip">💭 Let's work on anxiety</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Render existing chat history
for message in st.session_state.chat_history:
    avatar = "👤" if message["role"] == "user" else "✨"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ==========================================
# 3. Emergency Guardrail Function
# ==========================================
def check_crisis(text):
    crisis_words = ["suicide", "kill myself", "die", "end my life", "suicidal"]
    if any(word in text.lower() for word in crisis_words):
        crisis_message = "I hear how much pain you are in right now. Please immediately call the National Emergency Helpline at 112. You are not alone."
        st.session_state.chat_history.append({"role": "assistant", "content": crisis_message})
        with st.chat_message("assistant", avatar="✨"):
            st.error(crisis_message)
        st.stop()

# ==========================================
# 4. Mode 1: Voice Chat 
# ==========================================
if app_mode == "🗣️ Spoken Audio":
    st.write("") 
    
    status_ui = st.empty()
    
    if st.button("🎙️ Tap to Speak to Visyntra"):
        r = sr.Recognizer()
        r.pause_threshold = 1.5  
        r.energy_threshold = 300 
        
        # Premium Listening Animation
        listening_animation = """
            <style>
                .listening-box {
                    display: flex; justify-content: center; align-items: center;
                    padding: 12px 20px; background-color: #ffffff; border-radius: 30px;
                    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.2);
                    width: fit-content; margin: 0 auto 20px auto;
                }
                .dot {
                    width: 10px; height: 10px; margin: 0 4px;
                    background-color: #10B981; border-radius: 50%;
                    animation: bounce-listen 1.4s infinite ease-in-out both;
                }
                .dot:nth-child(1) { animation-delay: -0.32s; }
                .dot:nth-child(2) { animation-delay: -0.16s; }
                @keyframes bounce-listen {
                    0%, 80%, 100% { transform: scale(0); opacity: 0.4; }
                    40% { transform: scale(1.2); opacity: 1; box-shadow: 0 0 8px rgba(16,185,129,0.8); }
                }
                .listen-text {
                    color: #10B981 !important; font-weight: 600; font-size: 1rem; margin-left: 10px; letter-spacing: 0.5px;
                }
            </style>
            <div class="listening-box">
                <div class="dot"></div><div class="dot"></div><div class="dot"></div>
                <div class="listen-text">Listening...</div>
            </div>
        """
        status_ui.markdown(listening_animation, unsafe_allow_html=True)

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = r.listen(source, timeout=10) 
                
                status_ui.success("✅ Audio captured! Processing...")
                
                wav_data = audio.get_wav_data()
                with open("temp_user_voice.wav", "wb") as f:
                    f.write(wav_data)
                
                with open("temp_user_voice.wav", "rb") as audio_file:
                    transcription = client.audio.transcriptions.create(
                        file=("temp_user_voice.wav", audio_file.read()),
                        model="whisper-large-v3",
                        language="en" 
                    )
                user_text = transcription.text
                
                if os.path.exists("temp_user_voice.wav"):
                    os.remove("temp_user_voice.wav")
                
                st.session_state.chat_history.append({"role": "user", "content": user_text})
                status_ui.empty()
                
                with st.chat_message("user", avatar="👤"):
                    st.markdown(user_text)

                check_crisis(user_text)

                with st.spinner("Visyntra is preparing response..."):
                    messages = [{"role": "system", "content": system_prompt}] + st.session_state.chat_history
                    chat_completion = client.chat.completions.create(
                        messages=messages,
                        model="llama-3.1-8b-instant",
                    )
                    response_text = chat_completion.choices[0].message.content

                    audio_file = "response.mp3"
                    async def generate_speech(text, filepath):
                        communicate = edge_tts.Communicate(text, "en-US-EmmaNeural", rate="-10%", pitch="-5Hz")
                        await communicate.save(filepath)

                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(generate_speech(response_text, audio_file))

                    with open(audio_file, "rb") as f:
                        audio_bytes = f.read()
                        b64_audio = base64.b64encode(audio_bytes).decode()

                st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                with st.chat_message("assistant", avatar="✨"):
                    
                    hidden_audio_html = f"""
                        <audio autoplay="true" style="display:none;">
                            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                        </audio>
                    """
                    st.markdown(hidden_audio_html, unsafe_allow_html=True)

                    speaking_visualization_html = """
                        <style>
                            .speaking-container {
                                display: flex; justify-content: flex-start; align-items: center;
                                height: 40px; margin: 10px 0px 20px 15px; gap: 6px; 
                            }
                            .speaking-line {
                                width: 6px; border-radius: 4px; background-color: #0F172A; 
                                animation: speaking-pulse 1.2s ease-in-out infinite;
                            }
                            @keyframes speaking-pulse {
                                0%, 100% { height: 10px; opacity: 0.5; }
                                50% { height: 30px; opacity: 1; } 
                            }
                            .speaking-line:nth-child(1) { animation-delay: 0.0s; }
                            .speaking-line:nth-child(2) { animation-delay: 0.15s; }
                            .speaking-line:nth-child(3) { animation-delay: 0.3s; }
                            .speaking-line:nth-child(4) { animation-delay: 0.45s; }
                            .speaking-line:nth-child(5) { animation-delay: 0.6s; }
                        </style>
                        <div class="speaking-container">
                            <div class="speaking-line"></div><div class="speaking-line"></div>
                            <div class="speaking-line"></div><div class="speaking-line"></div>
                            <div class="speaking-line"></div>
                        </div>
                    """
                    animation_placeholder = st.empty()
                    animation_placeholder.markdown(speaking_visualization_html, unsafe_allow_html=True)

                    def sync_stream(text):
                        words = text.split()
                        for word in words:
                            yield word + " "
                            time.sleep(0.35) 

                    st.write_stream(sync_stream(response_text))
                    
                    time.sleep(1.0)
                    animation_placeholder.empty()

            except sr.UnknownValueError:
                status_ui.error("⚠️ I couldn't quite catch that. Could you try speaking again?")
            except sr.WaitTimeoutError:
                status_ui.warning("⚠️ It's quiet. Take your time, and tap the button when you're ready.")
            except Exception as e:
                status_ui.error(f"System Error: {e}")

# ==========================================
# 5. Mode 2: Text Chat (WRITTEN JOURNAL)
# ==========================================
elif app_mode == "⌨️ Written Journal":
    
    user_input = st.chat_input("Write your thoughts to Visyntra here...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
            
        check_crisis(user_input)

        with st.chat_message("assistant", avatar="✨"):
            try:
                messages = [{"role": "system", "content": system_prompt}] + st.session_state.chat_history
                response_stream = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.1-8b-instant",
                    stream=True
                )
                
                def generate_response():
                    for chunk in response_stream:
                        if chunk.choices[0].delta.content is not None:
                            yield chunk.choices[0].delta.content
                
                reply_text = st.write_stream(generate_response())
                st.session_state.chat_history.append({"role": "assistant", "content": reply_text})
                
            except Exception as e:
                st.error(f"System Error: {e}")
