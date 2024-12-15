function createFilterItem(id, name, callback, selected) {
    let filter = document.createElement("div")
    filter.className = "filter-item"
    if (selected) {
        filter.classList.add("selected")
    }
    filter.onclick = () => {
        if (callback(id)) {
            filter.classList.add("selected")
        } else {
            filter.classList.remove("selected")
        }
    }
    let filter_text = document.createElement("p")
    filter_text.innerText = name
    filter.appendChild(filter_text)
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
