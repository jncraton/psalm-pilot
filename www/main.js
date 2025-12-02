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
    }
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

async function prompt_recommendations() {
  const date = document.querySelector('#sermon-date').value
  const scripture = document.querySelector('#scripture').value
  const sermon_topic = document.querySelector('#sermon-topic').value
  return `
Generate worship service hymn recommendations from these:
Date: ${date}
Scripture(s): ${scripture}
Sermon topic: ${sermon_topic}
`
}
