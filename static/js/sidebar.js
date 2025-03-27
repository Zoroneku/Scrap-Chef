document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.querySelector(".sidebar-toggle-btn");
    const modal = document.getElementById("postModal");
    const vidModal = document.getElementById("vidPostModal");
    const notification = document.getElementById("notification");

    // Function to toggle the sidebar
    function toggleSidebar() {
        if (sidebar) {
            sidebar.classList.toggle("active");
        }
    }

    // Ensure the sidebar toggle button works
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener("click", function (event) {
            toggleSidebar();
            event.stopPropagation(); // Prevents sidebar from closing immediately
        });

        // Click outside to close sidebar
        document.addEventListener("click", function (event) {
            if (!sidebar.contains(event.target) && !toggleBtn.contains(event.target)) {
                sidebar.classList.remove("active");
            }
        });
    }

    // Open Post Modal
    function openPhotoPostModal() {
        if (modal) modal.style.display = 'block';
    }

    function openVidPostModal() {
        if (vidModal) vidModal.style.display = 'block';
    }

    // Close Post Modal (Click outside to close)
    function closePostModal(event) {
        if (!event || (modal && event.target === modal)) {
            modal.style.display = 'none';
        }
    }

    function closeVidPostModal(event) {
        if (!event || (vidModal && event.target === vidModal)) {
            vidModal.style.display = 'none';
        }
    }

    // Attach functions to global scope so they work with inline event handlers
    window.toggleSidebar = toggleSidebar;
    window.openPhotoPostModal = openPhotoPostModal;
    window.openVidPostModal = openVidPostModal;
    window.closePostModal = closePostModal;
    window.closeVidPostModal = closeVidPostModal;

    // ✅ Extract success parameter from URL (For notifications)
    const urlParams = new URLSearchParams(window.location.search);
    const successMessage = urlParams.get("success");

    if (successMessage && notification) {
        let message = "";
        let color = "";

        if (successMessage === "saved") {
            message = "✅ Post has been saved!";
            color = "green";
        } else if (successMessage === "unsaved") {
            message = "❌ Post has been unsaved!";
            color = "red";
        }

        if (message) {
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

