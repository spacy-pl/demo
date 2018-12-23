const pageNames = ['home', 'lemmatizer', 'vectors'];
let pages = [];

function setActivePage(loadedPages, activePageName) {
    loadedPages.forEach(pageData => {
        if (pageData.page === activePageName) {
            console.log(`setting ${pageData.page} to active`);
            pageData.menuItem.classList.add('uk-active');
            pageData.contentContainer.classList.remove('uk-hidden');
        } else {
            console.log(`setting ${pageData.page} to inactive`);
            pageData.menuItem.classList.remove('uk-active');
            pageData.contentContainer.classList.add('uk-hidden');
        }
    });
}

function searchHandler(inputElement, outputElement) {
    axios.post('/lemmatizer', {
        query: inputElement.value
    }).then(response => {
        console.log(response);
        outputElement.innerHTML = Array.from(response.data).map(searchResult => {
            let parsedText = searchResult['token_text'].replace(/(?:\r\n|\r|\n)/g, '<br>');
            if (searchResult['direct_match']) {
                return `<span class="uk-label uk-label-success">${parsedText}</span>`
            } else if (searchResult['lemma_match']) {
                return `<span class="uk-label uk-label-warning">${parsedText}</span>`
            } else {
                return parsedText
            }
        }).join('');  // tokens already contain whitespace
    }).catch(error => {
        console.log(error);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    console.log("setting up application...");
    // get all pages' menu items and content divs
    pages = pageNames.map(page => {
        return {
            page: page,
            menuItem: document.getElementById(`${page}-menu-item`),
            contentContainer: document.getElementById(`${page}-content`)
        }
    });
    // make all pages except home invisible (this is done in JS to make sure crawlers see entire html)
    pages.slice(1).forEach(pageData => {
        pageData.contentContainer.classList.add('uk-hidden');
    });
    // add page selection functionality to the menu
    pages.forEach(pageData => {
        const boundHandler = setActivePage.bind(null, pages, pageData.page);
        pageData.menuItem.addEventListener('click', e => {
            e.preventDefault();
            boundHandler();
            return false;
        });
    });
    // add handler resetting page selection to the navbar logo
    const boundResetPageHandler = setActivePage.bind(null, pages, pages[0].page);
    document.getElementById('navbar-logo').addEventListener('click', e => {
        e.preventDefault();
        boundResetPageHandler();
        return false;
    });
    console.log("done");
    console.log("setting up demos...");
    // lemmatizer demo search handler
    const searchOutputElement = document.getElementById('lemmatizer-search-output');
    const searchInputElement = document.getElementById('lemmatizer-search-input');
    const boundSearchHandler = searchHandler.bind(null, searchInputElement, searchOutputElement);
    document.getElementById('lemmatizer-search-submit').addEventListener('click', e => {
        e.preventDefault();
        boundSearchHandler();
        return false;
    });
    boundSearchHandler();  // send an empty search request to populate the page
    console.log("done");
});
