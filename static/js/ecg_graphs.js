function drawLeads(params, data) {

    let NUM_LEADS = 12

    data = data.data
    const myNode = document.getElementById("graph");
    while (myNode.lastElementChild) {
        myNode.removeChild(myNode.lastElementChild);
    }

    for (let i = 0; i < NUM_LEADS; i++) {
        var div = document.createElement('div')
        div.className = "chart"
        div.id = "chartContainer" + i
        div.style = "position: relative; width: 100%; height: 150px;display: inline-block;"
        document.getElementById('graph').appendChild(div)
        drawSingleLead(i, 'chartContainer' + i, data[i])
    }

}

function drawSingleLead(lead, containerName, singleLeadData) {
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

    var xAxisStripLinesArray = [];
    var yAxisStripLinesArray = [];
    var dps = [];
    var dataPointsArray = singleLeadData;

    var chart = new CanvasJS.Chart(containerName, {
        height: 160,
        zoomEnabled: true,
        animationEnabled: true,
        animationDuration: 2000,
        showInLegend: true,
        // title: {
        //     text: lead,
        // },
        subtitles: [{
            fontSize:15,
            text: "Lead " + leadNames[lead] + "      25мм/сек   10мм/мв",
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
        },
        axisX: {
            stripLines: xAxisStripLinesArray,
            // gridThickness: 2,
            gridColor: "#DC74A5",
            lineColor: "#DC74A5",
            // tickColor: "#DC74A5",
            labelFontColor: "#DC74A5",
            labelFormatter: function(e){
				return  e.value / 1000;},
            valueFormatString: "0",
        },
        data: [{
            type: "spline",
            color: "black",
            dataPoints: dps
        }]
    });

    addDataPointsAndStripLines();
    chart.render();

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
        for (var i = 0; i < singleLeadData.length; i += 40) {
            if (i % 200 !== 0) {
                xAxisStripLinesArray.push({
                value: i,
                thickness: 0.3,
                color: "#DC74A5"
            });
            } else if ( i % 1000 == 0) {
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