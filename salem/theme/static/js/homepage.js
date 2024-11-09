const joinGameButton = document.getElementById('join-game');
const mainContainer = document.getElementById('main-container');
let formDiv = document.getElementById('form-div');
let usernameForm = document.getElementById('username-form');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
let previousClientSize = 0;
const playerLimit = 1;

setInterval(()=>{
    fetch('check_user',{
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
        }
    })
}, 3000)

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
    waitingMessage.innerHTML = `
    <h1 data-aos="fade-in" class="font-bold text-3xl text-slate-50 text-center mt-10 p-2 rounded-2xl max-w-fit" style="font-family: HeaderFont, sans-serif">Waiting for other players to join</h1>
    <h2 id="clientSize" class="font-bold text-3xl text-slate-50 text-center mt-2 p-2 rounded-2xl max-w-fit">Test</h2>
`
    fetchClientSize();
    mainContainer.appendChild(waitingMessage);
});

function fetchClientSize() {
    fetch('/get_clients_size', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            // If the client size has changed, update it
            updateUI(data.clients_size);
            if (data.clients_size == playerLimit){
                window.location.href = "/main"
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Function to update the UI with the new client size
function updateUI(clientSize) {
    const resultElement = document.getElementById('clientSize');
    resultElement.textContent = `Current Client Size: ${clientSize}/12`;
}

// Set the interval to call fetchClientSize every 5 seconds (5000ms)
setInterval(fetchClientSize, 5000);



