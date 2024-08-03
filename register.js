document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent form from submitting the traditional way

    // Get the registration details
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // For simplicity, store the user data in localStorage (not secure for real applications)
    localStorage.setItem('username', username);
    localStorage.setItem('email', email);
    localStorage.setItem('password', password);

    alert('User registered successfully!');

    // Redirect to the home page
    window.location.href = 'index.html';
});
