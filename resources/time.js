google.charts.load('current', {'packages': ['gantt']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Task ID');
    data.addColumn('string', 'Task Name');
    data.addColumn('string', 'Resource');
    data.addColumn('date', 'Start Date');
    data.addColumn('date', 'End Date');
    data.addColumn('number', 'Duration');
    data.addColumn('number', 'Percent Complete');
    data.addColumn('string', 'Dependencies');

    data.addRows([
        ['x', 'Analyse', 'resource',
            new Date(2016, 3, 1), new Date(2016, 4, 21), null, 100, null],
        ['machbarkeit', 'Machbarkeit prüfen', 'resource',
            new Date(2016, 3, 1), new Date(2016, 4, 21), null, 100, null],
        ['y', 'Funktionsumfang/Tools+Libaries', 'resource',
            new Date(2016, 3, 1), new Date(2016, 3, 4), null, 100, null],
        ['systemarchitektur', 'Systemarchitektur', 'resource',
            new Date(2016, 3, 6), new Date(2016, 3, 16), null, 100, null],
        ['a', 'Prototyp', 'resource',
            new Date(2016, 3, 6), new Date(2016, 4, 21), null, 100, null],
        ['b', 'Implementierung', 'resource',
            new Date(2016, 4, 22), new Date(2016, 6, 22), null, 0, null],
        ['c', 'Thesis schreiben', 'resource',
            new Date(2016, 4, 22), new Date(2016, 7, 28), null, 0, null],
    ]);

    var options = {
        height: 400,
        gantt: {
            trackHeight: 30
        }
    };

    var chart = new google.visualization.Gantt(document.getElementById('chart_div'));

    chart.draw(data, options);
}