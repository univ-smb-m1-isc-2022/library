document.querySelectorAll('.favorite-btn').forEach(btn => {
    btn.addEventListener('click', event => {
        const bookId = event.target.dataset.bookId;
        // event.target.style.backgroundColor = '#FF0066';
        // event.target.textContent = 'The book added';
        fetch('/dashboard', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'  // Set Content-Type header
            },
            body: JSON.stringify({ book_id: bookId })  
        }).then(response => {
            console.log("success")
            return response.json()  
        }).then(data => {
        });
    });
});

// var favoritesBtn = document.getElementById('favorites');
// favoritesBtn.addEventListener('click', function() {
//   fetch('/dashboard', {
//     method: 'POST',
//     body: JSON.stringify({button: 'favorites'}),
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({"favorites": "True"}) 
//   })
//   .then(function(response) {
//     console.log("clicked");
//     return response.json() 
//   });
// });

// document.getElementById("favorites-btn").addEventListener("click", function() {
//     var xhr = new XMLHttpRequest();
//     xhr.open("GET", "/favorites", true);
//     xhr.onreadystatechange = function() {
//       if (xhr.readyState === 4 && xhr.status === 200) {
//         // Do something with the response data
//         console.log(xhr.responseText);
//       }
//     };
//     xhr.send();
//   });