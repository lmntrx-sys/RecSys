document.getElementById('postForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent form from submitting the traditional way

    // Get the text from the textarea
    const postText = document.getElementById('postText').value;

    if (postText.trim() !== '') {
        // Create a new div for the post
        const postDiv = document.createElement('div');
        postDiv.className = 'post';
        postDiv.textContent = postText;

        // Add the new post to the top of the posts container
        const postsContainer = document.getElementById('posts');
        postsContainer.insertBefore(postDiv, postsContainer.firstChild);

        // Clear the textarea
        document.getElementById('postText').value = '';
    }
});
