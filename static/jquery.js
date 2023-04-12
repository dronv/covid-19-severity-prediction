var predict_button = document.getElementById('predict_button');
predict_button.onclick = function(){

    var data = [
        {
            domain: { x: [0, 1], y: [0, 1] },
            value: prediction_value,
            title: { text: "Speed" },
            type: "indicator",
            mode: "gauge+number"
        }
    ];

    var layout = { width: 600, height: 500, margin: { t: 0, b: 0 } };
    Plotly.newPlot('myDiv', data, layout);
    }