const state = {
  rating: 0,
  feedbackData: [],
}

const aiResponses = {
  refill: "You can visit any Green Wells service station or request pickup via our hotline.",
  kisumu: "Yes — we have branches in Kisumu, Ugunja, and Mbita.",
  hours: "We are open Monday to Sunday, 6 AM to 10 PM.",
  price: "Our prices are competitive and vary by service. Please visit our website for current rates.",
  default: "Thank you for your question! How else can I help you?",
}

document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners()
})

function setupEventListeners() {
  document.getElementById("feedback-form").addEventListener("submit", handleFeedbackSubmit)

  document.querySelectorAll(".star").forEach((star) => {
    star.addEventListener("click", () => setRating(star.dataset.value))
    star.addEventListener("mouseover", () => hoverRating(star.dataset.value))
  })

  document.getElementById("chat-btn").addEventListener("click", openChat)
  document.getElementById("close-chat").addEventListener("click", closeChat)
  document.getElementById("send-btn").addEventListener("click", sendChatMessage)
  document.getElementById("chat-input").addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendChatMessage()
  })
  document.getElementById("escalate-btn").addEventListener("click", escalateChat)
}

function handleFeedbackSubmit(e) {
  e.preventDefault()

  const formData = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    serviceType: document.getElementById("service-type").value,
    rating: state.rating,
    comments: document.getElementById("comments").value,
    timestamp: new Date().toLocaleString(),
  }

  state.feedbackData.push(formData)
  localStorage.setItem("feedbackData", JSON.stringify(state.feedbackData))

  document.getElementById("success-message").classList.remove("hidden")

  const sentiment = generateSentiment(formData.comments, formData.rating)
  document.getElementById("summary-text").textContent =
    `${sentiment} feedback detected — user appreciated the service quality.`
  document.getElementById("ai-summary").classList.remove("hidden")

  e.target.reset()
  state.rating = 0
  updateStarDisplay()

  setTimeout(() => {
    document.getElementById("success-message").classList.add("hidden")
    document.getElementById("ai-summary").classList.add("hidden")
  }, 5000)
}

function setRating(value) {
  state.rating = value
  updateStarDisplay()
  document.getElementById("rating").value = value
}

function hoverRating(value) {
  document.querySelectorAll(".star").forEach((star, index) => {
    if (index < value) {
      star.style.color = "#6DD47E"
    } else {
      star.style.color = "#ddd"
    }
  })
}

function updateStarDisplay() {
  document.querySelectorAll(".star").forEach((star, index) => {
    if (index < state.rating) {
      star.classList.add("active")
      star.style.color = "#6DD47E"
    } else {
      star.classList.remove("active")
      star.style.color = "#ddd"
    }
  })
}

function openChat() {
  document.getElementById("chat-popup").classList.remove("hidden")
}

function closeChat() {
  document.getElementById("chat-popup").classList.add("hidden")
}

function sendChatMessage() {
  const input = document.getElementById("chat-input")
  const message = input.value.trim()

  if (!message) return

  addChatBubble(message, "user")
  input.value = ""

  setTimeout(() => {
    const response = generateAIResponse(message)
    addChatBubble(response, "bot")
  }, 500)
}

function addChatBubble(message, sender) {
  const messagesContainer = document.getElementById("chat-messages")
  const bubble = document.createElement("div")
  bubble.className = `chat-bubble ${sender}`
  bubble.innerHTML = `<p>${message}</p>`
  messagesContainer.appendChild(bubble)
  messagesContainer.scrollTop = messagesContainer.scrollHeight
}

function generateAIResponse(userMessage) {
  const lowerMessage = userMessage.toLowerCase()

  if (lowerMessage.includes("refill") || lowerMessage.includes("lpg")) {
    return aiResponses.refill
  } else if (lowerMessage.includes("kisumu")) {
    return aiResponses.kisumu
  } else if (lowerMessage.includes("hour") || lowerMessage.includes("open")) {
    return aiResponses.hours
  } else if (lowerMessage.includes("price") || lowerMessage.includes("cost")) {
    return aiResponses.price
  }
  return aiResponses.default
}

function escalateChat() {
  addChatBubble("Connecting you to a live agent...", "bot")
  setTimeout(() => {
    addChatBubble("A support agent will be with you shortly.", "bot")
  }, 1000)
}

function generateSentiment(text, rating) {
  if (rating >= 4) return "Positive"
  if (rating === 3) return "Neutral"
  return "Negative"
}
