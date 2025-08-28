async function sendMessage() {
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const message = input.value.trim();
  if (!message) return;

  // hiển thị tin nhắn user
  const userMsg = document.createElement("div");
  userMsg.className = "message user";
  userMsg.innerText = message;
  chatBox.appendChild(userMsg);
  chatBox.scrollTop = chatBox.scrollHeight;
  input.value = "";

  // gọi API backend
  try {
    const res = await fetch("http://127.0.0.1:5000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: message })
    });
    const data = await res.json();

    const botMsg = document.createElement("div");
    botMsg.className = "message bot";
    botMsg.innerText = data.answer || "No answer.";
    chatBox.appendChild(botMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

  } catch (error) {
    const errMsg = document.createElement("div");
    errMsg.className = "message bot";
    errMsg.innerText = "⚠️ Error connecting to server.";
    chatBox.appendChild(errMsg);
  }
}

async function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const status = document.getElementById("upload-status");
  if (!fileInput.files.length) {
    status.innerText = "Please choose a file first.";
    return;
  }

  const file = fileInput.files[0];
  const reader = new FileReader();
  reader.onload = async function(e) {
    try {
      const jsonData = JSON.parse(e.target.result);
      const res = await fetch("http://127.0.0.1:5000/api/upload", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(jsonData)
      });

      if (res.ok) {
        status.innerText = "✅ Upload successful!";
        status.style.color = "green";
      } else {
        status.innerText = "❌ Upload failed.";
        status.style.color = "red";
      }
    } catch (err) {
      status.innerText = "❌ Invalid JSON file.";
      status.style.color = "red";
    }
  };
  reader.readAsText(file);
}

// Gửi bằng phím Enter
document.getElementById("user-input").addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

function formatTime(date) {
  const h = String(date.getHours()).padStart(2, '0');
  const m = String(date.getMinutes()).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  const mo = String(date.getMonth() + 1).padStart(2, '0');
  const y = date.getFullYear();
  return `${h}:${m} - ${d}/${mo}/${y}`;
}

function insertChatDate(date) {
  const chatBox = document.getElementById("chat-box");
  const dateEl = document.createElement("div");
  dateEl.className = "chat-date";

  const day = date.toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  });
  dateEl.textContent = day;
  chatBox.appendChild(dateEl);
}

let lastMessageDate = null;
function isNewDay(date) {
  const dateString = date.toDateString();
  if (lastMessageDate !== dateString) {
    lastMessageDate = dateString;
    return true;
  }
  return false;
}