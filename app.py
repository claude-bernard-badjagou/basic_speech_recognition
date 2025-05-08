import streamlit as st
import speech_recognition as sr

def transcribe_audio_file(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language="fr-FR")
            return text
        except sr.UnknownValueError:
            return "Je n'ai pas compris l'audio."
        except sr.RequestError as e:
            return f"Erreur du service Google Speech Recognition : {e}"

def main():
    st.title("Application de reconnaissance vocale")
    st.write("Téléverse un fichier audio au format .wav pour transcription.")

    uploaded_file = st.file_uploader("Choisis un fichier .wav", type=["wav"])
    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/wav")
        st.info("Transcription en cours...")
        transcription = transcribe_audio_file(uploaded_file)
        st.success("Résultat de la transcription :")
        st.write(transcription)

if __name__ == "__main__":
    main()
