function getRandomColor() {
    var letters = 'BCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * letters.length)];
    }
    return color;
}

window.onload = function() {
    var buttonsContainer = document.getElementById('grid-buttons');
    // Function to update button color
    function updateButtonColor(button, color) {
        button.style.backgroundColor = color;
    }

    for (var i = 0; i < 16; i++) {
        var button = document.createElement('button');
        button.className = 'btn';
        button.textContent = 'Button ' + (i);
        button.onclick = (function(index) {
            return function() {
                sendRequest(index);
            };
        })(i);
        updateButtonColor(button, getRandomColor());
        buttonsContainer.appendChild(button);
    }

    // Function to send request
    function sendRequest(buttonNumber) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "http://192.168.69.1:80/api", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({
            button: buttonNumber
        }));

        xhr.onload = function() {
            if (xhr.status != 200) {
                console.log(`Error ${xhr.status}: ${xhr.statusText}`);
            } else {
                var response = JSON.parse(xhr.responseText);
                console.log(`Response: ${xhr.responseText}`);
                updateButtonColor(response.button, response.color);
            }
        };
    }
};
