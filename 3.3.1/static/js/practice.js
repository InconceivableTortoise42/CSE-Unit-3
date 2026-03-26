import { ComputeEngine } from "https://esm.run/@cortex-js/compute-engine";

const ce = new ComputeEngine();

const mf = document.getElementById("mathField");
const apiUrl = `/api/${problemType}`;
const directionsElement = document.getElementById("directions");
const menuExclusions = ["mode", "color", "background-color", "accent", "decoration", "variant", "ce-evaluate", "ce-simplify", "ce-solve"];
const sumbitButton = document.getElementById("submit");
const mathProblemElement = document.getElementById("mathProblem");
const cardHeader = document.getElementById("cardHeader");
const solutionElement = document.getElementById("solution");
const card = document.querySelector(".card");

let solution = "";

let directions = {
    "basic_algebra": "Find the value of x:  ",
    "combine_like_terms": "Put the expression in it's simplest form: ",
    "factoring": "Factor the quadratic into it's roots: ",
    "expanding": "Expand the factored binomial: ",
    "addition": "Find the sum: "
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
            mathProblemElement.innerText = data["problem"];
            solutionElement.innerText = data["solution"]
            MathJax.typeset([mathProblemElement, solutionElement]);
            solution = JSON.stringify(ce.parse(data["solution"].replaceAll("$", "")).json);
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

function flashFeedback(correctBool) {
    let className;
    if (correctBool) {
        className = "correct";
    } else {
        className = "incorrect";
    }
    card.classList.add(className);
    setTimeout(() => {
        card.classList.remove(className);
    }, 1000);
}

sumbitButton.addEventListener("click", (event) => {
    if (mf.getValue("math-json") == solution) {
        console.log("Correct!");
        flashFeedback(true);
    } else {
        flashFeedback(false);
        console.log("Incorrect!");
    }
    fetchProblem();
    mf.setValue("");
});

window.onload = () => {
    mf.menuItems = mf.menuItems.filter(item => !menuExclusions.includes(item.id));
    document.title = cardHeader.innerText = toTitleCase(problemType.replaceAll("_", " "));
    if (directions[problemType]) {
        directionsElement.innerHTML = directions[problemType] + directionsElement.innerHTML
    } else {
        directionsElement.remove();
        mathProblemElement.parentElement.style.height = "2rem";
        mathProblemElement.parentElement.querySelector("br").remove();
    }
    fetchProblem();
}
