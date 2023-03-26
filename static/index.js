const btn = document.getElementById("new-word-button")

btn.addEventListener("click", async () => {
  const ul = document.getElementById("generated-words")
  const li = document.createElement("li")
  li.innerText = await fetchWord()
  ul.insertBefore(li, ul.firstChild)
})

async function fetchWord() {
  btn.disabled = true
  const resp = await fetch(`/word/portmanteau_and_markov/${getNGramSize()}`)
  const word = await resp.text()
  btn.disabled = false
  return word
}

function getNGramSize() {
  const radioBtns = document.querySelectorAll('input[name="ngram-size"]')
  for (const btn of radioBtns) {
    if (btn.checked) {
      return btn.value
    }
  }
  return null
}