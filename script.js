var checkbox = document.querySelector('input[name=mode]');
var data = document.getElementById("myForm");

window.onload = () => {
    console.log(checkbox.value)
    if (checkbox.value == "On" || checkbox.checked == true) {
        document.documentElement.setAttribute('data-theme', 'dark')
        checkbox.checked = true
        checkbox.value = "On"
    }
    else {
        document.documentElement.setAttribute('data-theme', 'light')
        checkbox.checked = false
        checkbox.value = "Off"
    }
    console.log("load success")
}
checkbox.addEventListener('change', function() {
    var theme = this.checked ? 'dark' : 'light';
    this.value = this.checked ? "On" : "Off";
    trans()
    document.documentElement.setAttribute('data-theme', theme)
    console.log("is " + this.value)
    data.submit()
})

let trans = () => {
    document.documentElement.classList.add('transition');
    window.setTimeout(() => {
        document.documentElement.classList.remove('transition');
    }, 1000)
}