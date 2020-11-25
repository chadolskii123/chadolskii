$(document).ready(function () {
    function renderChart(id, data, labels) {
        // var ctx = document.getElementById('myChart').getContext('2d');
        let ctx = $('#' + id)
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Sales',
                    data: data,
                    backgroundColor: [
                        'rgba(255, 159, 64, 0.2)'

                    ],
                    borderColor: [
                        'rgba(197, 77, 132, 1)',

                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },

            }
        });
    }

    function getSalesData(id, type) {
        let url = '/analytics/sales/data/'
        let method = "GET"
        let data = {"type": type}
        $.ajax({
            url: url,
            method: method,
            data: data,
            success: function (responseData) {
                renderChart(id, responseData.data, responseData.labels)
            },
            error: function (error) {
                $.alert("An Error Occurred")
            }
        })
    }

    let chartsToRender = $(".render-chart")
    $.each(chartsToRender, function (index, html) {
        let $this = $(this)
        if ($this.attr('id') && $this.attr('data-type')) {
            getSalesData($this.attr("id"), $this.attr("data-type"))
        }
    })


})