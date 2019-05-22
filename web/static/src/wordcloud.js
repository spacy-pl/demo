// named entity wordcloud demonstration

// computed later
let wordCloudSize = [640, 480] // width, height
let ners = []
let wordCloud
let activeEntity

// updated dynamically when viewport changes:
let defaultMaxItemsInList = 42
let maxDisplayAdjectives = 128
let maxAdjFontSize = 96
let minAdjFontSize = 16

function parseAndScale (responseData) {
  const compareCounts = (a, b) => b[1] - a[1]
  const saturate = adj => [ adj[0], Math.pow(adj[1], 2.137), adj[2] ]
  maxDisplayAdjectives = Math.floor(maxDisplayAdjectives * Math.max(...wordCloudSize) / 640)
  let adjectives = Object.keys(responseData).map(key => {
    return [
      key,
      parseInt(responseData[key]['count']),
      responseData[key]['sents']
    ]
  }).sort(compareCounts).slice(0, maxDisplayAdjectives)
  adjectives = adjectives.map(saturate)

  const maxAll = adjectives => {
    return adjectives.map(adj => {
      adj[1] = maxAdjFontSize
      return adj
    })
  }
  if (adjectives.length <= 1) return maxAll(adjectives)

  let counts = adjectives.map(adj => adj[1])
  let minCount = Math.min(...counts)
  let maxCount = Math.max(...counts)
  if (minCount === maxCount) return maxAll(adjectives)

  maxAdjFontSize = Math.floor(maxAdjFontSize * Math.max(...wordCloudSize) / 640)
  minAdjFontSize = Math.floor(minAdjFontSize * Math.min(...wordCloudSize) / 480)
  let scale = (maxAdjFontSize - minAdjFontSize) / (maxCount - minCount)
  const scaleCount = adj => [ adj[0], scale * adj[1] - scale * minCount + minAdjFontSize, adj[2] ]
  return adjectives.map(scaleCount)
}

function createModal (adj, sents) {
  const getModalData = () => {
    let modalTitle = document.getElementById('sentence-modal-title')
    let modalList = document.getElementById('sentence-modal-list')
    return [modalTitle, modalList]
  }
  const defineModal = () => {
    let modalElement = document.createElement('div')
    modalElement.id = 'sentence-modal'
    modalElement.className = 'modal-overflow'
    modalElement.setAttribute('uk-modal', '')
    let modalTitle = document.createElement('h4')
    modalTitle.id = 'sentence-modal-title'
    modalTitle.className = 'uk-modal-title'
    let modalList = document.createElement('ul')
    modalList.id = 'sentence-modal-list'
    modalList.className = 'uk-list uk-list-divider'
    let modalContent = document.createElement('div')
    modalContent.className = 'uk-modal-dialog uk-modal-body'
    modalContent.setAttribute('uk-overflow-auto', '')
    let modalButton = document.createElement('button')
    modalButton.className = 'uk-modal-close-default'
    modalButton.setAttribute('type', 'button')
    modalButton.setAttribute('uk-close', '')
    modalContent.appendChild(modalButton)
    modalContent.appendChild(modalTitle)
    modalContent.appendChild(modalList)
    modalElement.appendChild(modalContent)
    document.getElementById('wordcloud').appendChild(modalElement)
    return [modalTitle, modalList]
  }
  let modalElement = document.getElementById('sentence-modal')
  let [modalTitle, modalList] = modalElement ? getModalData() : defineModal()
  modalTitle.innerHTML = `Sample uses of ${adj} adjective for ${activeEntity}`
  // clear the list
  while (modalList.firstChild) {
    modalList.removeChild(modalList.firstChild)
  }
  // add sentences to the list
  sents.forEach(sent => {
    let el = document.createElement('li')
    el.innerText = sent
    modalList.appendChild(el)
  })
  return modalElement
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
      fontFamily: "'Baloo Bhai', cursive",
      weightFactor: 1,
      rotateRatio: 0.125,
      rotationSteps: 16,
      click: (item, dimension, event) => {
        UIkit.modal(createModal(item[0], item[2])).show()
      } // TODO: Display part of article
    })
    clearInterval(timer)
    smoothProgressbarComplete(progressBar)
  }).catch(error => {
    console.log(error)
    clearInterval(timer)
  })
}

function selectFromList (formElement, inputElement, listElement, listItemElement) {
  activeEntity = listItemElement.innerText
  inputElement.value = activeEntity
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

function computeMaxListSize () {
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
  defaultMaxItemsInList = computeMaxListSize()
  fitToContainer(document.getElementById('wordcloud-content'))
  setNerAutocomplete('ner-wordcloud')
  addDemoEventListenerWithDefaulNaming('ner-wordcloud', wordcloudHandler)
}
