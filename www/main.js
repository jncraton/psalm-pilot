function search_title() {
  let input = document.querySelector('#search').value.toLowerCase()
  document.querySelectorAll('tbody tr').forEach(r => {
    r.style.display = r.textContent.toLowerCase().includes(input) ? '' : 'none'
  })
}

async function chat(message, model = 'gemini-2.5-flash-lite', tries = 3) {
  if (tries < 1) {
    throw new Error('Chat retries exceeded')
  }

  localStorage.geminiKey = localStorage.geminiKey || prompt('Enter Gemini key')

  const res = await fetch(
    `https://generativelanguage.googleapis.com/v1/models/${model}:generateContent`,
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

let hymns = []
async function loadHymns() {
  const res = await fetch('./hymns/hymns.json')
  hymns = await res.json()
}

window.addEventListener('load', loadHymns)

const form = document.querySelector('#recommendation-form')

function prompt_recommendations() {
  const date = document.querySelector('#sermon-date').value
  const topic = document.querySelector('#topic-textbox').value
  const scripture = document.querySelector('#scripture-textbox').value

  return `
You are a worship planning assistant.

SERVICE CONTEXT
- Date: ${date || 'Not known'}
- Scriptures: ${scripture || 'Not known'}
- Sermon topic: ${topic || 'Not known'}

You are given a JSON array of hymns. Each hymn includes fields like:
- titleId
- title
- authors
- firstLine
- refrainFirstLine
- popularity
- year
- scriptureRefs
- text

HYMNS JSON:
${JSON.stringify(hymns, null, 2)}

TASK:
From ONLY the hymns in the JSON array above, choose 3-5 hymns that best fit the scriptures and sermon topic from the service context. Use the time of year to pick ones that are relevant to the season (e.g. no christmas songs in august).
Respond in Markdown with a service order recommendation that includes:
- additional scriptures that can be read
- A list of the chosen hymns (title)
- 1-2 sentences for each explaining why it fits.
- link to the chosen hymn page as [{title}](https://jncraton.github.io/psalm-pilot/hymns/{titleId})
- anything you recommend give what the person reading it should say about it this includes the benediction
- make sure to include where the sermon message should go in the order
`
}

if (form) {
  form.addEventListener('submit', async e => {
    e.preventDefault()
    responseBox.innerHTML = 'Please be patient, I am working very slowly...'

    const prompt = prompt_recommendations()

    const reply = await chat(prompt)
    console.log(reply)
    responseBox.innerHTML = marked.parse(reply)

    return false
  })
}
