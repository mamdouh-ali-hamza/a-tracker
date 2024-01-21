const welcomDashboard = document.getElementById("welcomDashboard");

const usernameWelcome = document.createElement("h3");
usernameWelcome.innerText = "Welcome, " + localStorage.getItem("username");
welcomDashboard.appendChild(usernameWelcome);




const hide = document.getElementById("hide");

let username = localStorage.getItem("username");

if(username == null){
    hide.style.display = "none";
}