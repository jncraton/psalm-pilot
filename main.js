function search_title() {
  let input = document.getElementById('search').value

  input = input.toLowerCase()

  let title = document.querySelectorAll('tbody tr')
  console.log(title)

  for (i = 0; i < title.length; i++) {
    const whole_row = title[i].closest('tr')
    // var evenRows = document.querySelectorAll('tbody tr:nth-child(even)');
    

    if (title[i].textContent.toLowerCase().includes(input)) {
      // evenRows.forEach(function(row) {
      //   row.style.backgroundColor = "#f1f1f1";
      // });
      title.forEach(titleElement => {
        titleElement.style.backgroundColor = "transparent";
      });
      whole_row.style.display = ''
    } else {
      whole_row.style.display = 'none'
    }
  }
}
