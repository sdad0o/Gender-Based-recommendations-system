import os
import librosa
import numpy as np
import h5py
from .utils import create_model

def extract_feature(file_name, **kwargs):
    mfcc = kwargs.get("mfcc")
    chroma = kwargs.get("chroma")
    mel = kwargs.get("mel")
    contrast = kwargs.get("contrast")
    tonnetz = kwargs.get("tonnetz")
    X, sample_rate = librosa.core.load(file_name)
    if chroma or contrast:
        stft = np.abs(librosa.stft(X))
    result = np.array([])
    if mfcc:
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
        result = np.hstack((result, mfccs))
    if chroma:
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
        result = np.hstack((result, chroma))
    if mel:
        mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T,axis=0)
        result = np.hstack((result, mel))
    if contrast:
        contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
        result = np.hstack((result, contrast))
    if tonnetz:
        tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
        result = np.hstack((result, tonnetz))
    return result

if __name__ == "__main__":
    file_path = os.path.join('uploads', 'recording.wav')
    model = create_model()
    model.load_weights("app/results/model.h5")
    if os.path.isfile(file_path):
        features = extract_feature(file_path, mel=True).reshape(1, -1)
        male_prob = model.predict(features)[0][0]
        female_prob = 1 - male_prob
        gender = "male" if male_prob > female_prob else "female"
        print("Result:", gender)
        print(f"Probabilities: Male: {male_prob*100:.2f}% Female: {female_prob*100:.2f}%")
    else:
        print("File not found:", file_path)