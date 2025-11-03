function search_title() {
    
    let input = document.getElementById('search').value
    input = input.toLowerCase();
    console.log(input);

    let title = document.querySelectorAll('tr');

    for (i = 0; i < title.length; i++) {
        const whole_row = title[i].closest('tr');
        if (title[i].textContent.toLowerCase().includes(input)) {
            whole_row.style.display = ""
        }
        else {
            whole_row.style.display = "none";
        }
    }
}

