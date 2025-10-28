const state = {
  isAgentAuthenticated: false,
  currentChatId: 1,
}

function initAgent() {
  loadAuthenticationState()
  setupEventListeners()
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initAgent)
} else {
  initAgent()
}

function loadAuthenticationState() {
  const isAuthenticated = localStorage.getItem("agentAuthenticated") === "true"
  state.isAgentAuthenticated = isAuthenticated
  updateAuthUI()
}

function updateAuthUI() {
  const loginModal = document.getElementById("login-modal")
  const navbar = document.getElementById("navbar")
  const agentDashboard = document.getElementById("agent-dashboard")

  // Defensive: only change classes if elements exist on the page
  if (state.isAgentAuthenticated) {
    if (loginModal) loginModal.classList.add("hidden")
    if (navbar) navbar.classList.remove("hidden")
    if (agentDashboard) {
      // `.view` elements are shown when they have the `active` class.
      agentDashboard.classList.remove("hidden")
      agentDashboard.classList.add("active")
    }
  } else {
    if (loginModal) loginModal.classList.remove("hidden")
    if (navbar) navbar.classList.add("hidden")
    if (agentDashboard) {
      agentDashboard.classList.remove("active")
      agentDashboard.classList.add("hidden")
    }
  }
}

function handleAgentLogin(e) {
  e.preventDefault()
  const username = document.getElementById("login-username").value
  const password = document.getElementById("login-password").value
  const errorMsg = document.getElementById("login-error")

  if (username === "agent" && password === "agent123") {
    state.isAgentAuthenticated = true
    localStorage.setItem("agentAuthenticated", "true")
    document.getElementById("login-form").reset()
    errorMsg.classList.add("hidden")
    updateAuthUI()
  } else {
    errorMsg.classList.remove("hidden")
  }
}

function handleLogout() {
  state.isAgentAuthenticated = false
  localStorage.setItem("agentAuthenticated", "false")
  updateAuthUI()
}

function setupEventListeners() {
  const loginForm = document.getElementById("login-form")
  if (loginForm) {
    loginForm.addEventListener("submit", handleAgentLogin)
  }

  const logoutBtn = document.getElementById("logout-btn")
  if (logoutBtn) {
    logoutBtn.addEventListener("click", handleLogout)
  }

  const chatItems = document.querySelectorAll(".chat-item")
  if (chatItems && chatItems.length) {
    chatItems.forEach((item) => {
      item.addEventListener("click", (e) => selectChat(e.currentTarget.dataset.chatId))
    })
  }

  const suggestionBtns = document.querySelectorAll(".suggestion-btn")
  if (suggestionBtns && suggestionBtns.length) {
    suggestionBtns.forEach((btn) => {
      btn.addEventListener("click", (e) => insertSuggestion(e.target.textContent))
    })
  }
}

function selectChat(chatId) {
  state.currentChatId = chatId

  document.querySelectorAll(".chat-item").forEach((item) => item.classList.remove("active"))
  document.querySelector(`[data-chat-id="${chatId}"]`).classList.add("active")

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
