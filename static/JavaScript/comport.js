document.addEventListener("DOMContentLoaded", function () {
    const submenuToggle = document.getElementById("submenuToggle");
    const submenu = document.getElementById("submenu");

    submenuToggle.addEventListener("click", function () {
        submenu.style.display = submenu.style.display === "none" || submenu.style.display === "" ? "block" : "none";
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach((message) => {
        setTimeout(() => {
            message.classList.add('fade-out');
            setTimeout(() => message.remove(), 500); // Elimina el mensaje tras desvanecer
        }, 3000);
    });
});