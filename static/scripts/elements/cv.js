function createCV(id, name) {
    let container = document.createElement("div")
    container.className += "cv-container"
    container.setAttribute("cv_id", id)
    let name_container = document.createElement("div")
    let name_input = document.createElement("input")
    name_input.type = "text"
    name_input.className = "cv-name"
    name_input.placeholder = "CV name"
    name_input.value = name
    let name_errors = document.createElement("p")
    let rename_button = document.createElement("button")
    rename_button.className = "cv-save"
    rename_button.innerText = "Rename"
    rename_button.onclick = () => {
        fetch(`/api/cv/name?cv_id=${id}`, {
            method: "PATCH",
            body: JSON.stringify({
                name: name_input.value
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8",
            },
        })
        .then(async (response) => {
            if (response.status === 200) {
                alert('Successfully updated CV, reload page to see changes')
                return
            }
            response_json = await response.json()
            Object.keys(response_json).forEach(key => {
                if (key === 'cv_id') {
                    updateCVList()
                    return
                } else if (key === 'name') {
                    name_errors.innerText = response_json[key][0]['message']
                }
            })
        })
    }
    let delete_button = document.createElement("button")
    delete_button.className = "cv-delete"
    delete_button.innerText = "Delete"
    delete_button.onclick = () => {
        fetch(`/api/cv?cv_id=${id}`, {
            method: "DELETE"
        })
        .then(async (response) => {
            if (response.status === 200) {
                updateCVList()
                return
            }
            response_json = await response.json()
            Object.keys(response_json).forEach(key => {
                if (key === 'cv_id') {
                    updateCVList()
                    return
                }
            })
        })
    }
    name_container.appendChild(name_input)
    name_container.appendChild(name_errors)
    container.appendChild(name_container)
    container.appendChild(rename_button)
    container.appendChild(delete_button)
    return container
}
