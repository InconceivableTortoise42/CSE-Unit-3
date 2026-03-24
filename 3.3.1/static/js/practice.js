const mf = document.getElementById("mathField");
const apiUrl = `/api/${problemType}`;
const directionsElement = document.getElementById("directions");
const menuExclusions = ["mode", "color", "background-color", "accent", "decoration", "variant"];

let directions = {
    "algebra": "Find the value of x"
}

function fetchProblem() {
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            directionsElement.innerText = directions[problemType] + data["problem"]
            MathJax.Hub.Queue(["Typeset", MathJax.Hub, "directions"]);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}   

window.onload = () => {
    mf.menuItems = mf.menuItems.filter(item => !menuExclusions.includes(item.id));
    fetchProblem()
}