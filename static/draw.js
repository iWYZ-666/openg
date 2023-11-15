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






// 饼状图 
(function() {
    // 基于准备好的dom，初始化echarts实例
    var myChart_pie = echarts.init(document.querySelector(".pie .chart"));

    var xAxisData = [

        1,2,3
    ];
    var data1 = [

        1,2,3
    ];


    var option_pie = {

        legend: {
            data: ['openRange'],
            // 距离容器10%
            right: "10%",
            // 修饰图例文字的颜色
            textStyle: {
                color: "#4c9bfd"
            }
            // 如果series 里面设置了name，此时图例组件的data可以省略
            // data: ["邮件营销", "联盟广告"]
        },

        tooltip: {
            trigger: "axis"
        },
        xAxis: {
            data: xAxisData,
            splitLine: {
                show: false
            }
        },
        yAxis: {},
        series: [
            {
                name: 'base',
                type: 'bar',
                data: data1,
                emphasis: {
                    focus: 'series'
                },
                animationDelay: function (idx) {
                    return idx * 10;
                }
            },
            
        ],
        animationEasing: 'elasticOut',
        animationDelayUpdate: function (idx) {
            return idx * 5;
        }
    };

    var dataAll = [

    ];

    // 使用刚指定的配置项和数据显示图表。
    // myChart_pie.setOption(option_pie);
    // $(".pie h2 ").on("click", "a", function() {
    //     var dataIndex = $(this).index() - 1;
    //     option_pie.xAxis.data = dataAll[dataIndex][0];
    //     option_pie.series[0].data = dataAll[dataIndex][1];

    //     option_pie.series[1].data = dataAll[dataIndex][2];
    //     myChart_pie.setOption(option_pie);
    // });
    window.addEventListener("resize", function() {
        myChart_pie.resize();
    });
})();

(function() {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.querySelector(".line1 .chart"));

    option = {
      tooltip: {
        trigger: "axis",
        axisPointer: {
          lineStyle: {
            color: "#dddc6b"
          }
        }
      },
      legend: {
        top: "0%",
        textStyle: {
          color: "rgba(255,255,255,.5)",
          fontSize: "12"
        }
      },
      grid: {
        left: "10",
        top: "30",
        right: "10",
        bottom: "10",
        containLabel: true
      },

      xAxis: [
        {
          type: "category",
          boundaryGap: false,
          axisLabel: {
            textStyle: {
              color: "rgba(255,255,255,.6)",
              fontSize: 12
            }
          },
          axisLine: {
            lineStyle: {
              color: "rgba(255,255,255,.2)"
            }
          },

          data: [
            // {% for item in fig_score_dis_data.0.data.0 %}
            //       '{{ item }}',
            //   {% endfor %}
          ]
        },
        {
          axisPointer: { show: false },
          axisLine: { show: false },
          position: "bottom",
          offset: 20
        }
      ],

      yAxis: [
        {
          type: "value",
          axisTick: { show: false },
          axisLine: {
            lineStyle: {
              color: "rgba(255,255,255,.1)"
            }
          },
          axisLabel: {
            textStyle: {
              color: "rgba(255,255,255,.6)",
              fontSize: 12
            }
          },

          splitLine: {
            lineStyle: {
              color: "rgba(255,255,255,.1)"
            }
          }
        }
      ],
      series: [
        {
          name: "number",
          type: "line",
          smooth: true,
          symbol: "circle",
          symbolSize: 5,
          showSymbol: false,
          lineStyle: {
            normal: {
              color: "#0184d5",
              width: 2
            }
          },
          areaStyle: {
            normal: {
              color: new echarts.graphic.LinearGradient(
                0,
                0,
                0,
                1,
                [
                  {
                    offset: 0,
                    color: "rgba(1, 132, 213, 0.4)"
                  },
                  {
                    offset: 0.8,
                    color: "rgba(1, 132, 213, 0.1)"
                  }
                ],
                false
              ),
              shadowColor: "rgba(0, 0, 0, 0.1)"
            }
          },
          itemStyle: {
            normal: {
              color: "#0184d5",
              borderColor: "rgba(221, 220, 107, .1)",
              borderWidth: 12
            }
          },
          data: [
            //   {% for item in fig_score_dis_data.0.data.1 %}
            //       {{ item }},
            //   {% endfor %}
          ]
        },
        
      ]
    };
    // 一样的格式化数据
  var dataALL = [
    //   {% for item in fig_score_dis_data %}
    //   [
    //     {% for item2 in item.data.0 %}
    //       {{ item2 }},
    //     {% endfor %}
    //   ],
    // {% endfor %}
  ];
  var dataALL_base = [
    //   {% for item in fig_score_dis_data %}
    //   [
    //     {% for item2 in item.data.1 %}
    //       {{ item2 }},
    //     {% endfor %}
    //   ],
    // {% endfor %}
  ];
  var dataALL_peak = [
    // {% for item in fig_score_dis_data %}
    //   [
    //     {% for item2 in item.data.2 %}
    //       {{ item2 }},
    //     {% endfor %}
    //   ],
    // {% endfor %}
  ];

    // 使用刚指定的配置项和数据显示图表。
  myChart.setOption(option);
      window.addEventListener("resize", function() {
      myChart.resize();
  });
  $(".line1 h2 ").on("click", "a", function() {
       

      var dataIndex = $(this).index() - 1;
      option.xAxis.data = dataALL[dataIndex];
      option.series[0].data = dataALL_base[dataIndex];
    //   {#console.log(dataALL_base[dataIndex]);#}
      option.series[1].data = dataALL_peak[dataIndex];

      myChart.setOption(option);
  });

  })();
