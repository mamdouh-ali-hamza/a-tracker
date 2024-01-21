const welcomDashboard = document.getElementById("welcomDashboard");

const usernameWelcome = document.createElement("h3");
usernameWelcome.innerText = "Welcome, " + localStorage.getItem("username");
welcomDashboard.appendChild(usernameWelcome);


// document.getElementById("dailyDate").valueAsDate = new Date();
// document.getElementById("dateField").valueAsDate = new Date();






 
// const usernameGet = document.getElementById("usernameGet");
// usernameGet.value = localStorage.getItem("username");

// const usernameGetAdd = document.getElementById("usernameGetAdd");
// usernameGetAdd.value = localStorage.getItem("username");


const nav = document.getElementById("nav");
const allDashboard = document.getElementById("allDashboard");

let username = localStorage.getItem("username");

if(username == null){
    nav.style.display = "none";
    allDashboard.style.display = "none";
}







