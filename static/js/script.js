// State Management
const state = {
  currentView: "user",
  currentLanguage: "en",
  theme: "light",
  aiPersonality: "friendly",
  feedbackData: [],
  currentChatId: 1,
  rating: 0,
  isAdminAuthenticated: false,
}

// Translations
const translations = {
  en: {
    feedback: "Send Us Your Feedback",
    submit: "Submit Feedback",
    chat: "Chat with Support",
    settings: "Settings",
  },
  sw: {
    feedback: "Tuma Maoni Yako",
    submit: "Tuma Maoni",
    chat: "Sema na Msaada",
    settings: "Mipango",
  },
  fr: {
    feedback: "Envoyez-nous vos commentaires",
    submit: "Soumettre les commentaires",
    chat: "Discuter avec le support",
    settings: "Paramètres",
  },
}

// AI Chat Responses
const aiResponses = {
  refill: "You can visit any Green Wells service station or request pickup via our hotline.",
  kisumu: "Yes — we have branches in Kisumu, Ugunja, and Mbita.",
  hours: "We are open Monday to Sunday, 6 AM to 10 PM.",
  price: "Our prices are competitive and vary by service. Please visit our website for current rates.",
  default: "Thank you for your question! How else can I help you?",
}

// Initialize App
document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners()
  loadSettings()
  generateChartData()
  loadAuthenticationState()
})

function loadAuthenticationState() {
  const isAuthenticated = localStorage.getItem("adminAuthenticated") === "true"
  state.isAdminAuthenticated = isAuthenticated
  updateAuthUI()
}

function updateAuthUI() {
  const logoutBtn = document.getElementById("logout-btn")
  if (state.isAdminAuthenticated) {
    logoutBtn.classList.remove("hidden")
  } else {
    logoutBtn.classList.add("hidden")
  }
}

function handleAdminLogin(e) {
  e.preventDefault()
  const username = document.getElementById("login-username").value
  const password = document.getElementById("login-password").value
  const errorMsg = document.getElementById("login-error")

  // Simple credential check (in production, this would be server-side)
  if (username === "admin" && password === "admin123") {
    state.isAdminAuthenticated = true
    localStorage.setItem("adminAuthenticated", "true")
    document.getElementById("login-modal").classList.add("hidden")
    document.getElementById("login-form").reset()
    errorMsg.classList.add("hidden")
    updateAuthUI()
  } else {
    errorMsg.classList.remove("hidden")
  }
}

function handleLogout() {
  state.isAdminAuthenticated = false
  localStorage.setItem("adminAuthenticated", "false")
  switchView("user")
  updateAuthUI()
}

// Event Listeners
function setupEventListeners() {
  // Navigation
  document.querySelectorAll(".nav-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const view = e.target.dataset.view
      if (view === "admin" && !state.isAdminAuthenticated) {
        document.getElementById("login-modal").classList.remove("hidden")
      } else {
        switchView(view)
      }
    })
  })

  document.getElementById("logout-btn").addEventListener("click", handleLogout)

  document.getElementById("login-form").addEventListener("submit", handleAdminLogin)

  // Feedback Form
  document.getElementById("feedback-form").addEventListener("submit", handleFeedbackSubmit)

  // Star Rating
  document.querySelectorAll(".star").forEach((star) => {
    star.addEventListener("click", () => setRating(star.dataset.value))
    star.addEventListener("mouseover", () => hoverRating(star.dataset.value))
  })

  // Chat
  document.getElementById("chat-btn").addEventListener("click", openChat)
  document.getElementById("close-chat").addEventListener("click", closeChat)
  document.getElementById("send-btn").addEventListener("click", sendChatMessage)
  document.getElementById("chat-input").addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendChatMessage()
  })
  document.getElementById("escalate-btn").addEventListener("click", escalateChat)

  // Admin Dashboard
  document.querySelectorAll(".sidebar-item").forEach((item) => {
    item.addEventListener("click", (e) => switchAdminSection(e.target.dataset.section))
  })

  // Agent Dashboard
  document.querySelectorAll(".chat-item").forEach((item) => {
    item.addEventListener("click", (e) => selectChat(e.currentTarget.dataset.chatId))
  })

  // Settings
  document.querySelectorAll(".settings-tab").forEach((tab) => {
    tab.addEventListener("click", (e) => switchSettingsTab(e.target.dataset.tab))
  })

  document.querySelectorAll(".toggle-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => toggleTheme(e.target.dataset.theme))
  })

  document.getElementById("language-select").addEventListener("change", (e) => {
    changeLanguage(e.target.value)
  })

  document.getElementById("ai-slider").addEventListener("input", (e) => {
    updateAIPersonality(e.target.value)
  })

  // Suggestion buttons
  document.querySelectorAll(".suggestion-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => insertSuggestion(e.target.textContent))
  })
}

// View Switching
function switchView(view) {
  state.currentView = view
  document.querySelectorAll(".view").forEach((v) => v.classList.remove("active"))
  document.getElementById(`${view}-view`).classList.add("active")

  document.querySelectorAll(".nav-btn").forEach((btn) => btn.classList.remove("active"))
  document.querySelector(`[data-view="${view}"]`).classList.add("active")
}

// Feedback Form
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

  // Show success message
  document.getElementById("success-message").classList.remove("hidden")

  // Generate AI Summary
  const sentiment = generateSentiment(formData.comments, formData.rating)
  document.getElementById("summary-text").textContent =
    `${sentiment} feedback detected — user appreciated the service quality.`
  document.getElementById("ai-summary").classList.remove("hidden")

  // Reset form
  e.target.reset()
  state.rating = 0
  updateStarDisplay()

  // Hide messages after 5 seconds
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

// Chat Functions
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

  // Add user message
  addChatBubble(message, "user")
  input.value = ""

  // Simulate typing
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

// Admin Dashboard
function switchAdminSection(section) {
  document.querySelectorAll(".dashboard-section").forEach((s) => s.classList.remove("active"))
  document.getElementById(`${section}-section`).classList.add("active")

  document.querySelectorAll(".sidebar-item").forEach((item) => item.classList.remove("active"))
  document.querySelector(`[data-section="${section}"]`).classList.add("active")
}

function generateChartData() {
  const chart = document.getElementById("trend-chart")
  const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
  const data = [45, 52, 48, 61, 55, 67, 72]

  chart.innerHTML = ""
  const maxValue = Math.max(...data)

  data.forEach((value, index) => {
    const bar = document.createElement("div")
    bar.className = "chart-bar"
    bar.style.height = `${(value / maxValue) * 100}%`
    bar.title = `${days[index]}: ${value} feedback`
    chart.appendChild(bar)
  })
}

// Agent Dashboard
function selectChat(chatId) {
  state.currentChatId = chatId

  document.querySelectorAll(".chat-item").forEach((item) => item.classList.remove("active"))
  document.querySelector(`[data-chat-id="${chatId}"]`).classList.add("active")

  // Update conversation (simulated)
  const chatData = {
    1: { name: "Mercy K.", sentiment: "friendly" },
    2: { name: "James M.", sentiment: "urgent" },
    3: { name: "Lisa P.", sentiment: "neutral" },
  }

  const customer = chatData[chatId]
  document.getElementById("current-customer").textContent = customer.name
  document.getElementById("current-sentiment").textContent = customer.sentiment
  document.getElementById("current-sentiment").className = `sentiment-tag ${customer.sentiment}`
}

function insertSuggestion(text) {
  document.getElementById("agent-input").value = text
}

// Settings
function switchSettingsTab(tab) {
  document.querySelectorAll(".settings-tab-content").forEach((content) => content.classList.remove("active"))
  document.getElementById(`${tab}-tab`).classList.add("active")

  document.querySelectorAll(".settings-tab").forEach((t) => t.classList.remove("active"))
  document.querySelector(`[data-tab="${tab}"]`).classList.add("active")
}

function toggleTheme(theme) {
  state.theme = theme
  document.querySelectorAll(".toggle-btn").forEach((btn) => btn.classList.remove("active"))
  document.querySelector(`[data-theme="${theme}"]`).classList.add("active")

  if (theme === "dark") {
    document.body.classList.add("dark-mode")
  } else {
    document.body.classList.remove("dark-mode")
  }

  localStorage.setItem("theme", theme)
}

function changeLanguage(lang) {
  state.currentLanguage = lang
  localStorage.setItem("language", lang)
  // In a real app, this would update all UI text
}

function updateAIPersonality(value) {
  const personalities = ["Friendly", "Professional", "Neutral"]
  state.aiPersonality = personalities[value - 1]
  document.querySelector(".slider-value").textContent = `Current: ${personalities[value - 1]}`
  localStorage.setItem("aiPersonality", state.aiPersonality)
}

// Utility Functions
function generateSentiment(text, rating) {
  if (rating >= 4) return "Positive"
  if (rating === 3) return "Neutral"
  return "Negative"
}

function loadSettings() {
  const savedTheme = localStorage.getItem("theme") || "light"
  const savedLanguage = localStorage.getItem("language") || "en"
  const savedPersonality = localStorage.getItem("aiPersonality") || "Friendly"

  state.theme = savedTheme
  state.currentLanguage = savedLanguage
  state.aiPersonality = savedPersonality

  if (savedTheme === "dark") {
    document.body.classList.add("dark-mode")
    document.querySelector('[data-theme="dark"]').classList.add("active")
  }

  document.getElementById("language-select").value = savedLanguage

  const personalityIndex = ["Friendly", "Professional", "Neutral"].indexOf(savedPersonality)
  document.getElementById("ai-slider").value = personalityIndex + 1
  document.querySelector(".slider-value").textContent = `Current: ${savedPersonality}`
}
