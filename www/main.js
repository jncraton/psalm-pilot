function search_title() {
  let input = document.querySelector('#search').value.toLowerCase()
  document.querySelectorAll('tbody tr').forEach(r => {
    r.style.display = r.textContent.toLowerCase().includes(input) ? '' : 'none'
  })
}

async function chat(message, model = 'gemini-flash-lite-latest', tries = 3) {
  if (tries < 1) {
    throw new Error('Chat retries exceeded')
  }

  localStorage.geminiKey = localStorage.geminiKey || prompt('Enter Gemini key')

  const res = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-goog-api-key': localStorage.geminiKey,
      },
      body: `{contents:[{parts:[{text:${JSON.stringify(message)}}]}]}`,
    },
  )

  try {
    if (res.status != 200) {
      console.error(await res.json())
      throw new Error(`Gemini API: ${res.status} ${res.statusText}`)
    }
    return (await res.json()).candidates[0].content.parts[0].text
  } catch (error) {
    console.error(error)
    console.warn('Waiting 3 seconds before Gemini retry')
    await new Promise(r => setTimeout(r, 3000))
    return await chat(message, model, tries - 1)
  }
}

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('service-worker.js')
  })
}

const recButton = document.querySelector('form')
const textInput = document.querySelector('textarea')
const responseBox = document.querySelector('.response-text')

recButton.addEventListener('submit', async e => {
  e.preventDefault()
  const msg = textInput.value
  console.log(msg)
  const reply = await chat(msg)
  responseBox.innerHTML = marked.parse(reply)
  return false
})


//Pgaes Button
const currentPath = window.location.pathname; 
const aPoints = document.querySelectorAll("a.directory-page, a.recommendations-page")

aPoints.forEach(btn => {
  const href = btn.getAttribute("href");
  aPoints.forEach(link => link.classList.remove('active'));
  if (href && currentPath.endsWith(href)) {
    btn.classList.add("active");
  } else if (href === '/') {
    btn.classList.add("active");
  }
});

//Recomendation input
const timeOfYear = document.getElementById('time-of-year')
const scriptureS = document.getElementById('scripture-s')
const sermonTopic = document.getElementById('sermon-topic')

function updateTextarea() {
  textInput.value =
    (timeOfYear.value || '') +
    '\n' +
    (scriptureS.value || '') +
    '\n' +
    (sermonTopic.value || '')
}

timeOfYear.addEventListener('input', updateTextarea)
scriptureS.addEventListener('input', updateTextarea)
sermonTopic.addEventListener('input', updateTextarea)
