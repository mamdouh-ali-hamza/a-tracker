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