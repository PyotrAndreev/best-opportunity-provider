let opportunity_id = undefined
let defaultTabId = 0
let activeTabId = 0

function loadOpportunityDump() {
    let dump = JSON.parse(document.getElementById("opportunity-dump").innerHTML)
    opportunity_id = dump.id
    console.log(dump)

    const form_title_container = document.getElementById("opportunity-form-name")
    let form_title = document.createElement("p")
    form_title.innerText = dump.name;
    form_title_container.appendChild(form_title)

    const provider_container = document.getElementById("provider-container")
    let provider_logo = document.createElement("img")
    provider_logo.id = "provider-logo"
    provider_logo.src = dump.provider_logo_url
    let provider_name = document.createElement("p")
    provider_name.innerText = dump.provider_name
    provider_container.appendChild(provider_logo)
    provider_container.appendChild(provider_name)

    const tags_container = document.getElementById("tags-container")
    for (let [id, name] of Object.entries(dump.tags)) {
        tags_container.appendChild(createTag(id, name))
    }

    const geotags_container = document.getElementById("geotags-container")
    for (let [id, name] of Object.entries(dump.geotags)) {
        geotags_container.appendChild(createGeotag(id, name))
    }

    const form_link = document.getElementById("opportunity-link")
    if (dump.link) {
        form_link.innerText = dump.link
        form_link.href = dump.link
    } else {
        form_link.innerText = "no link provided"
    }
}

function transformTags() {
    const tagsContainer = document.getElementById("tags-container")
    if (tagsContainer.childNodes.length === 0) {
        return
    }
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
    if (geotagsContainer.childNodes.length === 0) {
        return
    }
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

function createStringField(name, data) {
    let string_form_fields = document.createElement("div")
    string_form_fields.classList.add("string-form-field")
    string_form_fields.setAttribute("field_name", name)
    let form_label_data = document.createElement("p")
    form_label_data.innerText = data["label"]
    form_label_data.classList.add("form-label-data")
    let form_field_data = document.createElement("input")
    form_field_data.classList.add("form-field-data")
    form_field_data.type = "text"
    if (data["max_length"]) {
        form_field_data.maxLength = data["max_length"]
    }
    if (data["is_required"]) {
        form_field_data.setAttribute("is_required", data["is_required"])
    }
    let form_field_errors = document.createElement("p")
    form_field_errors.classList.add("form-field-errors")

    string_form_fields.appendChild(form_label_data)
    string_form_fields.appendChild(form_field_data)
    string_form_fields.appendChild(form_field_errors)

    return string_form_fields
}

function createRegexField(name, data) {
    let string_form_fields = document.createElement("div")
    string_form_fields.classList.add("regex-form-field")
    string_form_fields.setAttribute("field_name", name)
    let form_label_data = document.createElement("p")
    form_label_data.innerText = data["label"]
    form_label_data.classList.add("form-label-data")
    let form_field_data = document.createElement("input")
    form_field_data.classList.add("form-field-data")
    form_field_data.type = "text"
    form_field_data.pattern = data["regex"]
    if (data["max_length"]) {
        form_field_data.maxLength = data["max_length"]
    }
    if (data["is_required"]) {
        form_field_data.setAttribute("is_required", data["is_required"])
    }
    let form_field_errors = document.createElement("p")
    form_field_errors.classList.add("form-field-errors")

    string_form_fields.appendChild(form_label_data)
    string_form_fields.appendChild(form_field_data)
    string_form_fields.appendChild(form_field_errors)

    return string_form_fields
}

function createChoiceField(name, data) {
    let choice_form_field = document.createElement("div")
    choice_form_field.classList.add("choice-form-field")
    choice_form_field.setAttribute("field_name", name)

    let form_label_data = document.createElement("p")
    form_label_data.classList.add("form-label-data")
    form_label_data.innerText = data["label"]

    let form_select_data = document.createElement("select")
    form_select_data.classList.add("form-select-data")

    for (let option of data["choices"]) {
        let choice_field = document.createElement("option")
        choice_field.innerText = option
        form_select_data.appendChild(choice_field)
    }

    let form_field_errors = document.createElement("p")
    form_field_errors.classList.add("form-field-errors")

    choice_form_field.appendChild(form_label_data)
    choice_form_field.appendChild(form_select_data)
    choice_form_field.appendChild(form_field_errors)

    return choice_form_field
}

function getForm() {
    const formContainer = document.getElementById("form-container")
    fetch(`/api/opportunity/form?opportunity_id=${opportunity_id}`, {
        method: "GET"
    })
    .then(async (response) => {
        if (response.status === 200) {
            const form_data = JSON.parse(await response.text())
            // formContainer.innerText = form_data

            let form_fields_container = document.createElement("div")
            form_fields_container.id = "form-fields-container"
            console.log(form_data)
            for (let [name, field] of Object.entries(form_data['fields'])) {
                if (field["type"] === "string") {
                    form_fields_container.appendChild(createStringField(name, field))
                } else if (field["type"] === "regex") {
                    form_fields_container.appendChild(createRegexField(name, field))
                } else if (field["type"] === "choice") {
                    form_fields_container.appendChild(createChoiceField(name, field))
                }
            }

            formContainer.appendChild(form_fields_container)

            if (!form_data["already_responded"]) {
                let form_submit_button = document.createElement("button")
                form_submit_button.id = "form-submit-button"
                form_submit_button.innerText = "Submit"
                formContainer.appendChild(form_submit_button)
            }

            let submitButton = document.getElementById("form-submit-button")
            submitButton.addEventListener('click', submitOpportunityForm)
            return
        }
        formContainer.textContent = "Some error occured, refresh page to see opportunity response form"
    })
}

function createErrorBlock(error_string) {
    const p_block = document.createElement("p");
    p_block.innerText = error_string;
    return p_block;
}

function submitOpportunityForm() {
    const fieldsContainer = document.getElementById("form-fields-container")
    formData = {}
    formData['response_data'] = {}
    for (let child of fieldsContainer.children) {
        const field_data = child.getElementsByClassName("form-field-data")
        const select_data = child.getElementsByClassName("form-select-data")[0]
        const errorsField = child.getElementsByClassName("form-field-errors")
        if (errorsField.length != 1) {
            getForm()
            return
        }
        errorsField[0].innerText = ""
        const classAttr = child.getAttribute("class")
        console.log(classAttr)

        if (classAttr === "string-form-field") {
            const string_field = child.getElementsByClassName("form-field-data")[0]

            is_required = string_field.getAttribute("is_required")
            if (is_required && !string_field.checkValidity() || string_field.value === "") {
                const string_label = child.getElementsByClassName("form-label-data")[0]
                const string_errors = child.getElementsByClassName("form-field-errors")[0]
                if (is_required && string_field.value === "") {
                    string_errors.appendChild(createErrorBlock(string_label.innerText + " field is required"))
                }
                return;
            }
        }  else if (classAttr === "regex-form-field") {
            const regex_field = child.getElementsByClassName("form-field-data")[0]
            is_required = regex_field.getAttribute("is_required")
            if (is_required && !regex_field.checkValidity() || regex_field.value === "") {
                const regex_errors = child.getElementsByClassName("form-field-errors")[0]
                const regex_label = child.getElementsByClassName("form-label-data")[0]
                if (is_required && regex_field.value === "") {
                    regex_errors.appendChild(createErrorBlock(regex_label.innerText + " field is required"));
                } else if (!regex_field.checkValidity()) {
                    regex_errors.appendChild(createErrorBlock(regex_label.innerText + " not validated"));
                }
                return;
            }
        }

        if (field_data.length > 0) {
            formData['response_data'][child.getAttribute('field_name')] = field_data[0].value;
        } else {
            formData['response_data'][child.getAttribute('field_name')] = select_data.options[select_data.selectedIndex].text;
        }
    }
    fetch(`/api/opportunity-response?opportunity_id=${opportunity_id}`, {
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

function activateTab(button, tabId) {
    let tab = document.getElementsByClassName("tab-content")[tabId]
    tab.style.display = "block";
    button.classList.add("active")
    activeTabId = tabId;
}

function deactivateTab(tabId) {
    let tab = document.getElementsByClassName("tab-content")[tabId]
    tab.style.display = "none";
    document.getElementsByClassName("tab-links")[tabId].classList.remove("active")
}

function changeTab(event, tabId) {
    deactivateTab(activeTabId)
    activateTab(event.currentTarget, tabId)
    activeTabId = tabId;
}

function setDefaultTab() {
    const defaultButton = document.getElementsByClassName("tab-links")[defaultTabId]
    activateTab(defaultButton, defaultTabId)
    activeTabId = defaultTabId;
}

document.addEventListener("DOMContentLoaded", () => {
    setDefaultTab()
    loadOpportunityDump()
    getDescription()
    getForm()
})
