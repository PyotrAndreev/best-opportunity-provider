const filter_items = {
    providers: {},
    tags: {},
    geotags: {}
}
let filters = {
    providers: new Set(),
    tags: new Set(),
    geotags: new Set(),
    page: 1
}

function copy_filters(filters) {
    return {
        providers: new Set(filters.providers),
        tags: new Set(filters.tags),
        geotags: new Set(filters.geotags),
        page: filters.page
    }
}

function same_filters(other) {
    return equalSets(filters.providers, other.providers) &&
        equalSets(filters.tags, other.tags) &&
        equalSets(filters.geotags, other.geotags) &&
        filters.page === other.page
}

function serialize_filters() {
    let str = []
    for (let id of filters.providers) {
        str.push(`provider_ids=${id}`)
    }
    for (let id of filters.tags) {
        str.push(`tag_ids=${id}`)
    }
    for (let id of filters.geotags) {
        str.push(`geotag_ids=${id}`)
    }
    str.push(`page=${filters.page}`)
    return "?" + str.join("&")
}

function loadFiltersDump() {
    let dump = JSON.parse(document.getElementById("filters-dump").innerHTML)
    Object.assign(filter_items.providers, dump.providers)
    Object.assign(filter_items.tags, dump.tags)
    Object.assign(filter_items.geotags, dump.geotags)
    filters.providers = new Set(Object.keys(dump.providers))
    filters.tags = new Set(Object.keys(dump.tags))
    filters.geotags = new Set(Object.keys(dump.geotags))
    filters.page = dump.page
}

function toggleProviderFilter(id) {
    if (filters.providers.has(id)) {
        filters.providers.delete(id)
        return false
    }
    filters.providers.add(id)
    return true
}

function createProviderFilter() {
    let container = document.createElement("div")
    container.id = "provider-filter-container"
    let text = document.createElement("h3")
    text.innerText = "Provider"
    container.appendChild(text)
    let items_container = document.createElement("div")
    items_container.className = "filter-items-container"
    createProviderFilterItems = () => {
        items_container.innerText = ""
        for (let [id, name] of Object.entries(filter_items.providers)) {
            let item = createFilterItem(id, name, toggleProviderFilter, filters.providers.has(id))
            items_container.appendChild(item)
        }
    }
    updateProviderFilterItems = () => {
        Object.keys(filter_items.providers).forEach((id, index) => {
            if (filters.providers.has(id)) {
                items_container.children[index].classList.add("selected")
            } else {
                items_container.children[index].classList.remove("selected")
            }
        })
    }
    container.appendChild(items_container)
    let load_more_container = document.createElement("div")
    load_more_container.className = "filter-load-more-container"
    let load_more_button = document.createElement("button")
    let load_more_error = document.createElement("p")
    load_more_container.appendChild(load_more_button)
    load_more_container.appendChild(load_more_error)
    load_more_button.innerText = "Load more"
    load_more_button.onclick = async () => {
        let success = await fetch("/api/opportunity-provider/all", {
            method: "GET"
        })
        .then(async (response) => {
            if (response.status === 200) {
                Object.assign(filter_items.providers, await response.json())
                return true
            } else if (response.status === 422) {
                document.location.href = "/sign-in"
                return false
            }
            load_more_error.innerText = "Something went wrong, try again later"
            return false
        })
        if (!success) {
            return
        }
        createProviderFilterItems()
        let search_container = createFilterSearch("Provider name")
        container.insertBefore(search_container, items_container)
        updateProviderFilterItems = () => {
            let query = search_container.getElementsByTagName("input")[0].value
            query = query.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&')
            const regex = new RegExp(`\\b${query}.*`, "i")
            Object.entries(filter_items.providers).forEach((item, index) => {
                if (regex.test(item[1])) {
                    items_container.children[index].classList.remove("hidden")
                } else {
                    items_container.children[index].classList.add("hidden")
                    return
                }
                if (filters.providers.has(item[0])) {
                    items_container.children[index].classList.add("selected")
                } else {
                    items_container.children[index].classList.remove("selected")
                }
            })
        }
        search_container.getElementsByTagName("input")[0].oninput = debounce(updateProviderFilterItems, 200)
        load_more_container.remove()
    }
    container.appendChild(load_more_container)
    return container
}

let createProviderFilterItems = () => {}
let updateProviderFilterItems = () => {}

function toggleTagFilter(id) {
    if (filters.tags.has(id)) {
        filters.tags.delete(id)
        return false
    }
    filters.tags.add(id)
    return true
}

function createTagFilter() {
    let container = document.createElement("div")
    container.id = "tag-filter-container"
    let text = document.createElement("h3")
    text.innerText = "Tag"
    container.appendChild(text)
    let items_container = document.createElement("div")
    items_container.className = "filter-items-container"
    createTagFilterItems = () => {
        items_container.innerText = ""
        for (let [id, name] of Object.entries(filter_items.tags)) {
            let item = createFilterItem(id, name, toggleTagFilter, filters.tags.has(id))
            items_container.appendChild(item)
        }
    }
    updateTagFilterItems = () => {
        Object.keys(filter_items.tags).forEach((id, index) => {
            if (filters.tags.has(id)) {
                items_container.children[index].classList.add("selected")
            } else {
                items_container.children[index].classList.remove("selected")
            }
        })
    }
    container.appendChild(items_container)
    let load_more_container = document.createElement("div")
    load_more_container.className = "filter-load-more-container"
    let load_more_button = document.createElement("button")
    let load_more_error = document.createElement("p")
    load_more_container.appendChild(load_more_button)
    load_more_container.appendChild(load_more_error)
    load_more_button.innerText = "Load more"
    load_more_button.onclick = async () => {
        let success = await fetch("/api/opportunity-tag/all", {
            method: "GET"
        })
        .then(async (response) => {
            if (response.status === 200) {
                Object.assign(filter_items.tags, await response.json())
                return true
            } else if (response.status === 422) {
                document.location.href = "/sign-in"
                return false
            }
            load_more_error.innerText = "Something went wrong, try again later"
            return false
        })
        if (!success) {
            return
        }
        createTagFilterItems()
        let search_container = createFilterSearch("Tag name")
        container.insertBefore(search_container, items_container)
        updateTagFilterItems = () => {
            let query = search_container.getElementsByTagName("input")[0].value
            query = query.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&')
            const regex = new RegExp(`\\b${query}.*`, "i")
            Object.entries(filter_items.tags).forEach((item, index) => {
                if (regex.test(item[1])) {
                    items_container.children[index].classList.remove("hidden")
                } else {
                    items_container.children[index].classList.add("hidden")
                    return
                }
                if (filters.tags.has(item[0])) {
                    items_container.children[index].classList.add("selected")
                } else {
                    items_container.children[index].classList.remove("selected")
                }
            })
        }
        search_container.getElementsByTagName("input")[0].oninput = debounce(updateTagFilterItems, 200)
        load_more_container.remove()
    }
    container.appendChild(load_more_container)
    return container
}

let createTagFilterItems = () => {}
let updateTagFilterItems = () => {}

function toggleGeotagFilter(id) {
    if (filters.geotags.has(id)) {
        filters.geotags.delete(id)
        return false
    }
    filters.geotags.add(id)
    return true
}

function createGeotagFilter() {
    let container = document.createElement("div")
    container.id = "geotag-filter-container"
    let text = document.createElement("h3")
    text.innerText = "Geotag"
    container.appendChild(text)
    let items_container = document.createElement("div")
    items_container.className = "filter-items-container"
    createGeotagFilterItems = () => {
        items_container.innerText = ""
        for (let [id, [country, city]] of Object.entries(filter_items.geotags)) {
            let item = createFilterItem(id, `${country}, ${city}`, toggleGeotagFilter, filters.geotags.has(id))
            items_container.appendChild(item)
        }
    }
    updateGeotagFilterItems = () => {
        Object.keys(filter_items.geotags).forEach((id, index) => {
            if (filters.geotags.has(id)) {
                items_container.children[index].classList.add("selected")
            } else {
                items_container.children[index].classList.remove("selected")
            }
        })
    }
    container.appendChild(items_container)
    let load_more_container = document.createElement("div")
    load_more_container.className = "filter-load-more-container"
    let load_more_button = document.createElement("button")
    let load_more_error = document.createElement("p")
    load_more_container.appendChild(load_more_button)
    load_more_container.appendChild(load_more_error)
    load_more_button.innerText = "Load more"
    load_more_button.onclick = async () => {
        let success = await fetch("/api/opportunity-geotag/all", {
            method: "GET"
        })
        .then(async (response) => {
            if (response.status === 200) {
                Object.assign(filter_items.geotags, await response.json())
                return true
            } else if (response.status === 422) {
                document.location.href = "/sign-in"
                return false
            }
            load_more_error.innerText = "Something went wrong, try again later"
            return false
        })
        if (!success) {
            return
        }
        createGeotagFilterItems()
        let search_container = createFilterSearch("Geotag name")
        container.insertBefore(search_container, items_container)
        updateGeotagFilterItems = () => {
            let query = search_container.getElementsByTagName("input")[0].value
            query = query.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&')
            const regex = new RegExp(`\\b${query}.*`, "i")
            Object.entries(filter_items.geotags).forEach((item, index) => {
                if (regex.test(item[1][0]) || regex.test(item[1][1])) {
                    items_container.children[index].classList.remove("hidden")
                } else {
                    items_container.children[index].classList.add("hidden")
                    return
                }
                if (filters.geotags.has(item[0])) {
                    items_container.children[index].classList.add("selected")
                } else {
                    items_container.children[index].classList.remove("selected")
                }
            })
        }
        search_container.getElementsByTagName("input")[0].oninput = debounce(updateGeotagFilterItems, 200)
        load_more_container.remove()
    }
    container.appendChild(load_more_container)
    return container
}

let createGeotagFilterItems = () => {}
let updateGeotagFilterItems = () => {}

function initializeFilters() {
    const categoriesContainer = document.getElementById("filter-categories-container")
    categoriesContainer.appendChild(createProviderFilter())
    createProviderFilterItems()
    updateProviderFilterItems()
    categoriesContainer.appendChild(createTagFilter())
    createTagFilterItems()
    updateTagFilterItems()
    categoriesContainer.appendChild(createGeotagFilter())
    createGeotagFilterItems()
    updateGeotagFilterItems()
    const applyButton = document.getElementById("apply-filters-button")
    applyButton.onclick = () => {
        if (same_filters(history.state.filters)) {
            return
        }
        history.pushState({ filters: copy_filters(filters), fetched: false }, "", serialize_filters())
        fetchOpportunityCards()
    }
}

function createOpportunityCards(cards) {
    const cardsContainer = document.getElementById("cards-container")
    cardsContainer.innerText = JSON.stringify(cards)
}

function fetchOpportunityCards() {
    fetch(`/api/opportunity-cards${serialize_filters()}&responded=true`, {
        method: "GET"
    })
    .then(async (response) => {
        if (response.status === 200) {
            let cards = await response.json()
            createOpportunityCards(cards)
            history.replaceState(
                Object.assign(history.state, { fetched: true, cards: cards }), ""
            )
            return
        } else if (response.status === 422) {
            document.location.href = "/sign-in"
            return
        }
        const cardsContainer = document.getElementById("cards-container")
        cardsContainer.innerText = "Something went wrong, try again later"
    })
}

document.addEventListener("DOMContentLoaded", () => {
    loadFiltersDump()
    history.replaceState({ filters: copy_filters(filters), fetched: false }, "")
    initializeFilters()
    fetchOpportunityCards()
})

window.addEventListener("popstate", (event) => {
    filters = copy_filters(event.state.filters)
    updateProviderFilterItems()
    updateTagFilterItems()
    updateGeotagFilterItems()
    if (!event.state.fetched) {
        fetchOpportunityCards()
    } else {
        createOpportunityCards(event.state.cards)
    }
})
