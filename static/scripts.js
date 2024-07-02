// scripts.js
document.getElementById('trainButton').addEventListener('click', function() {
    // Show the loading spinner
    document.getElementById('loadingSpinner').style.display = 'block';
    
    // Make an AJAX request to run the training
    fetch('/run_training', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // Hide the loading spinner
        document.getElementById('loadingSpinner').style.display = 'none';
        
        // Display a message to the user
        let message = `Training completed. Best model: ${data.model_name}`;
        document.getElementById('trainingMessage').innerText = message;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('loadingSpinner').style.display = 'none';
        alert('An error occurred during training.');
    });
});
