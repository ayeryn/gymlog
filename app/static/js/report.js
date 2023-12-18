document.addEventListener("DOMContentLoaded", function () {
  var ctx = document.getElementById(reportId).getContext("2d");
  var chartData = {
    labels: labels,
    datasets: [
      {
        label: "Attendances",
        data: values,
        backgroundColor: ["rgba(50, 205, 50, 0.5)"],
        borderColor: ["rgba(50, 205, 50, 1)"],
        borderWidth: 1,
      },
    ],
  };

  var chartOptions = {
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  var myChart = new Chart(ctx, {
    type: "bar",
    data: chartData,
    options: chartOptions,
  });
});
