import whisper

# Load tiny model
model = whisper.load_model("tiny")

# Replace with a small sample audio file you have
result = model.transcribe("recordings/4.wav")  

print("Transcript:", result["text"])
