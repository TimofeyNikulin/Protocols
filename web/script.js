const committee = document.getElementById("committee");
const chapterLabel = document.getElementById("chapterLabel");
const deputyLabel = document.getElementById("deputyLabel");
const btn = document.querySelector("button");
const checkboxes = document.querySelectorAll(".checkClass").forEach((checkbox) => {
    checkbox.addEventListener('change', (event) => {
        addActivist(checkbox.getAttribute('name'))
    })
});
const checkboxesBSP = document.querySelectorAll(".checkClassBSP").forEach((checkbox) => {
    checkbox.addEventListener('change', (event) => {
        addActivist(checkbox.getAttribute('name'))
    })
});
const checkChapter = document.getElementById("chapter");
const checkDeputy = document.getElementById("deputy");
const tableBSP = document.querySelector(".tableBSP");
const tableNotBSP = document.querySelector(".tableNotBSP");
const dateInput = document.getElementById("dateInput");
const agendaInput = document.getElementById("agendaInput");
const solutionInput = document.getElementById("solutionInput");
const discussionInput = document.getElementById("disc");
const numberInput = document.getElementById("number");
const activists = [];
let activist_for_convert = [];
let committeeValue;
let chapter;
let deputy;
let date;
let agenda;
let solution;
let discussion;
let number;
let isFirst = true;

function changeCommittee() {
    let name = committee.value;
    eel.get_committee(name)(function(returnedData) {
        if (returnedData == "Не передано название комитета") {
            alert(returnedData)
        } else if (!(name == 'BSP')) {
            committeeValue = returnedData[0];
            chapter = returnedData[1];
            deputy = returnedData[2];
            chapterLabel.innerHTML = "Председатель: " + chapter;
            deputyLabel.innerHTML = "Зам. Председателя: " + deputy;
            if (tableNotBSP.classList.contains("hidden")) {
                tableNotBSP.classList.remove("hidden")
                tableBSP.classList.add("hidden")
            }
        } else {
            committeeValue = returnedData[0];
            chapter = returnedData[1];
            deputy = returnedData[2];
            chapterLabel.innerHTML = "Глава БСП: " + chapter;
            deputyLabel.innerHTML = "Зам. Главы: " + deputy;
            if (tableBSP.classList.contains("hidden")) {
                tableBSP.classList.remove("hidden")
                tableNotBSP.classList.add("hidden")
            }
        }       
    })
}

function addActivist(activist) {
    if (activist in activists) {
        activists.splice(activists.indexOf(activist), activists.indexOf(activist))
    } else {
        activists.push(activist)
    }
}

function convertData() {
    activist_for_convert = {};
    date = dateInput.value;
    number = numberInput.value;
    agenda = agendaInput.value;
    solution = solutionInput.value;
    discussion = discussionInput.value;
    if (checkChapter.checked) {
        activist_for_convert["chapter"] = chapter
    } else {
        activist_for_convert["chapter"] = ""
    }
    if (checkDeputy.checked) {
        activist_for_convert["deputy"] = deputy
    } else {
        activist_for_convert["deputy"] = ""
    }
    activist_for_convert["activists"] = activists
    eel.convert_to_doc(number, date, activist_for_convert, agenda, discussion, solution, committeeValue)(function(returnedData) {
        if (returnedData) {
            alert(returnedData)
        }
    })
}

btn.addEventListener('click', () => {
    convertData()
})