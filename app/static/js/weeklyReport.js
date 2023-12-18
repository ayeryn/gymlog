document.addEventListener("DOMContentLoaded", function () {
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
