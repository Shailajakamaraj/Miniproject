document.getElementById("generateBtn").addEventListener("click", async () => {
    const fileInput = document.getElementById("audioFile");
    if (!fileInput.files[0]) {
        alert("Please select an audio file!");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    document.getElementById("transcript").textContent = data.transcript;
    document.getElementById("agenda").textContent = data.agenda;
    document.getElementById("speaker_notes").textContent = data.speaker_notes;
    document.getElementById("summary").textContent = data.summary;
});
