const usernameText = document.getElementById("usernameText");
const buttonEnter = document.getElementById("buttonEnter");
const loginContainer = document.getElementById("loginContainer");
const loginChild = document.getElementById("loginChild");
const welcomeContainer = document.getElementById("welcomeContainer");
const welcome = document.getElementById("welcome");

const buttonExit = document.createElement("input");




//
function display(){
    const welcomeMessage = document.createElement("p");
    welcomeMessage.innerText = "Welcome, " + localStorage.getItem("username");
    welcomeMessage.className = "group";
    welcomeContainer.appendChild(welcomeMessage);

    const goToDashboardForm = document.createElement("form");
    goToDashboardForm.setAttribute("method", "get");
    goToDashboardForm.setAttribute("action", "/dashboard");

    const goToDashboard = document.createElement("input");
    goToDashboard.setAttribute("type", "submit");
    goToDashboard.setAttribute("value", "Go To Dashboard");
    goToDashboard.className = "button"
    
    goToDashboardForm.appendChild(goToDashboard);
    welcomeContainer.appendChild(goToDashboardForm);
    
    buttonExit.setAttribute("type", "button");
    buttonExit.setAttribute("value" , "Exit");
    buttonExit.setAttribute("id", "buttonExit");
    welcomeContainer.appendChild(buttonExit);
}


//
function addUser(){
    if(usernameText.value != ""){
        localStorage.setItem("username", usernameText.value);
        usernameText.value = "";                                                        // text field to become empty after use

        display();

        loginContainer.removeChild(loginChild);                                     // remove text box and login button
        welcomeContainer.removeChild(welcome);

        location.reload();
    }
    
}


//
function exitUser(){
    localStorage.clear();
    location.reload();
}





//
usernameText.value = "";

let username = localStorage.getItem("username");                            // check if user logged in

if(username != null){
    loginContainer.removeChild(loginChild);                                 // remove text box and login button
    welcomeContainer.removeChild(welcome);

    display();
}


//
buttonEnter.addEventListener("click", addUser);


//
buttonExit.addEventListener("click", exitUser);





document.getElementById("pleaseEnter").style.display = "none";

if(username == null){
    document.getElementById("welcomDashboard").style.display = "none";
    document.getElementById("addNav").style.display = "none";
    document.getElementById("allNav").style.display = "none";
    document.getElementById("dashboardNav").style.display = "none";
    document.getElementById("pleaseEnter").style.display = "inline";
}







// Function to open the popup
document.addEventListener("DOMContentLoaded", function() {
    const openPopupBtn = document.getElementById("openPopupBtn");
    const closePopupBtn = document.getElementById("closePopupBtn");
    const popup = document.getElementById("popup");
    const overlay = document.getElementById("overlay");

    openPopupBtn.addEventListener("click", function() {
        popup.style.display = "block";
        overlay.style.display = "block";
    });

    closePopupBtn.addEventListener("click", function() {
        popup.style.display = "none";
        overlay.style.display = "none";
    });

    // Close the popup if the user clicks outside the popup
    window.addEventListener("click", function(event) {
        if (event.target === overlay) {
            popup.style.display = "none";
            overlay.style.display = "none";
        }
    });
});









function openTab(tabName) {
    var tabs = document.getElementsByClassName("form-group");
    
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].style.display = "none";
    }

    document.getElementById(tabName).style.display = "block";

    // Remove "active" class from all tabs
    var tabButtons = document.getElementsByClassName("tab");
    for (var i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove("active");
    }

    // Add "active" class to the clicked tab
    document.querySelector(`.tab[href="#"][onclick*='${tabName}']`).classList.add("active");
}

// function login() {
//     // Add your login logic here
//     alert("Login button clicked");
// }

// function register() {
//     // Add your registration logic here
//     alert("Register button clicked");
// }

// Initially, open the login tab
openTab("login-form");



const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");
const buttonLogin = document.getElementById("buttonLogin");
const buttonRegister = document.getElementById("buttonRegister");
const registerName = document.getElementById("register-name");
const loginName = document.getElementById("login-name");


function submitRegister(){
    registerForm.submit();
}
buttonRegister.addEventListener("click", submitRegister);

function submitLogin(){
    localStorage.setItem("name", loginName.value);
    loginForm.submit();
}
buttonLogin.addEventListener("click", submitLogin);











// Function to display flash messages
document.addEventListener('DOMContentLoaded', function() {
    // Function to display flash messages
    function displayFlashMessage(message, messageType) {
        var container = document.getElementById('flash-messages');

        var alertDiv = document.createElement('div');
        alertDiv.className = 'alert';
        alertDiv.classList.add('alert-' + messageType);
        alertDiv.innerHTML = message;

        container.appendChild(alertDiv);

        // Hide the message after 5 seconds
        setTimeout(function() {
            container.removeChild(alertDiv);
        }, 5000);
    }

    // Fetch and display flash messages on page load
    var urlParams = new URLSearchParams(window.location.search);
    var flashMessage = urlParams.get('flash_message');
    if (flashMessage) {
        displayFlashMessage(flashMessage, 'success');  // You may adjust 'success' based on your message type
    }
});

