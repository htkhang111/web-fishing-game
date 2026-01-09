// frontend/static/js/main.js

document.addEventListener("DOMContentLoaded", function() {
    console.log("Web Fishing Game - Main JS loaded successfully!");

    // Tự động tắt thông báo (Flash messages) sau 3 giây
    const alerts = document.querySelectorAll('.alert');
    if (alerts) {
        setTimeout(() => {
            alerts.forEach(alert => {
                alert.style.opacity = '0';
                setTimeout(() => alert.style.display = 'none', 500);
            });
        }, 3000);
    }
});