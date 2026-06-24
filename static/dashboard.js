const fileInput =
document.getElementById("fileInput");

const fileText =
document.getElementById("fileText");

const analyzeBtn =
document.getElementById("analyzeBtn");

const modeSection =
document.getElementById("modeSection");

const autoMode =
document.getElementById("autoMode");

const manualMode =
document.getElementById("manualMode");

const manualOptions =
document.getElementById("manualOptions");

const resultBtn =
document.getElementById("resultBtn");

const xAxis =
document.getElementById("xAxis");

const yAxis =
document.getElementById("yAxis");

const historyBtn =
document.getElementById("historyBtn");

const historyPanel =
document.getElementById("historyPanel");

const logoutBtn =
document.getElementById("logoutBtn");

let file = null;
let mode = "";


// ====================
// HISTORY
// ====================

historyBtn.onclick = e => {

    e.stopPropagation();

    historyPanel
    .classList
    .toggle("show");

    loadHistory();
};

document.onclick = e => {

    if(
        !historyPanel.contains(e.target)
        &&
        !historyBtn.contains(e.target)
    ){

        historyPanel
        .classList
        .remove("show");
    }
};

async function loadHistory(){

    const res =
    await fetch("/history");

    const data =
    await res.json();

    const area =
    document.querySelector(
    ".history-content"
    );

    area.innerHTML = "";

    data.forEach(i => {

        area.innerHTML += `
        <div class="history-card">
            <h4>${i.filename}</h4>
            <p>
                ${i.time}
                •
                ${i.mode}
            </p>
        </div>`;
    });
}


// ====================
// FILE
// ====================

fileInput.onchange = () => {

    file =
    fileInput.files[0];

    fileText.textContent =
    file.name;
};


// ====================
// ANALYZE
// ====================

analyzeBtn.onclick = () => {

    if(!file){

        alert(
        "Upload file first"
        );

        return;
    }

    modeSection.style.display =
    "block";
};


// ====================
// AUTO MODE
// ====================

autoMode.onclick =
async () => {

    mode = "auto";

    await sendData();

    resultBtn.style.display =
    "block";

    manualOptions.style.display =
    "none";
};


// ====================
// MANUAL MODE
// ====================

manualMode.onclick =
async () => {

    mode = "manual";

    const form =
    new FormData();

    form.append(
    "file",
    file
    );

    form.append(
    "mode",
    "manual"
    );

    const res =
    await fetch(
    "/analyze",
    {
        method:"POST",
        body:form
    });

    const data =
    await res.json();

    xAxis.innerHTML =
    "<option>Select X Axis</option>";

    yAxis.innerHTML =
    "<option>Select Y Axis</option>";

    data.columns.forEach(c => {

        xAxis.innerHTML +=
        `<option value="${c}">
        ${c}
        </option>`;

        yAxis.innerHTML +=
        `<option value="${c}">
        ${c}
        </option>`;
    });

    manualOptions.style.display =
    "block";

    resultBtn.style.display =
    "block";
};


// ====================
// SEND DATA
// ====================

async function sendData(){

    const form =
    new FormData();

    form.append(
    "file",
    file
    );

    form.append(
    "mode",
    mode
    );

    form.append(
    "x_axis",
    xAxis.value
    );

    form.append(
    "y_axis",
    yAxis.value
    );

    await fetch(
    "/analyze",
    {
        method:"POST",
        body:form
    });
}


// ====================
// RESULT
// ====================

resultBtn.onclick =
async () => {

    if(
        mode === "manual"
    ){

        if(
            xAxis.selectedIndex === 0
            ||
            yAxis.selectedIndex === 0
        ){

            alert(
            "Select X and Y axis"
            );

            return;
        }

        await sendData();
    }

    window.location.href =
    "/app/results";
};


// ====================
// LOGOUT
// ====================

logoutBtn.onclick =
() =>
window.location.href =
"/app";