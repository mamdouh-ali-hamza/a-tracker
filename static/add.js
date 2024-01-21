document.getElementById("dateField").valueAsDate = new Date();


const welcomDashboard = document.getElementById("welcomDashboard");

const usernameWelcome = document.createElement("h3");
usernameWelcome.innerText = "Welcome, " + localStorage.getItem("username");
welcomDashboard.appendChild(usernameWelcome);



const nav = document.getElementById("nav");
const all = document.getElementById("all");

let username = localStorage.getItem("username");

if(username == null){
    nav.style.display = "none";
    all.style.display = "none";
}







// document.getElementById('addForm').addEventListener('submit', function (event) {
//     event.preventDefault(); // Prevent the default form submission

//     // Show the notification
//     showNotification('Activity added successfully!');
// });

// function showNotification(message) {
//     var notification = document.getElementById('notification');
//     notification.innerHTML = message;
//     notification.style.display = 'block';

//     // Hide the notification after 3 seconds (adjust as needed)
//     setTimeout(function () {
//         notification.style.display = 'none';
//     }, 3000);
// }