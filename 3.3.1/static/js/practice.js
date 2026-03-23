const mf = document.getElementById("mathField")
let menuExclusions = ["mode", "color", "background-color", "font-style", "accent", "decoration"]

window.onload = () => {
    mf.menuItems = mf.menuItems.filter(item => !menuExclusions.includes(item.id));
}