/* ================================
   SCHEMA DEFINITIONS
================================ */

const schemas = {
  review: {
    required: ["name", "start_date", "due_date", "workflow", "priority"],
    optional: ["parent_review", "estimated_cost", "actual_cost", "checklist"]
  },
  rfa: {
    required: ["name", "request_date", "due_date", "workflow", "priority"],
    optional: ["checklist"]
  },
  issue: {
    required: [
      "name",
      "issue_type",
      "placement",
      "root_cause",
      "start_date",
      "due_date",
      "workflow"
    ],
    optional: ["location", "estimated_cost", "actual_cost"]
  }
};

/* ================================
   DOM ELEMENTS
================================ */

const entitySelect = document.getElementById("entityType");
const form = document.getElementById("dynamicForm");
const result = document.getElementById("result");
const generateBtn = document.getElementById("generateBtn");

const micBtn = document.getElementById("micBtn");
const voiceText = document.getElementById("voiceText");

/* ================================
   EVENT LISTENERS
================================ */

entitySelect.addEventListener("change", renderForm);
generateBtn.addEventListener("click", generate);

micBtn.addEventListener("click", (e) => {
  e.preventDefault();
  toggleRecording();
});

/* ================================
   FORM RENDERING
================================ */

function renderForm() {
  form.innerHTML = "";
  const type = entitySelect.value;
  if (!schemas[type]) return;

  [...schemas[type].required, ...schemas[type].optional].forEach(field => {
    form.innerHTML += `
      <label>${formatLabel(field)}</label>
      <input id="${field}" />
    `;
  });
}

function formatLabel(text) {
  return text.replace(/_/g, " ").toUpperCase();
}

/* ================================
   AI DESCRIPTION GENERATION
================================ */

async function generate() {
  const type = entitySelect.value;
  if (!type) {
    alert("Select entity type");
    return;
  }

  let fields = {};
  [...schemas[type].required, ...schemas[type].optional].forEach(field => {
    const input = document.getElementById(field);
    if (input && input.value) {
      fields[field] =
        field === "checklist"
          ? input.value.split(",").map(i => i.trim())
          : input.value;
    }
  });

  const payload = {
    entity_type: type,
    generation_mode: "ai",
    fields: fields
  };

  result.innerText = "Generating description...";

  try {
    const res = await fetch(
      "http://127.0.0.1:8001/generate/api/generate",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      }
    );

    const data = await res.json();
    result.innerText = data.generated_description || data.error;

  } catch (err) {
    result.innerText = "Error connecting to server";
  }
}

/* ================================
   🎤 VOICE RECORDING LOGIC
================================ */

let mediaRecorder;
let audioChunks = [];

async function toggleRecording() {
  if (!mediaRecorder || mediaRecorder.state === "inactive") {
    startRecording();
  } else {
    stopRecording();
  }
}

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = event => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
      }
    };

    mediaRecorder.onstop = sendAudioToServer;

    mediaRecorder.start();
    micBtn.innerText = "⏹️";
    micBtn.classList.add("recording");

  } catch (err) {
    alert("Microphone access denied or unavailable");
  }
}

function stopRecording() {
  mediaRecorder.stop();
  micBtn.innerText = "🎤";
  micBtn.classList.remove("recording");
}

async function sendAudioToServer() {
  const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
  const formData = new FormData();
  formData.append("file", audioBlob, "voice.wav");

  voiceText.value = "Transcribing voice...";

  try {
    const res = await fetch(
      "http://127.0.0.1:8001/voice/transcribe",
      {
        method: "POST",
        body: formData
      }
    );

    const data = await res.json();

    if (data.success) {
      voiceText.value = data.text;
    } else {
      voiceText.value = "Voice transcription failed";
    }

  } catch (err) {
    voiceText.value = "Error connecting to voice service";
  }
}
