# ✨ Visyntra - AI Therapist
**Your quiet harbor in the storm. Talk. Journal. Find Clarity.**

Built for the **AMD Slingshot Hackathon** by Team **AGENTIC BOTS**.

---

## 🛑 The Problem
In today's high-pressure environment, severe stress, burnout, and behavioral addictions are rising rapidly. While proper therapeutic guidance has the power to transform lives, mental health care remains heavily stigmatized, expensive, or inaccessible. Millions lack the critical guidance needed to break negative loops.

## 💡 Our Solution
**Visyntra** is a deeply private, Voice and Text-based AI Therapist. It provides a safe, zero-judgment space for mental health support. Powered by advanced LLMs and heavily optimized for edge devices, it delivers real-time Cognitive Behavioral Therapy (CBT) and empathetic support right on the user's local machine, ensuring absolute data privacy.

---

## 🚀 AMD Integration & Edge Privacy
Visyntra is specifically engineered to leverage AMD hardware for maximum privacy:
* **Local LLM Inference:** Our "Deep Privacy Mode" processes highly sensitive therapy data (like addiction recovery) 100% offline using the **Phi-3** model. 
* **Optimized Compute:** This heavy computational task is perfectly suited for the multi-core architecture of **AMD Ryzen™ processors** and **Radeon™ graphics**, ensuring zero-latency voice and text generation without sending private data to the cloud.
* **Future-Proofing:** The unified architecture is designed to scale with **AMD Ryzen™ AI (NPUs)** for future multimodal real-time video avatars.

---

## ✨ Key Features
1. **Unified Multimodal Dashboard:** Seamlessly interact using natural Voice (Speech-to-Text) or secure Text within a single, distraction-free interface.
2. **Clinical Emergency Guardrails:** Real-time monitoring of input for self-harm or crisis keywords. Automatically halts the AI to provide national emergency helplines (e.g., 112).
3. **Dynamic CBT Engine:** The AI adapts its response format automatically—providing empathetic paragraphs for general stress, and actionable, step-by-step bullet points for breaking habit loops.
4. **Edge-Optimized Privacy:** 100% secure processing for sensitive disclosures.

---

## 🛠️ Technology Stack
* **Frontend:** Python, Streamlit
* **Cloud AI Engine:** Groq API (Llama 3.1) for ultra-fast general inference
* **Edge AI Engine:** Ollama (Microsoft Phi-3) for local execution
* **Audio Processing:** SpeechRecognition, Google Text-to-Speech (gTTS) / edge-tts

---

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/Visyntra-AI-Therapist.git](https://github.com/YourUsername/Visyntra-AI-Therapist.git)
   cd Visyntra-AI-Therapist

   Install the required dependencies:
   pip install -r requirements.txt

   Run the application:
   streamlit run app.py
