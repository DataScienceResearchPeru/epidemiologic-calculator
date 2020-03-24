axios.get("/api/sird")
    .then(response => {
        let data = response.data;
        let type = "sird";
        console.log("data", data);
        graphics(data, type);
    })
    .catch(err => {
        console.log('err', err);
    });

axios.get("/api/seird")
    .then(response => {
        let data = response.data;
        let type = "seird";
        console.log("data", data);
        graphics(data, type);
    })
    .catch(err => {
        console.log('err', err);
    });

axios.get("/api/seaichurd")
    .then(response => {
        let data = response.data;
        let type = "seaichurd";
        console.log("data", data);
        graphics(data, type);
    })
    .catch(err => {
        console.log('err', err);
    });


function graphics(dataset, type) {
    let datasets = [{
                    label: "Suceptibles",
                    data: dataset.susceptible,
                    borderColor: "rgb(75, 192, 192)",
                    backgroundColor: "rgba(75, 192, 192, 0.1)",
                    borderWidth: 3,
                    pointBorderWidth: 1,
                    pointRadius: 3,
                    lineTension: 0.1,
                },
                {
                    label: "Infectados",
                    data: dataset.infected,
                    borderColor: "rgb(51, 92, 181)",
                    backgroundColor: "rgba(51, 92, 181, 0.1)",
                    borderWidth: 3,
                    pointBorderWidth: 1,
                    pointRadius: 3,
                    lineTension: 0.1,
                },
                {
                    label: "Recuperados",
                    data: dataset.recovered,
                    borderColor: "rgb(59, 136, 205)",
                    backgroundColor: "rgba(59, 136, 205, 0.1)",
                    borderWidth: 3,
                    pointBorderWidth: 1,
                    pointRadius: 3,
                    lineTension: 0.1,

                },
                {
                    label: "Muertos",
                    data: dataset.death,
                    borderColor: "rgb(255, 99, 132)",
                    backgroundColor: "rgba(255, 99, 132, 0.1)",
                    borderWidth: 3,
                    pointBorderWidth: 1,
                    pointRadius: 3,
                    lineTension: 0.1,
                }];

    if (type=="seird") {
        datasets.push({
                    label: "Expuestos",
                    data: dataset.exposed,
                    borderColor: "rgb(201, 203, 207)",
                    backgroundColor: "rgba(201, 203, 207, 0.1)",
                    borderWidth: 3,
                    pointBorderWidth: 1,
                    pointRadius: 3,
                    lineTension: 0.1,
        });
    }

    if (type=="seaichurd") {
        dataset_seaichurd=[{
                            label: "Expuestos",
                            data: dataset.exposed,
                            borderColor: "rgb(201, 203, 207)",
                            backgroundColor: "rgba(201, 203, 207, 0.1)",
                            borderWidth: 3,
                            pointBorderWidth: 1,
                            pointRadius: 3,
                            lineTension: 0.1,
                           },
                           {
                            label: "Asintomáticos",
                            data: dataset.asymptomatic,
                            borderColor: "rgb(54, 162, 235)",
                            backgroundColor: "rgba(54, 162, 235, 0.1)",
                            borderWidth: 3,
                            pointBorderWidth: 1,
                            pointRadius: 3,
                            lineTension: 0.1,
                           },
                           {
                            label: "Cuarentena",
                            data: dataset.quarantine,
                            borderColor: "rgb(255, 205, 86)",
                            backgroundColor: "rgba(255, 205, 86, 0.1)",
                            borderWidth: 3,
                            pointBorderWidth: 1,
                            pointRadius: 3,
                            lineTension: 0.1,
                           },
                           {
                            label: "Hospitalizados",
                            data: dataset.hospitalized,
                            borderColor: "rgb(153, 102, 255)",
                            backgroundColor: "rgba(153, 102, 255, 0.1)",
                            borderWidth: 3,
                            pointBorderWidth: 1,
                            pointRadius: 3,
                            lineTension: 0.1,
                           },
                           {
                            label: "UCI - Hospital",
                            data: dataset.uci,
                            borderColor: "rgb(201, 203, 207)",
                            backgroundColor: "rgba(201, 203, 207, 0.1)",
                            borderWidth: 3,
                            pointBorderWidth: 1,
                            pointRadius: 3,
                            lineTension: 0.1,
                           }];

        datasets = datasets.concat(dataset_seaichurd);
    }


    let options = {
        responsive: true,
        hoverMode: 'index',
        stacked: true,
        legend: {
            display: true
        },
        scales: {
            xAxes: [
                {
                    scaleLabel: {
                    display: true,
                    labelString: 'Tiempo (días)'
                    }

                }
            ],
            yAxes: [
                {
                   display: true,
                   position: 'left',
                   drawTicks: true,
                   scaleLabel: {
                    display: true,
                    labelString: 'Población'
                  }
                }
            ]
        }
    };

    let data = {
            labels: dataset.time,
            datasets: datasets
    }

    if (type == "sird") {
        new Chart(document.getElementById("chart-sird").getContext('2d'), {
            type: 'line',
            data: data,
            options: options
        });

    }

    if (type == "seird") {
        new Chart(document.getElementById("chart-seird").getContext('2d'), {
            type: 'line',
            data: data,
            options: options
        });
    }

    if (type == "seaichurd") {
        new Chart(document.getElementById("chart-seaichurd").getContext('2d'), {
            type: 'line',
            data: data,
            options: options
        });

        console.log("paso!!", data);
    }

}