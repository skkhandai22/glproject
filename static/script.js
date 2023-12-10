function showInsertForm() {
    document.getElementById('insertForm').style.display = 'block';
    document.getElementById('fetchForm').style.display = 'none';
}

function showFetchForm() {
    document.getElementById('fetchForm').style.display = 'block';
    document.getElementById('insertForm').style.display = 'none';
}

function submitInsertDetails() {
    // Get values from the form
    const email = document.getElementById('email').value;
    const mobile = document.getElementById('mobile').value;
    const name = document.getElementById('name').value;
    const workauth = document.getElementById('workauth').value;
    const annualrate = document.getElementById('annualrate').value;
    const hourlyrate = document.getElementById('hourlyrate').value;
    const relocate = document.getElementById('relocate').value;
    const location = document.getElementById('location').value;

    // Send data to the backend API
    fetch('/eximius/api/inputcandidatedetail', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email,
            mobile,
            name,
            workauth,
            annualrate,
            hourlyrate,
            relocate,
            location,
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Display the response message on the UI
        document.getElementById('insertMessage').innerText = data.message;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('insertMessage').innerText = 'Error occurred.';
    });
}

function submitFetchDetails() {
    // Get value from the form
    const fetchEmail = document.getElementById('fetchEmail').value;

    // Send data to the backend API
    fetch('/eximius/api/getData/findcandidatedetail', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: fetchEmail,
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Display the response on the UI
        if (data.message) {
            document.getElementById('fetchMessage').innerText = data.message;
        } else {
            // Assuming the data is displayed in a div
            document.getElementById('fetchMessage').innerText = JSON.stringify(data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('fetchMessage').innerText = 'Error occurred.';
    });
}
