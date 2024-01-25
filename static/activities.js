const welcomDashboard = document.getElementById("welcomDashboard");
const usernameWelcome = document.createElement("h3");


const buttonDeleteLast = document.getElementById("buttonDeleteLast");
const backDeleteLast = document.getElementById("backDeleteLast");
const confirmDeleteLast = document.getElementById("confirmDeleteLast");
const buttonDeleteAll = document.getElementById("buttonDeleteAll");
const backDeleteAll = document.getElementById("backDeleteAll");
const confirmDeleteAll = document.getElementById("confirmDeleteAll");


// buttons not visible by default
backDeleteLast.style.display = "none";
confirmDeleteLast.style.display = "none";
backDeleteAll.style.display = "none";
confirmDeleteAll.style.display = "none";

// change buttons visible or not
buttonDeleteLast.addEventListener("click", function(){
    buttonDeleteLast.style.display = "none";
    backDeleteLast.style.display = "inline";
    confirmDeleteLast.style.display = "inline";
});
buttonDeleteAll.addEventListener("click", function(){
    buttonDeleteAll.style.display = "none";
    backDeleteAll.style.display = "inline";
    confirmDeleteAll.style.display = "inline";
});

backDeleteLast.addEventListener("click", function(){
    backDeleteLast.style.display = "none";
    confirmDeleteLast.style.display = "none";
    buttonDeleteLast.style.display = "inline";
});
backDeleteAll.addEventListener("click", function(){
    backDeleteAll.style.display = "none";
    confirmDeleteAll.style.display = "none";
    buttonDeleteAll.style.display = "inline";
});

// make the table scrolled down by default
let scrollContainer = document.getElementById('table-container');
scrollContainer.scrollTop = scrollContainer.scrollHeight;



usernameWelcome.innerText = "Welcome, " + localStorage.getItem("username");
welcomDashboard.appendChild(usernameWelcome);



let username = localStorage.getItem("username");
document.getElementById("pleaseEnter").style.display = "none";

if(username == null){
    document.getElementById("welcomDashboard").style.display = "none";
    document.getElementById("addNav").style.display = "none";
    document.getElementById("allNav").style.display = "none";
    document.getElementById("dashboardNav").style.display = "none";
    document.getElementById("allActivities").style.display = "none";
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