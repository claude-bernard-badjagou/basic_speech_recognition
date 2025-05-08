import streamlit as st
import av
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, ClientSettings

# Paramètres WebRTC
WEBRTC_CLIENT_SETTINGS = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"audio": True, "video": False},
)

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.transcription = ""

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Convertir l'audio en données utilisables par SpeechRecognition
        audio = frame.to_ndarray().flatten().astype("int16").tobytes()
        audio_data = sr.AudioData(audio, frame.sample_rate, 2)

        try:
            # Transcrire l'audio avec Google
            text = self.recognizer.recognize_google(audio_data, language="fr-FR")
            self.transcription = text
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            self.transcription = f"[Erreur Google API : {e}]"

        return frame

def main():
    st.title("🎙️ Application de reconnaissance vocale en ligne")

    ctx = webrtc_streamer(
        key="speech-to-text",
        client_settings=WEBRTC_CLIENT_SETTINGS,
        audio_processor_factory=AudioProcessor,
    )

    if ctx.audio_processor:
        if ctx.audio_processor.transcription:
            st.markdown("**Texte transcrit :**")
            st.success(ctx.audio_processor.transcription)

if __name__ == "__main__":
    main()
