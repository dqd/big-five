document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('canvas.chart').forEach(function(canvas) {
        const labels = canvas.dataset.labels.split(',');
        new Chart(canvas, {
            type: 'bar',
            data: {
                labels,
                datasets: [
                    {
                        label: canvas.dataset.title,
                        data: canvas.dataset.values.split(',')
                    }
                ]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    annotation: {
                        annotations: {
                            high: {
                                type: 'line',
                                scaleID: 'y',
                                label: {
                                    display: true,
                                    content: translations.high,
                                    backgroundColor: 'rgba(255, 99, 132, 0.8)'
                                },
                                value: thresholds.high,
                                borderColor: 'rgba(255, 99, 132, 0.8)',
                                borderDash: [10, 5]
                            },
                            low: {
                                type: 'line',
                                scaleID: 'y',
                                label: {
                                    display: true,
                                    content: translations.low,
                                    backgroundColor: 'rgba(255, 159, 64, 0.8)'
                                },
                                value: thresholds.low,
                                borderColor: 'rgba(255, 159, 64, 0.8)',
                                borderDash: [10, 5]
                            }
                        }
                    }
                }
            }
        });
    });
});
