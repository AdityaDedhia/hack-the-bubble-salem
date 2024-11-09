const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
async function selectRole(){
    fetch(`${window.location.origin}/attempt_assign_role`,{
        method: "POST",
        headers:{
            role: this.id,
            'X-CSRFToken': csrftoken
        }
    })
}