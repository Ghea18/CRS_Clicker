function showChart(text, number) {
    var canvas = document.getElementById('myChart');
    canvas.style.height = '400px';
    canvas.style.width = '800px';
    var ctx = canvas.getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: text,
            datasets: [{
                    label: 'A',
                    data: number[0],
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                },
                {
                    label: 'B',
                    data: number[1],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'C',
                    data: number[2],
                    backgroundColor: 'rgba(255, 206, 86, 0.2)',
                    borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 1
                },
                {
                    label: 'D',
                    data: number[3],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'E',
                    data: number[4],
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            title: {
                display: true,
                text: 'Cumulative Response'
            },
            tooltips: {
                mode: 'index',
                intersect: false
            },
            responsive: true,
            aspectRatio: 3,
            scales: {
                xAxes: [{
                    stacked: false,
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    },
                    stacked: false
                }]
            }
        }
    });
}
document.addEventListener('DOMContentLoaded', () => {
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    // When connected, configure buttons
    socket.on('connect', () => {
        // Each button should emit a "submit response" event
        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
                // When button clicked emit a dataset
                const response = button.dataset.input;
                const selection = button.dataset.response;
                console.log(response);
                console.log(selection);
                socket.emit(response, {
                    'selection': selection
                });
            };
        });
        document.querySelectorAll('input').forEach(input => {
            input.onclick = () => {
                // When button clicked emit a dataset
                const response = input.dataset.input;
                console.log(response);
                socket.emit(response);
            };
        });
        //socket.emit('timer');
    });
    socket.on('response admin_totals', data => {
        let chart = [
            [],
            [],
            [],
            [],
            []
        ];
        let label = [];
        for (var num in data) {
            console.log(data[num]);
            chart[0].push(data[num]['A']);
            chart[1].push(data[num]['B']);
            chart[2].push(data[num]['C']);
            chart[3].push(data[num]['D']);
            chart[4].push(data[num]['E']);
            label.push(parseInt(num) + 1);
        }
        showChart(label, chart);
    });
    socket.on('response admin_people', data => {
        console.log(data);
        responden = '';
        for (let num = 0; num < data.length; num++) {
            const name = data[num];
            responden += name + ', '
        }
        document.querySelector('#responden').innerHTML = responden;
    });
});
