document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(this); // Create a FormData object from the form

    try {
        const response = await fetch('/', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        if (data.success) {
            // Show the result image
            document.getElementById('results-message').textContent = 'Results:';
            const resultImage = document.getElementById('result-image');
            resultImage.src = data.image_url; // Set the image source to the returned URL
            resultImage.style.display = 'block'; // Show the image
        } else {
            alert(data.error || 'An unknown error occurred while processing the files.');
        }
    } catch (error) {
        alert('An error occurred while submitting the form: ' + error.message);
    }
});
