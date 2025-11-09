function search_title() {
  let input = document.getElementById('search').value
  input = input.toLowerCase()
  let title = document.querySelectorAll('tbody tr')

  for (i = 0; i < title.length; i++) {
    const whole_row = title[i].closest('tr')

    if (title[i].textContent.toLowerCase().includes(input)) {
      whole_row.style.display = ''
    } else {
      whole_row.style.display = 'none'
    }

    const visibleRows = []
    for (let i = 0; i < title.length; i++) {
      if (title[i].style.display !== 'none') {
        visibleRows.push(title[i])
      }
    }
    for (let i = 0; i < visibleRows.length; i++) {
      if (i % 2 === 0) {
        visibleRows[i].style.backgroundColor = '#f1f1f1'
      } else {
        visibleRows[i].style.backgroundColor = 'transparent'
      }
    }
  }
}
