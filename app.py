from flask import Flask, request, jsonify, render_template
import os
import whisper
from transformers import pipeline

app = Flask(__name__)
UPLOAD_FOLDER = "recordings"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Whisper model
print("Loading Whisper model...")
whisper_model = whisper.load_model("tiny")
print("Whisper loaded!")

# Load summarization model
print("Loading summarization model...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)  # CPU
print("Summarizer loaded!")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Transcribe audio
    result = whisper_model.transcribe(filepath)
    transcript = result['text']

    # Summarize transcript
    summary_text = summarizer(transcript, max_length=150, min_length=50, do_sample=False)[0]['summary_text']

    # Simple bullet formatting for demo
    agenda = "- Weekly Student Success Meeting\n- Attendance Issues\n- Student Concerns"
    speaker_notes = "- Speaker 1: Reports attendance\n- Speaker 2: Suggests pancake breakfast\n- Speaker 3: Shares student stress info"
    summary = f"- Transcript Summary: {summary_text}"

    response = {
        "transcript": transcript,
        "agenda": agenda,
        "speaker_notes": speaker_notes,
        "summary": summary
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
