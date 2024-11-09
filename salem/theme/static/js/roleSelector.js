const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
async function selectRole(role){
    await fetch(`${window.location.origin}/attempt_assign_role/${role}`, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
}

async function selectRoles() {
    const results = ["investigator","lookout","sheriff",'disguiser', "escort", "medium"];
    for (let result of results){
        await fetch(`${window.location.origin}/attempt_assign_role/` + result, {
            method: "POST",
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: {
                tester: true
            }
        }).then(response => {
            if (response.status === 207) {
                // Toggle the hidden class
                document.getElementById(`${role}` + "/div").classList.add('hidden');
            }
        });
    }
}

setInterval(selectRoles, 3000)
