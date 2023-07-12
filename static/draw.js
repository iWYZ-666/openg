// var container = document.getElementById('graph');
// var chart = echarts.init(container);

var chartDom = document.getElementById('main');
var bigData
var year = 0
var month = 0
var repository = ""
var isMin = false
var typeMap = new Map([
    ['r', 'repo'], ['i', 'issue'], ['p', 'pull'], ['u', 'user']
]);


var clearDiv = id => {
    let div = document.getElementById(id);
    if (div && div.hasChildNodes()) {
        let children = div.childNodes;
        for (let child of children) {
            div.removeChild(child);
        }
    }
}

var addRow = (table, texts) => {
    let tr = table.insertRow();
    for (let t of texts) {
        let td = tr.insertCell();
        td.appendChild(document.createTextNode(t));
    }
}

var genName = node => (node.c === 'i' || node.c === 'p') ?
    `#${node.n.toString()}` : node.n.toString();


var setLeaderboard = graph => {
    clearDiv('leaderboard_div');
    var table = document.getElementById('leaderboard_table');
    addRow(table, ['#', 'Login', 'OpenRank']);
    var users = graph.nodes.filter(c => c.c === 'u').sort((a, b) => b.v - a.v);
    var i = 1;
    for (var u of users) {
        if (i > 10) break;
        addRow(table, [i, u.n, u.v]);
        i += 1;
    }
}

var setDetails = (graph, node) => {
    console.log(node)
    clearDiv('details_table');
    let table = document.getElementById('details_table');
    addRow(table, ['From', 'Ratio', 'Value', 'OpenRank']);
    addRow(table, ['Self', node.v, node.v, (node.v * node.v).toFixed(3)]);
    var other = graph.links.filter(l => l.t == node.id).map(l => {
        var source = graph.nodes.find(n => n.id == l.s);
        return [
            genName(source),
            parseFloat((1 - node.v) * l.w).toFixed(3),
            source.v,
            parseFloat(((1 - node.v) * l.w * source.v).toFixed(3))
        ];
    }).sort((a, b) => b[3] - a[3]);
    for (var r of other) {
        addRow(table, r);
    }
}

var onGraphDataLoaded = graph => {
    var chart = echarts.init(chartDom)
    setLeaderboard(graph);
    let nodes = graph.nodes.map(node => {
        return {
            id: node.id,
            name: genName(node),
            symbolSize: Math.log(node.v + 1) * 6,
            value: node.v,
            category: typeMap.get(node.c),
        };
    });

    let links = graph.links.map(link => {
        return {
            source: link.s,
            target: link.t,
            value: link.w,
        };
    });
    let categories = Array.from(typeMap.values());
    option = {
        title: {
            text: `OpenRank Graphs`,
            top: 'bottom',
            left: 'center'
        },
        legend: [
            {
                data: categories,
            }
        ],
        tooltip: {
            trigger: 'item',
        },
        series: [
            {
                name: 'Collaborative graph',
                type: 'graph',
                layout: 'force',
                nodes,
                links,
                categories: categories.map(c => {
                    return {name: c};
                }),
                roam: true,
                label: {
                    position: 'right',
                    show: true,
                },
                force: {
                    layoutAnimation: false,
                    repulsion: 300
                },
            }
        ]
    };
    chart.setOption(option);
    chart.on('dblclick', function (params) {
        setDetails(bigData, bigData.nodes.find(i => i.id === params.data.id));
    });
}

function drawGraph(res) {
    let repoName = $("#repository").find('option:selected').val()
    let graph = res
    bigData = res
    onGraphDataLoaded(graph)
}

function drawMinGraph(res) {

}







