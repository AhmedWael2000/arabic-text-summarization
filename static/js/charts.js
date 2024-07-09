document.addEventListener('DOMContentLoaded', function () {
    const pieChartContainer = document.getElementById('pieChartContainer');
    const barChartContainer = document.getElementById('barChartContainer');
    const chartTypeSelect = document.getElementById('chartType');
    const groupedBarChart = document.getElementById('groupedBarChartContainer');

    chartTypeSelect.addEventListener('change', function () {
        if (chartTypeSelect.value === 'pie') {
            pieChartContainer.style.display = 'block';
            barChartContainer.style.display = 'none';
        } else {
            pieChartContainer.style.display = 'none';
            barChartContainer.style.display = 'block';
        }
    });

    // Fetch data for TFIDF Charts
    fetch('/count-data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const labels = data.labels;
            const pieChartData = {
                labels: labels,
                datasets: [{
                    label: 'توزيع الشكاوى', // Updated label to Arabic
                    data: data.data,
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
                }]
            };

            const ctxPie = document.getElementById('tfidfPieChart').getContext('2d');
            new Chart(ctxPie, {
                type: 'pie',
                data: pieChartData,
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'توزيع الشكاوى' // Updated title to Arabic
                        }
                    }
                }
            });

            // Reuse the data for the bar chart
            const barChartData = {
                labels: labels,
                datasets: [{
                    label: 'sentiment analysis ', // Updated label to Arabic
                    data: data.data,
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
                }]
            };

            const ctxBar = document.getElementById('tfidfBarChart').getContext('2d');
            new Chart(ctxBar, {
                type: 'bar',
                data: barChartData,
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'توزيع الشكاوى' // Updated title to Arabic
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching /count-data:', error);
        });
            });
// ////////////
        async function fetchData() {
        const response = await fetch('/sentiment-data');
        const data = await response.json();
        return data;
    }

    function processChartData(data) {
        const tfidfs = Object.keys(data);
        const sentiments = new Set();
        tfidfs.forEach(tfidf => {
            Object.keys(data[tfidf]).forEach(sentiment => {
                sentiments.add(sentiment);
            });
        });
        const colors = [
        { backgroundColor: 'rgba(255, 99, 132, 0.5)', borderColor: 'rgba(255, 99, 132, 1)' }, // Red
        { backgroundColor: 'rgba(75, 192, 192, 0.5)', borderColor: 'rgba(75, 192, 192, 1)' }, // Teal
        { backgroundColor: 'rgba(255, 159, 64, 0.5)', borderColor: 'rgba(255, 159, 64, 1)' }  // Orange
        ];

        const datasets = Array.from(sentiments).map((sentiment, index) => ({
            label: sentiment,
            data: tfidfs.map(tfidf => data[tfidf][sentiment] || 0),
            backgroundColor: colors[index % colors.length].backgroundColor,
            borderColor: colors[index % colors.length].borderColor,
            borderWidth: 1
        }));

        return {
            labels: tfidfs,
            datasets: datasets
        };
    }

    async function renderChart() {
        const data = await fetchData();
        const chartData = processChartData(data);

        const ctx = document.getElementById('groupedBarChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: 'Sentiment Analysis'
                    }
                },
                scales: {
                    x: {
                        stacked: true
                    },
                    y: {
                        stacked: true
                    }
                }
            }
        });
    }

    renderChart();
