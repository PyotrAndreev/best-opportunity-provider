let opportunity_id = undefined

function loadOpportunityDump() {
    let dump = JSON.parse(document.getElementById("opportunity-dump").innerHTML)
    opportunity_id = dump["opportunity_id"]
}

function transformTags() {
    const tagsContainer = document.getElementById("tags-container")
    const tagsJSON = tagsContainer.children[0].innerText
    let tags = JSON.parse(tagsJSON)
    for (let tag_id in tags) {
        let tag = createTag(tag_id, tags[tag_id])
        tag.onclick = () => {
            document.location.href = `/opportunities?tag_ids=${tag_id}`
        }
        tagsContainer.appendChild(tag)
    }
    tagsContainer.removeChild(tagsContainer.children[0])
}

function transformGeotags() {
    const geotagsContainer = document.getElementById("geotags-container")
    const tagsJSON = geotagsContainer.children[0].innerText
    let geotags = JSON.parse(tagsJSON)
    for (let geotag_id in geotags) {
        let geotag = createGeotag(geotag_id, geotags[geotag_id])
        geotag.onclick = () => {
            document.location.href = `/opportunities?geotag_ids=${geotag_id}`
        }
        geotagsContainer.appendChild(geotag)
    }
    geotagsContainer.removeChild(geotagsContainer.children[0])
}

function getDescription() {
    const descriptionContainer = document.getElementById("description-container")
    fetch(`/api/opportunity/description?opportunity_id=${opportunity_id}`, {
        method: "GET"
    })
    .then(async (response) => {
        if (response.status === 200) {
            descriptionContainer.innerHTML = (new showdown.Converter()).makeHtml(await response.text())
            return
        }
        descriptionContainer.textContent = "Some error occured, refresh page to see opportunity description"
    })
}

function getForm() {
    const formContainer = document.getElementById("form-container")
    fetch(`/api/opportunity/form?opportunity_id=${opportunity_id}`, {
        method: "GET"
    })
    .then(async (response) => {
        if (response.status === 200) {
            formContainer.innerHTML = await response.text()
            // let submitButton = document.getElementById("form-submit-button")
            // submitButton.addEventListener('click', submitOpportunityForm)
            return
        }
        formContainer.textContent = "Some error occured, refresh page to see opportunity response form"
    })
}

function submitOpportunityForm() {
    const fieldsContainer = document.getElementById("form-fields-container")
    formData = {}
    formData['opportunity_id'] = opportunity_id
    formData['data'] = {}
    for (let child of fieldsContainer.children) {
        const field_data = child.getElementsByClassName("form-field-data")
        const select_data = child.getElementsByClassName("form-select-data")[0]
        const errorsField = child.getElementsByClassName("form-field-errors")
        if (errorsField.length != 1) {
            getForm()
            return
        }
        errorsField[0].innerText = ""
        if (field_data.length > 0) {
            formData['data'][child.getAttribute('field_name')] = field_data[0].value;
        } else {
            formData['data'][child.getAttribute('field_name')] = select_data.options[select_data.selectedIndex].text;
        }
    }
    fetch(`/api/opportunity-response`, {
        method: "POST",
        body: JSON.stringify(formData),
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
        },
    })
    .then(async (response) => {
        if (response.status === 200) {
            getForm()
            return
        }
        response_json = await response.json()
        Object.keys(response_json).forEach(key => {
            response_json[key].forEach(error => {
                const form_field = fieldsContainer.querySelectorAll(`[field_name=${key}]`)
                if (form_field.length == 1) {
                    errorsField = form_field[0].getElementsByClassName("form-field-errors")
                    if (errorsField.length != 1) {
                        getForm()
                        return
                    }
                    errorsField[0].innerText += error['message']
                } else {
                    getForm()
                    return
                }
            })
        })
    })
}

document.addEventListener("DOMContentLoaded", () => {
    loadOpportunityDump()
    transformTags()
    transformGeotags()
    getDescription()
    getForm()
})
