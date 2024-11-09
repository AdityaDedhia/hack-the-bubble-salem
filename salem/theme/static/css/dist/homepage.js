const joinGameButton = document.getElementById('join-game');
const mainContainer = document.getElementById('main-container');
let usernameForm;

joinGameButton.addEventListener('click', () => {
    joinGameButton.classList.toggle('hidden');
    usernameForm = document.createElement('form');
    usernameForm.innerHTML = `<div style="gap: 10px" class="flex flex-col items-center p-4 bg-gray-100 rounded-lg shadow-lg max-w-sm mx-auto">
    <form id="username-form">
    <label for="username" class="mb-2 text-xl font-semibold text-slate-50">Username:</label>
    <input
        type="text"
        id="username"
        name="username"
        required
        class="w-full text-xl px-4 py-2 mb-4 border border-gray-300 rounded-2xl focus:outline-none focus:border-blue-500"
        placeholder="Enter your username"
    >
    <button
        type="submit"
        class="px-6 py-2 text-white bg-blue-500 text-xl rounded-md hover:bg-blue-600 transition duration-300"
    >
        Submit
    </button>
</form>
</div>`;
    mainContainer.appendChild(usernameForm);
    usernameForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        mainContainer.innerHTML = "";
        const waitingMessage = document.createElement('div');
        waitingMessage.innerHTML = `<h1 data-aos="fade-in" class="font-bold text-3xl text-slate-50 text-center mt-10 p-2 rounded-2xl max-w-fit" style="font-family: HeaderFont, sans-serif">Waiting for other players to join</h1>`
        mainContainer.appendChild(waitingMessage);
        const playerCount = await fetch('/get_clients_size')
            .then((response => response.json())
                .then(data => {
                        let clients_size = data.clients_size;
                        console.log(clients_size);
                    }
                ));
    });
});




