function createFilterItem(id, name, callback, selected) {
    let filter = document.createElement("div")
    filter.className = "filter-item"
    let filter_checkbox = document.createElement("input")
    filter_checkbox.type = "checkbox"
    if (selected) {
        filter.classList.add("selected")
        filter_checkbox.checked = true
    }
    filter.onclick = () => {
        if (callback(id)) {
            filter.classList.add("selected")
            filter_checkbox.checked = true
        } else {
            filter.classList.remove("selected")
            filter_checkbox.checked = false
        }
    }
    let filter_label = document.createElement("label")
    filter_label.innerText = name
    filter.appendChild(filter_checkbox)
    filter.appendChild(filter_label)
    return filter
}

function createFilterSearch(placeholder) {
    let search = document.createElement("div")
    search.className = "filter-search"
    let search_input = document.createElement("input")
    search_input.type = "text"
    search_input.placeholder = placeholder
    search.appendChild(search_input)
    return search
}
