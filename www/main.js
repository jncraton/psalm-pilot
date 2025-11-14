function search_title() {
  let input = document.querySelector('#search').value.toLowerCase()
  document.querySelectorAll('tbody tr').forEach(r => {
    r.style.display = r.textContent.toLowerCase().includes(input) ? '' : 'none'
  })
}
