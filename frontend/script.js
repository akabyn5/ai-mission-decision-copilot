function analyze() {
  fetch("http://127.0.0.1:5000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      subsystem: "thermal",
      metric: "temperature_core",
      value: 85,
      mission_phase: "nominal",
      timestamp: "2026-04-17T12:30:00Z"
    })
  })
  .then(res => res.json())
  .then(data => {

    // 🔴 Manejo de error backend
    if (data.error) {
      alert(data.error);
      return;
    }

    // ✅ MAPEO EXACTO (ESTO ES LO IMPORTANTE)
    document.getElementById("classification").textContent = data.classification;
    document.getElementById("severity").textContent = data.severity;
    document.getElementById("action").textContent = data.recommended_action;
    document.getElementById("reasoning").textContent = data.reasoning;

  })
  .catch(err => {
    console.error(err);
    alert("Error connecting to backend");
  });
}