import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import numpy as np
import speech_recognition as sr

def audio_frame_callback(frame: av.AudioFrame) -> av.AudioFrame:
    # Convertir la trame audio en tableau numpy
    audio = frame.to_ndarray(format="flt32", layout="mono")
    # Stocker l’audio dans le state pour traitement ultérieur
    if "audio_buffer" not in st.session_state:
        st.session_state.audio_buffer = audio
    else:
        st.session_state.audio_buffer = np.concatenate((st.session_state.audio_buffer, audio))
    return frame

def transcribe_audio(audio_np, sample_rate=48000):
    r = sr.Recognizer()
    # Convertir numpy float32 en bytes 16-bit PCM
    audio_int16 = (audio_np * 32767).astype(np.int16)
    audio_bytes = audio_int16.tobytes()
    audio_data = sr.AudioData(audio_bytes, sample_rate, 2)
    try:
        text = r.recognize_google(audio_data)
        return text
    except Exception:
        return "Sorry, could not transcribe."

def main():
    st.title("Speech Recognition with streamlit-webrtc")

    webrtc_ctx = webrtc_streamer(
        key="speech-recognition",
        audio_frame_callback=audio_frame_callback,
        media_stream_constraints={"audio": True, "video": False},
        async_processing=True,
    )

    if st.button("Transcribe recorded audio"):
        if "audio_buffer" in st.session_state and len(st.session_state.audio_buffer) > 0:
            text = transcribe_audio(st.session_state.audio_buffer)
            st.write("Transcription:", text)
            # Réinitialiser le buffer après transcription
            st.session_state.audio_buffer = np.array([], dtype=np.float32)
        else:
            st.warning("No audio recorded yet. Click 'Start' and speak.")

if __name__ == "__main__":
    main()
