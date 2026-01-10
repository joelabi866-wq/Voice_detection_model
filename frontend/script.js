const VOICE_API = "http://127.0.0.1:8000/voice/transcribe";
const GENERATE_API = "http://127.0.0.1:8000/api/generate";

async function recordVoice() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const mediaRecorder = new MediaRecorder(stream);

  let chunks = [];
  mediaRecorder.start();
  alert("Recording... Speak now");

  mediaRecorder.ondataavailable = e => chunks.push(e.data);

  setTimeout(() => {
    mediaRecorder.stop();
  }, 4000);

  mediaRecorder.onstop = async () => {
    const blob = new Blob(chunks, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("file", blob, "voice.webm");

    try {
      const res = await fetch(VOICE_API, {
        method: "POST",
        body: formData
      });

      const data = await res.json();

      if (data.text) {
        document.getElementById("description").value = data.text;
      } else {
        alert("Voice transcription failed");
      }

    } catch (err) {
      console.error(err);
      alert("Error calling voice API");
    }
  };
}

async function generate() {
  const payload = {
    entity_type: document.getElementById("entityType").value,
    generation_mode: "ai",
    fields: {
      name: document.getElementById("name").value,
      start_date: "2024-01-01",
      due_date: "2024-01-10",
      workflow: "Default",
      priority: "High"
    }
  };

  try {
    const res = await fetch(GENERATE_API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    document.getElementById("result").innerText = data.generated_description || "No response";

  } catch (err) {
    console.error(err);
    alert("Error calling generate API");
  }
}
