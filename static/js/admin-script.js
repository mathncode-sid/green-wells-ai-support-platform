const state = {
  isAdminAuthenticated: false,
}

function initAdmin() {
  loadAuthenticationState()
  setupEventListeners()
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initAdmin)
} else {
  initAdmin()
}

function loadAuthenticationState() {
  const isAuthenticated = localStorage.getItem("adminAuthenticated") === "true"
  state.isAdminAuthenticated = isAuthenticated
  updateAuthUI()
}

function updateAuthUI() {
  const loginModal = document.getElementById("login-modal")
  const navbar = document.getElementById("navbar")
  const adminDashboard = document.getElementById("admin-dashboard")

  // Defensive: elements may be missing on some pages. Only manipulate if present.
  if (state.isAdminAuthenticated) {
    if (loginModal) loginModal.classList.add("hidden")
    if (navbar) navbar.classList.remove("hidden")
    if (adminDashboard) {
      // `.view` elements use the `.active` class to be displayed. Keep both for compatibility.
      adminDashboard.classList.remove("hidden")
      adminDashboard.classList.add("active")
      generateChartData()
    }
  } else {
    if (loginModal) loginModal.classList.remove("hidden")
    if (navbar) navbar.classList.add("hidden")
    if (adminDashboard) {
      adminDashboard.classList.remove("active")
      adminDashboard.classList.add("hidden")
    }
  }
}

function handleAdminLogin(e) {
  e.preventDefault()
  const username = document.getElementById("login-username").value
  const password = document.getElementById("login-password").value
  const errorMsg = document.getElementById("login-error")

  if (username === "admin" && password === "admin123") {
    state.isAdminAuthenticated = true
    localStorage.setItem("adminAuthenticated", "true")
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
  updateAuthUI()
}

function setupEventListeners() {
  const loginForm = document.getElementById("login-form")
  if (loginForm) {
    loginForm.addEventListener("submit", handleAdminLogin)
  }

  const logoutBtn = document.getElementById("logout-btn")
  if (logoutBtn) {
    logoutBtn.addEventListener("click", handleLogout)
  }

  const sidebarItems = document.querySelectorAll(".sidebar-item")
  if (sidebarItems && sidebarItems.length) {
    sidebarItems.forEach((item) => {
      item.addEventListener("click", (e) => switchAdminSection(item.dataset.section))
    })
  }
}

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
