import { ComputeEngine } from "https://esm.run/@cortex-js/compute-engine";

const ce = new ComputeEngine();
const apiUrl = `/api/${problemType}`;
const menuExclusions = ["mode", "color", "background-color", "accent", "decoration", "variant", "ce-evaluate", "ce-simplify", "ce-solve"];

const pickRandomItem = (arr) => arr[Math.floor(Math.random() * arr.length)];

const mf = document.getElementById("mathField");
const card = document.querySelector(".card");
const cardTitle = document.getElementById("cardTitle");

const mathProblemElement = document.getElementById("mathProblem");
const directionsElement = document.getElementById("directions");

const sumbitButton = document.getElementById("submit");
const solutionButton = document.getElementById("solution");

const incorrectCount = document.getElementById("incorrectCount");
const correctCount = document.getElementById("correctCount");
const skipCount = document.getElementById("skipCount");

const correctSFX = document.querySelectorAll('audio[id^="correct"]');
const incorrectSFX = document.querySelectorAll('audio[id^="incorrect"]');

let skip = false;
let solution = "";

let directions = {
    "basic_algebra": "Find the value of x:  ",
    "combine_like_terms": "Put the expression in it's simplest form: ",
    "factoring": "Factor the quadratic into it's roots: ",
    "expanding": "Expand the factored binomial: ",
    "addition": "Find the sum: ",
    "simplify_square_roots": "Simplify the square root: ",
    "divide_fractions": "Find the quotient: "
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
            MathJax.typeset([mathProblemElement]);
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

function feedback(correctBool) {
    let className;
    if (correctBool == true) {
        className = "correct";
        pickRandomItem(correctSFX).play();
    } else if (correctBool == false){
        className = "incorrect";
        pickRandomItem(incorrectSFX).play();
    } else {
        className = "skip"
    }
    card.classList.add(className);
    setTimeout(() => {
        card.classList.remove(className);
    }, 1000);
}

function submit() {
    if (skip) {
        skip = false;
        sumbitButton.innerText = "Submit";
        mf.setValue("");
        mf.removeAttribute("inert");
        feedback();
        fetchProblem();
        skipCount.innerText = Number(skipCount.innerText) + 1;
    }
    if (mf.value) {
        if (mf.getValue("math-json") == solution) {
            correctCount.innerText = Number(correctCount.innerText) + 1;
            feedback(true);
        } else {
            incorrectCount.innerText = Number(incorrectCount.innerText) + 1;
            feedback(false);
        }
        fetchProblem();
        mf.setValue("");
    }
}

// Blur on buttons to prevent focus
sumbitButton.addEventListener("click", (event) => {
    submit();
    sumbitButton.blur();
});

solutionButton.addEventListener("click", (event) => {
    mf.value = ce.box(JSON.parse(solution)).latex;
    mf.setAttribute("inert", "");
    solutionButton.blur();
    skip = true;
    sumbitButton.innerText = "Next";
});

document.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        submit();
    }
});

window.onload = () => {
    mf.menuItems = mf.menuItems.filter(item => !menuExclusions.includes(item.id));
    document.title = cardTitle.innerText = toTitleCase(problemType.replaceAll("_", " "));
    if (directions[problemType]) {
        directionsElement.innerHTML = directions[problemType] + directionsElement.innerHTML
    } else {
        directionsElement.remove();
        mathProblemElement.parentElement.style.height = "2rem";
        mathProblemElement.parentElement.querySelector("br").remove();
    }
    fetchProblem();
}
