// named entity wordcloud demonstration

// computed later
let wordCloudSize = [640, 480] // width, height
let ners = []
let wordCloud

// updated dynamically when viewport changes:
let defaultMaxItemsInList = 42
let maxAdjFontSize = 128
let minAdjFontSize = 16

function parseAndScale (responseData) {
  let adjectives = Object.keys(responseData)
  const maxAll = adjectives => {
    return adjectives.map(adj => [ adj, maxAdjFontSize, responseData[adj]['sents'] ])
  }
  if (adjectives.length <= 1) return maxAll(adjectives)

  let counts = adjectives.map(adj => parseInt(responseData[adj]['count']))
  let minCount = Math.min(...counts)
  let maxCount = Math.max(...counts)
  if (minCount === maxCount) return maxAll(adjectives)

  maxAdjFontSize = Math.min(maxAdjFontSize, Math.max(...wordCloudSize) / 8)
  minAdjFontSize = Math.max(minAdjFontSize, Math.min(...wordCloudSize) / 8)
  let scale = (maxAdjFontSize - minAdjFontSize) / (maxCount - minCount)
  const scaleCount = realCount => scale * realCount + minAdjFontSize - scale * minCount
  return adjectives.map(adj => [ adj, scaleCount(responseData[adj]['count']), responseData[adj]['sents'] ])
}

function wordcloudHandler (inputElement, _) {
  if (inputElement.value.length === 0) return
  // set up progressbar animation
  const progressBar = document.getElementById('ner-wordcloud-progressbar')
  const wordCloudElement = document.getElementById('wordcloud-content')
  progressBar.value = 0
  let timer = setInterval(() => {
    smoothProgressbarIncrement(progressBar)
  }, 50)
  // query search endpoint
  axios.get(`/api/NERs/${inputElement.value}`).then(response => {
    console.log(response)
    // let wordFreqs = Object.keys(response.data).map(word => [word, Number(response.data[word])])
    wordCloud = WordCloud(wordCloudElement, {
      list: parseAndScale(response.data),
      click: (item, dimension, event) => { console.log(item, dimension) } // TODO: Display part of article
    })
    clearInterval(timer)
    smoothProgressbarComplete(progressBar)
  }).catch(error => {
    console.log(error)
    clearInterval(timer)
  })
}

function selectFromList (formElement, inputElement, listElement, listItemElement) {
  inputElement.value = listItemElement.innerText
  Array.from(listElement.children).forEach(item => item.classList.remove('uk-active'))
  listItemElement.classList.add('uk-active')
  let submitEvent = new Event('submit')
  formElement.dispatchEvent(submitEvent)
}

function filterListByInput (formElement, inputElement, listElement, possibleItems, maxDisplayedItems = defaultMaxItemsInList) {
  // clear the list
  while (listElement.firstChild) {
    listElement.removeChild(listElement.firstChild)
  }
  // append all items matching input value to the list
  possibleItems.filter(item => {
    return item.toLowerCase().includes(inputElement.value.toLowerCase())
  }).slice(0, maxDisplayedItems).forEach(matchingItem => {
    let newItem = document.createElement('li')
    newItem.classList.add('uk-box-shadow-hover-small')
    let newAnchor = document.createElement('a')
    newAnchor.innerText = matchingItem
    newAnchor.href = '#!'
    let boundSelectItemHandler = selectFromList.bind(
      null,
      formElement,
      inputElement,
      listElement,
      newItem)
    newAnchor.addEventListener('click', event => {
      event.preventDefault()
      boundSelectItemHandler()
      return false
    })
    newItem.appendChild(newAnchor)
    listElement.appendChild(newItem)
  })
}

function setNerAutocomplete (elementId) {
  const nerInputElement = document.getElementById(`${elementId}-input`)
  const nerFormElement = document.getElementById(elementId)
  const nerListElement = document.getElementById(`${elementId}-list`)
  axios.get('/api/NERs').then(response => {
    ners = Array.from(response.data)
    const boundFilterHandler = filterListByInput.bind(
      null,
      nerFormElement,
      nerInputElement,
      nerListElement,
      ners)
    nerInputElement.addEventListener('keyup', event => {
      boundFilterHandler()
    })
    filterListByInput(nerFormElement, nerInputElement, nerListElement, ners)
  }).catch(error => {
    console.log(error)
  })
}

function fitToContainer (canvas) {
  // https://stackoverflow.com/questions/10214873/make-canvas-as-wide-and-as-high-as-parent
  // Make it visually fill the positioned parent
  canvas.style.width = '100%'
  canvas.style.height = '100%'
  // ...then set the internal size to match
  canvas.width = canvas.offsetWidth
  canvas.height = canvas.offsetHeight
}

function maxListLength () {
  let minDim = Math.floor(Math.min(
    document.documentElement.clientHeight,
    document.documentElement.clientWidth
  ))
  if (minDim < 400) {
    return Math.floor(minDim / 40)
  } else {
    return Math.floor(minDim / 20)
  }
}

function setupWordcloud () {
  defaultMaxItemsInList = maxListLength()
  fitToContainer(document.getElementById('wordcloud-content'))
  setNerAutocomplete('ner-wordcloud')
  addDemoEventListenerWithDefaulNaming('ner-wordcloud', wordcloudHandler)
}
