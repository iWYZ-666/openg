
function getYears() {
    let repository = $("#repository").find('option:selected').val()
    $.ajax({
        url: "/years",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({repository: repository}),
        dataType: "json",
        success: function (res) {
            console.log(res)
            let years = res["years"]
            $("#year").find("option").remove()
            $("#year").append(new Option("--请选择年份--"))
            for (let i = 0; i < years.length; i++) {
                $("#year").append(new Option(years[i], years[i]))
            }
        },
        error: function (res) {
            alert("getYears GG!")
        }
    })
}

function getMonths() {
    console.log('getMonths Start!')
    let repository = $("#repository").find('option:selected').val()
    let year = $("#year").find('option:selected').val()
    if (repository === "0" || year === "0")
        return
    console.log('It is all fine.')
    $.ajax({
        url: "/months",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            "repository": repository,
            "year": year
        }),
        dataType: "json",
        success: function (res) {
            console.log(res)
            let months = res["months"]
            $("#month").find("option").remove()
            $("#month").append(new Option("--请选择月份--"))
            for (let i = 0; i < months.length; i++) {
                $("#month").append(new Option(months[i], months[i]))
            }
            isMin = true
        },
        error: function (res) {
            alert("getMonths GG!")
        }
    })
}

function sendMinPost(point) {
    let id = point.id
    let kind = point.kind
    if (kind === 'r')
        return
    $.ajax({
        url:"/point",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            "year": year,
            "month": month,
            "id": id,
            "kind": kind
        }),
        dataType: "json",
        success: function (res) {
            console.log(res)
            // 画小图
        },
        error: function (res) {
            alert("sendMinPost GG!")
        }
    })
}

function sendPost() {
    year = $("#year").find('option:selected').val()
    month = $("#month").find('option:selected').val()
    repository = $("#repository").find('option:selected').val()
    $.ajax({
    url: "/",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({
        "year": year,
        "month": month,
        "repository": repository
    }),
    dataType: "json",
    success: function (res) {
            console.log(res)
            drawGraph(res)
        }
    ,
    error: function (res) {
        console.log(res)
        alert("sendPost GG!")
    }
})
}
