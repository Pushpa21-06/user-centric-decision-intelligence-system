const chartType =
document.getElementById(
"chartType"
);

const backBtn =
document.getElementById(
"backBtn"
);

const insightText =
document.getElementById(
"insightText"
);

const recommendationText =
document.getElementById(
"recommendationText"
);

const analysisText =
document.getElementById(
"analysisText"
);

let chart;


// ====================
// LOAD CHART
// ====================

async function loadChart(
type = "bar"
){

    const res =
    await fetch(
    "/get-results"
    );

    const data =
    await res.json();

    const ctx =
    document.getElementById(
    "resultChart"
    );

    if(chart)
    chart.destroy();

    chart =
    new Chart(
        ctx,
        {
            type:type,

            data:{

                labels:
                data.labels,

                datasets:[{
                    label:
                    data.y_axis,

                    data:
                    data.values,

                    borderWidth:1
                }]
            },

            options:{
                responsive:true,
                maintainAspectRatio:false
            }
        }
    );

    createNarrative(data);
}


// ====================
// AI STORY
// ====================

function createNarrative(
data
){

    const values =
    data.values;

    const total =
    values.reduce(
        (a,b)=>a+b,
        0
    );

    const avg =
    (
        total /
        values.length
    ).toFixed(2);

    const max =
    Math.max(
        ...values
    );

    const min =
    Math.min(
        ...values
    );

    const highest =
    data.labels[
    values.indexOf(max)
    ];

    const lowest =
    data.labels[
    values.indexOf(min)
    ];


    // =====================
    // INSIGHTS
    // =====================

    insightText.textContent =

    `The dataset presents
    noticeable variation in
    ${data.y_axis} across
    ${data.x_axis}. The highest
    recorded value was ${max}
    in ${highest}, whereas the
    lowest value was ${min}
    in ${lowest}. The average
    ${data.y_axis} observed
    throughout the dataset is
    ${avg}, indicating measurable
    fluctuations in performance.`;


    // =====================
    // RECOMMENDATIONS
    // =====================

    recommendationText
    .textContent =

    `Since ${highest} achieved
    the highest performance
    (${max}), similar strategies
    may be adopted for lower
    performing categories such
    as ${lowest}. Monitoring
    trends and identifying
    performance gaps can help
    improve consistency and
    support better decision
    making over time.`;


    // =====================
    // ANALYSIS
    // =====================

    analysisText
    .textContent =

    `The overall analysis shows
    that ${data.y_axis} is
    unevenly distributed across
    ${data.x_axis}. With a total
    value of ${total} and an
    average of ${avg}, certain
    categories contribute more
    significantly to the final
    outcome. This suggests scope
    for optimization, forecasting,
    and improved strategic
    planning.`;
}

// ====================
// EVENTS
// ====================

loadChart();

chartType.onchange =
() =>
loadChart(
chartType.value
);

backBtn.onclick =
() =>
window.location.href =
"/app/dashboard";