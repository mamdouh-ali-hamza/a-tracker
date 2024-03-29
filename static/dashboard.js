const welcomeDashboard = document.getElementById("welcome-dashboard");
const usernameWelcome = document.createElement("h3");

usernameWelcome.innerText = "Welcome, " + localStorage.getItem("username");
welcomeDashboard.appendChild(usernameWelcome);

document.getElementById("dateSelected").valueAsDate = new Date();

let username = localStorage.getItem("username");
document.getElementById("pleaseEnter").style.display = "none";

if (username == null) {
  document.getElementById("welcome-dashboard").style.display = "none";
  document.getElementById("addNav").style.display = "none";
  document.getElementById("allNav").style.display = "none";
  document.getElementById("dashboardNav").style.display = "none";
  document.getElementById("allDashboard").style.display = "none";
  document.getElementById("pleaseEnter").style.display = "inline";
}

// Function to open the popup
document.addEventListener("DOMContentLoaded", function () {
  const openPopupBtn = document.getElementById("openPopupBtn");
  const closePopupBtn = document.getElementById("closePopupBtn");
  const popup = document.getElementById("popup");
  const overlay = document.getElementById("overlay");

  openPopupBtn.addEventListener("click", function () {
    popup.style.display = "block";
    overlay.style.display = "block";
  });

  closePopupBtn.addEventListener("click", function () {
    popup.style.display = "none";
    overlay.style.display = "none";
  });

  // Close the popup if the user clicks outside the popup
  window.addEventListener("click", function (event) {
    if (event.target === overlay) {
      popup.style.display = "none";
      overlay.style.display = "none";
    }
  });
});
