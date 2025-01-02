document.addEventListener("DOMContentLoaded", () => {
    const uploadButton = document.querySelector("button");
    const fileInput = document.querySelector('input[type="file"]');
    const form = document.querySelector("form");

    uploadButton.addEventListener("click", (e) => {
        if (!fileInput.value) {
            alert("Please select a file before submitting!");
            e.preventDefault();
        }
    });
});
