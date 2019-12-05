var analyticsServerUrl = "http://localhost:8040/"

var storedSentimentData = []
var storedInterestData = []

var timescaleDict = { "Year": [365, 12], "Month": [30, 3], "Week": [7, 1] }
var timescaleOrder = { "Year": 3, "Month": 2, "Week": 1 }
var timeScale;
var oldScale;

window.onload = function () {
    var data = unpack_query();
    console.log(data.id);
    var email = data.email;
    var id = data.id;
    page_init(email, id)
}

function page_init(email, id) {
    //get request to analytics server
    // fetch(analyticsServerUrl + "?id=" + id + "&entity=NULL", {method: "GET"}).then(function (response) {
    fetch(analyticsServerUrl + "?id=" + id + "&entity=NULL", { method: "GET" }).then(function (response) {
        if (!response.ok) {
            return false
        }
        return response.text();
    }).then(function (body) {
        parsed = JSON.parse(body);
        var entitiesDropdown = document.getElementById("entities");
        var entities = parsed["entities"];
        timeScale = timescaleDict[$("input:radio[name='options']:checked").val()];
        addOptionsToDropdown(entities, entitiesDropdown);
        // changeTopicTitle(entitiesDropdown.options[entitiesDropdown.selectedIndex].text)
        // init starting blank graphs from first response
        // var sentiment = parsed["sentiment"];
        // var interest = parsed["interest"];
        // storedSentimentData = sentiment;
        // storedInterestData = interest;
        $('.selectpicker').selectpicker('val', entities[0]);
        selectionChanged();
        //generateGraphs(sentiment, interest, timeScale[0], timeScale[1]);
    });
    document.getElementById("email").innerHTML = email;
}

function unpack_query() {
    var url = document.location.href,
        params = url.split('?')[1].split('&'),
        data = {}, tmp;
    for (var i = 0, l = params.length; i < l; i++) {
        tmp = params[i].split('=');
        data[tmp[0]] = tmp[1];
    }
    return data
}

// gapiPromise = (function () {
//     var deferred = $.Deferred();
//     window.start = function () {
//         deferred.resolve(gapi);
//     };
//     return deferred.promise();
// }());
//
// auth2Promise = gapiPromise.then(function () {
//     var deferred = $.Deferred();
//     gapi.load('auth2', function () {
//         auth2 = gapi.auth2.init({
//             client_id: '154529731201-1fmdqacbv8re70076ljta1oqlnm2uc6l.apps.googleusercontent.com',
//             cookiepolicy: 'single_host_origin'
//         }).then(function () {
//             deferred.resolve(gapi.auth2);
//         });
//     });
//     return deferred.promise();
// });

function init() {
    gapi.load('auth2', function () {
        gapi.auth2.init();
    });
}

//todo fix signout with promises - can signout when gapi not loaded
function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
        window.location.href = "/"
    });
}

function addOptionsToDropdown(options, dropdown) {
    var option;
    for (option of options) {
        var op = new Option();
        op.text = option;
        dropdown.options.add(op)
    }
    $(".selectpicker").selectpicker("refresh")
}

function getCurrentSelection() {
    var dropdown = $(".selectpicker");
    return dropdown.find("option:selected").text();
}

function selectionChanged() {
    var id = unpack_query().id;
    var newSelection = getCurrentSelection();
    // changeTopicTitle(newSelection)
    fetch(analyticsServerUrl + "?id=" + id + "&entity=" + newSelection, { method: "GET" }).then(function (response) {
        if (!response.ok) {
            return false
        }
        return response.text();
    }).then(function (body) {
        parsed = JSON.parse(body);
        var sentiment = parsed["sentiment"]
        var interest = parsed["interest"]
        storedSentimentData = sentiment
        storedInterestData = interest
        generateGraphs(sentiment, interest, timeScale[0], timeScale[1])
    });
}

function changeTimeScale(scale) {
    timeScale = timescaleDict[scale]
    generateGraphs(storedSentimentData, storedInterestData, timeScale[0], timeScale[1])
}

function changeTopicTitle(text) {
    document.getElementById("topic").innerHTML = "Topic: " + text;
}

function changeData() {
    Plotly.animate('myDiv', {
        data: [{ y: [Math.random(), Math.random(), Math.random()] }],
        traces: [0],
        layout: {}
    }, {
        transition: {
            duration: 500,
            easing: 'cubic-in-out'
        },
        frame: {
            duration: 500
        }
    })
}

function generateGraphs(sentimentData, interestData, timespan, timegroups) {
    var formattedSentimentData = averageTimegroupsWithinTimespan(sentimentData, timespan, timegroups)
    var formattedInterestData = sumTimegroupsWithinTimespan(interestData, timespan, timegroups)
    var len = Math.ceil(timespan / timegroups)
    var sentimentGraph = {
        x: Array.from(Array(len).keys()),
        y: formattedSentimentData,
        name: "Sentiment",
        type: 'scatter',
        marker: {
            color: "#F9414B",
        },
    }
    var interestGraph = {
        x: Array.from(Array(len).keys()),
        y: formattedInterestData,
        name: "Interest",
        yaxis: "y2",
        type: 'scatter',
        marker: {
            color: "#4C8BF5",
        },
    }
    var graphElement = document.getElementById("graph");
    var data = [sentimentGraph, interestGraph]
    var getStyle = name => getComputedStyle(document.body).getPropertyValue(name);
    var currentScale = getCurrentScale();

    var ranges = {
        xaxis: { range: [0, len], title: "Time by " + currentScale },
        yaxis: { range: [0, 10], title: "Sentiment" },
        yaxis2: { title: "Interest", side: "right", overlaying: "y", range: [0, Math.max(...formattedInterestData) + 1] },
    };

    if ($("#graph").hasClass("js-plotly-plot")) {
        //If zooming in or changing topics
        var firstSetting = { layout: ranges };
        var secondSetting = { data: data };

        //If zooming out
        if (timescaleOrder[currentScale] > timescaleOrder[oldScale]) {
            //Then swap settings
            firstSetting = [secondSetting, secondSetting = firstSetting][0];
        }

        Plotly.update(graphElement,
            {},
            layout_update = {
                title: getCurrentSelection(),
            }
        );

        Plotly.animate(graphElement, {
            ...firstSetting,
            transition: {
                duration: 250,
                easing: 'cubic-in-out'
            },
        }).then(function () {
            Plotly.animate(graphElement, {
                ...secondSetting,
                transition: {
                    duration: 150,
                    easing: 'linear'
                },
            })
        });
    } else {
        var layout = {
            title: {
                text: getCurrentSelection(),
                font: {
                    family: getStyle("--font"),
                    size: 35,
                },
                xref: 'paper',
                x: 0.5,
                y: 0.91,
            },
            ...ranges,
            plot_bgcolor: getStyle("--blue-light"),
            paper_bgcolor: getStyle("--black-shade-light"),
            legend: { x: 1.05, y: 1.02 }
        }
        Plotly.newPlot(graphElement, data, layout, { responsive: true });
    }
    oldScale = currentScale;
}

function sumTimegroupsWithinTimespan(data, timespan, timegroups) {
    data = data.slice(timespan * -1)
    var newData = []
    var i = timespan % timegroups;
    if (i != 0) {
        newData = newData.concat(data.slice(0, i).reduce(function (acc, val) { return acc + val; }, 0));
    }
    for (; i <= data.length - timegroups; i += timegroups) {
        newData = newData.concat(data.slice(i, i + timegroups).reduce(function (acc, val) { return acc + val; }, 0));
    }
    return newData
}

function averageTimegroupsWithinTimespan(data, timespan, timegroups) {
    summedData = sumTimegroupsWithinTimespan(data, timespan, timegroups)
    if (timespan % timegroups == 0) {
        var i = 0
    }
    else {
        summedData[0] = summedData[0] / (timespan % timegroups)
        var i = 1
    }
    for (; i < summedData.length; i++) {
        summedData[i] = summedData[i] / timegroups
    }
    return summedData
}

function getCurrentScale() {
    return $("input:radio[name='options']:checked").val();
}

$(document).on("change", 'input:radio[name=options]', function (event) {
    changeTimeScale(getCurrentScale());
})