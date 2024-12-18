const debounce = (callback, wait) => {
    let timeoutId = null;
    return (...args) => {
        window.clearTimeout(timeoutId);
        timeoutId = window.setTimeout(() => {
        callback(...args);
        }, wait);
    };
}

const equalSets = (a, b) => {
    return a.size === b.size && [...a].every((x) => b.has(x))
}
