// Progressbar and event handler utilities for individual demos

function smoothProgressbarIncrement (progressBar) {
  setTimeout(() => {
    progressBar.value += (90 - progressBar.value) / 30
  }, 200)
}

function smoothProgressbarComplete (progressBar) {
  setTimeout(() => {
    progressBar.value = 100
  }, 200)
  setTimeout(() => {
    progressBar.value = 0
  }, 3200)
}

function addDemoEventListener (triggers, handlerFunction, inputElementId, outputElementId) {
  const inputEl = document.getElementById(inputElementId)
  const outputEl = document.getElementById(outputElementId)
  const boundHandler = handlerFunction.bind(null, inputEl, outputEl)
  triggers.forEach(triggerData => {
    document.getElementById(triggerData.elementId).addEventListener(triggerData.eventName, e => {
      e.preventDefault()
      boundHandler()
      return false
    })
  })
  boundHandler() // execute handler for the 1st time on registration
}

function addDemoEventListenerWithDefaulNaming (demoEventName, handler) {
  return addDemoEventListener(
    [{
      elementId: `${demoEventName}-submit`,
      eventName: 'click'
    },
    {
      elementId: `${demoEventName}`,
      eventName: 'submit'
    }],
    handler,
    `${demoEventName}-input`,
    `${demoEventName}-output`
  )
}
