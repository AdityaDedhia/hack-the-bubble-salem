const joinGameButton = document.getElementById('join-game');
const mainContainer = document.getElementById('main-container');
let formDiv = document.getElementById('form-div');
let usernameForm = document.getElementById('username-form');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

joinGameButton.addEventListener('click', () => {
    joinGameButton.classList.toggle('hidden');
    formDiv.classList.toggle('hidden');
});

usernameForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const formData = new FormData(usernameForm);
    formData.append("username", username);

    await fetch('/add_client', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: formData
    });

    mainContainer.innerHTML = "";
    const waitingMessage = document.createElement('div');
    waitingMessage.innerHTML = `<h1 data-aos="fade-in" class="font-bold text-3xl text-slate-50 text-center mt-10 p-2 rounded-2xl max-w-fit" style="font-family: HeaderFont, sans-serif">Waiting for other players to join</h1>`
    mainContainer.appendChild(waitingMessage);
    fetch('/get_clients_size')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
});




