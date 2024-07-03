Highcharts.addEvent(Highcharts.Series, 'addPoint', e => {
    const point = e.point,
        series = e.target;

    if (!series.pulse) {
        series.pulse = series.chart.renderer.circle()
            .add(series.markerGroup);
    }
    setTimeout(() => {
        series.pulse
            .attr({
                x: series.xAxis.toPixels(point.x, true),
                y: series.yAxis.toPixels(point.y, true),
                r: series.options.marker.radius,
                opacity: 1,
                fill: series.color
            })
            .animate({
                r: 20,
                opacity: 0
            }, {
                duration: 1000
            });
    }, 1);
});

Highcharts.chart('container', {
    chart: {
        type: 'scatter',
        margin: [70, 50, 60, 80],
        events: {
            click: function (e) {
                const x = Math.round(e.xAxis[0].value),
                    y = Math.round(e.yAxis[0].value),
                    series = this.series[0];
                
                if (e.shiftKey){
                    var bluePointIndex = this.series[0].data.findIndex(function(point) {
                        return point.color === 'blue';
                    });
                    if (bluePointIndex < 0) {
                        // Add it
                        series.addPoint({
                            x: x,
                            y: y,
                            color: 'blue'
                        });
                    }
                }
                else {
                    var orangeCount = this.series[0].data.filter(point => point.color === 'orange').length;
                    if (orangeCount < 4) {
                        // Add it
                        series.addPoint({
                            x: x,
                            y: y,
                            color: 'orange'
                        });
                    }
                }
            
            }
        }
    },
    title: {
        text: 'TDOA and FDOA lines',
        align: 'left'
    },
    subtitle: {
        text: 'Left click the plot area to add a receiver. Shift + left click to add the emitter. Left click an existing point to remove it.',
        align: 'left'
    },
    accessibility: {
        announceNewData: {
            enabled: true
        }
    },
    xAxis: {
        title: {
            text: 'x'
        },
        min: 0,
        max: 100,
        gridLineWidth: 1,
        minPadding: 0.2,
        maxPadding: 0.2,
        maxZoom: 60
    },
    yAxis: {
        title: {
            text: 'y'
        },
        min: 0,
        max: 100,
        minPadding: 0.2,
        maxPadding: 0.2,
        maxZoom: 60,
        plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
        }]
    },
    legend: {
        enabled: false
    },
    exporting: {
        enabled: false
    },
    plotOptions: {
        series: {
            stickyTracking: false,
            lineWidth: 0,
            point: {
                events: {
                    click: function () {
                        if (this.series.data.length > 0) {
                            this.remove();
                        }
                    }
                }
            }
        }
    },
    series: [{
        data: [],
        color: Highcharts.getOptions().colors[3],
        marker: {
            lineWidth: 2,
            radius: 6
        }
    }]
});
