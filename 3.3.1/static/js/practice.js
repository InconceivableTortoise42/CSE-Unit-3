const mf = document.getElementById("mathField");
const apiUrl = `/api/${problemType}`;
const directionsElement = document.getElementById("directions");
const menuExclusions = ["mode", "color", "background-color", "accent", "decoration", "variant"];
const sumbitButton = document.getElementById("submit");
const mathProblemElement = document.getElementById("mathProblem");
const cardHeader = document.getElementById("cardHeader");
const solution = document.getElementById("solution");

let directions = {
    "basic_algebra": "Find the value of x:  ",
    "combine_like_terms": "Put the expression in it's simplest form: "
}

function fetchProblem() {
    mathProblemElement.classList.add("placeholder")
    mathProblemElement.innerText = "&nbsp;";
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            window.setTimeout(() => {
                mathProblemElement.innerText = data["problem"];
                solution.innerText = data["solution"]
                MathJax.typeset([mathProblemElement, solution]);
                console.log(data["solution"])
                mathProblemElement.classList.remove("placeholder")
            }, 1000);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}   

function toTitleCase(string) {
  return string
    .split(' ') 
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' '); 
}

sumbitButton.addEventListener("click", (event) => {
    fetchProblem();
    console.log(mf.getValue());
    mf.setValue("");
});

window.onload = () => {
    mf.menuItems = mf.menuItems.filter(item => !menuExclusions.includes(item.id));
    cardHeader.innerText = toTitleCase(problemType.replaceAll("_", " "));
    document.title = toTitleCase(problemType);
    directionsElement.innerHTML = directions[problemType] + directionsElement.innerHTML
    fetchProblem();
}