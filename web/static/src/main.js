// page navigation and main demo setup

function activate (pageData) {
  pageData.menuElement.classList.add('uk-active')
  pageData.pageElement.classList.remove('uk-hidden')
  location.hash = pageData.pageElement.id
}

function deactivate (pageData) {

  pageData.menuElement.classList.remove('uk-active')
  pageData.pageElement.classList.add('uk-hidden')
}

let demoNavigator = undefined

UIkit.util.ready(() => {
  // setup all demos (defined in other files)
  setupWordcloud()
  // setup menu navigation
  let pageNames = [
    'home',
    'components',
    'models',
    'wordcloud']
  let pages = Object.assign(...pageNames.map(pageName => {
    let pageData = {}
    pageData[pageName] = {
      'menuElement': document.getElementById(`${pageName}-menu-item`),
      'pageElement': document.getElementById(pageName)
    }
    return pageData
  }))
  let hashPageId = location.hash.substring(1)
  let initialPage = hashPageId ? hashPageId : 'home'
  demoNavigator = new Navigator({pages, activate, deactivate, initialPage})
})
