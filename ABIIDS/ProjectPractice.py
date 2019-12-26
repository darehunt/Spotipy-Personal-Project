import librosa
import matplotlib.pyplot as plt
import librosa.display

# path for sampled audio
audio_path = '/Users/darehunt/ABIIDS/test2.m4a'

# x is the audio as a wave form
# sr is the sampling rate, default is 22050 Hz
x, sr = librosa.load(audio_path, sr=44100)

#plot the spectrogram
plt.figure(figsize=(14, 5))
librosa.display.waveplot(x, sr=sr)
plt.show()