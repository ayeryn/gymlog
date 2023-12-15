document.addEventListener("DOMContentLoaded", function () {
  // Grab labels and values
  var labels = ["label 1"];
  var values = [1, 2, 3];
  // FIXME: not entirely sure if we can separate chart.js from html because of the flask variables
  //   var labels = {{ labels|tojson|safe }};
  //   var values = {{ values|tojson|safe }};

  var ctx = document.getElementById("weeklyReport").getContext("2d");
  var chartData = {
    labels: labels,
    datasets: [
      {
        label: "Attendances",
        data: values,
        backgroundColor: ["rgba(50, 205, 50, 0.5)"],
        borderColor: ["rgba(255, 255, 255, 1)"],
        borderWidth: 1,
      },
    ],
  };

  var chartOptions = {
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
          },
        },
      ],
    },
  };

  var myChart = new Chart(ctx, {
    type: "bar",
    data: chartData,
    options: chartOptions,
  });
});
