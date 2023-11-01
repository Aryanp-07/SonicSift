import librosa
from tensorflow.keras.models import load_model
import numpy as np


genres = {
    'blues': 0, 'classical': 1, 'country': 2, 'disco': 3, 'hiphop': 4,
    'jazz': 5, 'metal': 6, 'pop': 7, 'reggae': 8, 'rock': 9
}

loaded_model = load_model('sonicsift.keras')

def divide_audio(y, sr):
    segment_duration = 2
    total_duration = 15
    segment_samples = int(segment_duration * sr)
    overlap = int(segment_samples / 2)
    total_samples = int(total_duration * sr)
    segments = [y[i:i + segment_samples] for i in range(0, min(len(y), total_samples) - segment_samples + 1, overlap)]
    return segments

def process_segment(segment, sr):
    ps = librosa.feature.melspectrogram(y=segment, sr=sr, hop_length=256, n_fft=512, n_mels=64)
    ps = librosa.power_to_db(ps**2)
    ps = ps.reshape((1, ps.shape[0], ps.shape[1], 1))
    return ps

def predict_genre(file_path): # pass the file path using flask ; collect the predicted genre
    y, sr = librosa.load(file_path, mono=True)
    segments = divide_audio(y, sr)
    votes = {genre: 0 for genre in genres}
    for segment in segments:
        processed_segment = process_segment(segment, sr)
        predictions = loaded_model.predict(processed_segment)
        predicted_genre_index = np.argmax(predictions, axis=1)[0]
        predicted_genre = list(genres.keys())[list(genres.values()).index(predicted_genre_index)]
        votes[predicted_genre] += 1
    return max(votes, key=votes.get)


# print('Predicted Genre:',predict_genre(''))