document.addEventListener("DOMContentLoaded", function () {
    let sidebar = document.getElementById("sidebar");
    let toggleBtn = document.querySelector(".sidebar-toggle-btn");

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener("click", function (event) {
            sidebar.classList.toggle("active");
            event.stopPropagation(); // Prevents immediate closing
        });

        document.addEventListener("click", function (event) {
            if (!sidebar.contains(event.target) && !toggleBtn.contains(event.target)) {
                sidebar.classList.remove("active");
            }
        });
    }

    // ✅ Extract success parameter from URL (For notifications)
    const urlParams = new URLSearchParams(window.location.search);
    const successMessage = urlParams.get("success");

    if (successMessage === "saved") {
        showNotification("✅ Post has been saved!", "green");
    } else if (successMessage === "unsaved") {
        showNotification("❌ Post has been unsaved!", "red");
    }

    function showNotification(message, color) {
        let notification = document.getElementById("notification");
        if (notification) {
            notification.textContent = message;
            notification.style.backgroundColor = color;
            notification.style.display = "block";
            notification.style.opacity = "1";

            setTimeout(() => {
                let fadeEffect = setInterval(() => {
                    let opacity = parseFloat(notification.style.opacity);
                    if (opacity > 0) {
                        notification.style.opacity = (opacity - 0.1).toString();
                    } else {
                        clearInterval(fadeEffect);
                        notification.style.display = "none";
                    }
                }, 50);
            }, 3000);
        }
    }
});

