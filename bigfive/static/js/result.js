'use strict';

// Renders a bar chart of percentile scores for every canvas.chart element,
// with the thresholds of low and high scores marked by dashed lines.
document.addEventListener('DOMContentLoaded', () => {
    const config = JSON.parse(document.getElementById('chart-config').textContent);

    const thresholdLine = (value, label, color) => ({
        type: 'line',
        scaleID: 'y',
        value,
        borderColor: color,
        borderDash: [10, 5],
        label: {
            display: true,
            content: label,
            backgroundColor: color
        }
    });

    document.querySelectorAll('canvas.chart').forEach((canvas) => {
        new Chart(canvas, {
            type: 'bar',
            data: {
                labels: canvas.dataset.labels.split('|'),
                datasets: [
                    {
                        label: canvas.dataset.title,
                        data: canvas.dataset.values.split(',').map(Number),
                        backgroundColor: 'rgba(1, 114, 173, 0.7)'
                    }
                ]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: config.labels.percentile
                        }
                    }
                },
                plugins: {
                    annotation: {
                        annotations: {
                            high: thresholdLine(config.high, config.labels.high, 'rgba(255, 99, 132, 0.8)'),
                            low: thresholdLine(config.low, config.labels.low, 'rgba(255, 159, 64, 0.8)')
                        }
                    }
                }
            }
        });
    });
});
