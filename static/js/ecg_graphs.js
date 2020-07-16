function drawLeads(params, data) {

    let NUM_LEADS = 12

    data = data.data
    const myNode = document.getElementById("graph");
    while (myNode.lastElementChild) {
        myNode.removeChild(myNode.lastElementChild);
    }

    for (let i = 0; i < NUM_LEADS; i++) {
        height_result = calc_height(data[i])
        width_result = Math.round(calc_width(data[i]))
        var height = height_result[2] - 18

        var div = document.createElement('div')
        div.className = "chart"
        div.id = "chartContainer" + i
        div.style = "position: relative; width: " + width_result + "%; height: " + height + "px;display: inline-block;"

        document.getElementById('graph').appendChild(div)
        drawSingleLead(i, 'chartContainer' + i, data[i], height_result, width_result)
    }

}

function calc_height(lead) {
    var max_round = Math.round(Math.max(...lead)) + 0.5
    var min_round = Math.round(Math.min(...lead)) - 0.5
    var height = (max_round - min_round) / 0.5 * 20 + 64
    return [max_round, min_round, height]
}

function calc_width(lead) {
    var length = lead.length / 20
    return length
}

async function drawSingleLead(lead, containerName, singleLeadData, height_result, width_result) {
    let leadNames = {
        0: "I",
        1: "II",
        2: "III",
        3: "aVR",
        4: "aVL",
        5: "aVF",
        6: "V1",
        7: "V2",
        8: "V3",
        9: "V4",
        10: "V5",
        11: "V6"
    }
    calc_height(singleLeadData)

    var xAxisStripLinesArray = [];
    var yAxisStripLinesArray = [];
    var dps = [];
    var dataPointsArray = singleLeadData;

    var max_round = height_result[0]
    var min_round = height_result[1]
    var height = height_result[2]

    var FREQ = 200 //HZ

    var chart = new CanvasJS.Chart(containerName, {
        height: height,
        zoomEnabled: true,
        animationEnabled: true,
        animationDuration: 2000,
        showInLegend: true,
        // title: {
        //     text: lead,
        // },
        subtitles: [{
            fontSize:15,
            text: "Lead " + leadNames[lead] + "      25мм/сек   10мм/мв,   mV: [" + min_round + "," + max_round + "]",
            horizontalAlign: "left",
        }],
        axisY: {
            stripLines: yAxisStripLinesArray,
            gridThickness: 0,
            gridColor: "#DC74A5",
            // lineColor: "#DC74A5",
            // tickColor: "#DC74A5",
            labelFontColor: "#DC74A5",
            valueFormatString: "0.0",
            labelFontSize: 10,
            minimum: min_round,
            maximum: max_round
        },
        axisX: {
            stripLines: xAxisStripLinesArray,
            // gridThickness: 2,
            gridColor: "#DC74A5",
            lineColor: "#DC74A5",
            // tickColor: "#DC74A5",
            labelFontColor: "#DC74A5",
            labelFormatter: function(e){
				return  e.value / FREQ;},
            valueFormatString: "0",
            labelFontSize: 10,
        },
        data: [{
            type: "spline",
            color: "black",
            dataPoints: dps
        }]
    });

    addDataPointsAndStripLines();
    await chart.render();

    function addDataPointsAndStripLines() {
        //dataPoints
        for (var i = 0; i < dataPointsArray.length; i++) {
            dps.push({
                y: dataPointsArray[i]
            });
        }
        //StripLines
        for (var i = i=-4; i < singleLeadData.length; i = i + 0.5) {
            yAxisStripLinesArray.push({
            value: i,
            thickness: 0.7,
            color: "#DC74A5"
        });
        }
        for (var i = 0; i < singleLeadData.length; i += (FREQ / 25)) {
            if (i % (FREQ / 5) !== 0) {
                xAxisStripLinesArray.push({
                value: i,
                thickness: 0.3,
                color: "#DC74A5"
            });
            } else if ( i % (FREQ / 5) == 0) {
                xAxisStripLinesArray.push({
                value: i,
                thickness: 1.5,
                color: "#DC74A5"
                });
            } else {
                xAxisStripLinesArray.push({
                value: i,
                thickness: 0.7,
                color: "#DC74A5"
            });
            }
        }
    }
}