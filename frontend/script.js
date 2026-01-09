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

const entitySelect = document.getElementById("entityType");
const form = document.getElementById("dynamicForm");
const result = document.getElementById("result");

entitySelect.addEventListener("change", renderForm);
document.getElementById("generateBtn").addEventListener("click", generate);

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

async function generate() {
  const type = entitySelect.value;
  if (!type) return alert("Select entity type");

  let fields = {};
  [...schemas[type].required, ...schemas[type].optional].forEach(field => {
    const value = document.getElementById(field).value;
    if (value) {
      fields[field] = field === "checklist" ? value.split(",") : value;
    }
  });

  const payload = {
    entity_type: type,
    generation_mode: "ai",
    fields: fields
  };

  try {
    const res = await fetch("http://127.0.0.1:8001/generate/api/generate",{
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    result.innerText = data.generated_description || data.error;

  } catch (err) {
    result.innerText = "Error connecting to server";
  }
}
