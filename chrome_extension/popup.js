var testData = {
    "thisPage":5,
    "Cards": [
        {"Title": "4", 
        "Score": 1,
        "Date": "4444 44",
        "Publisher": "Jhin",
        "Author": "Idk who made numbers",
        "URL": "http://www.google.com",
        },
        {"Title": "4", 
        "Score": 1,
        "Date": "4444 44",
        "Publisher": "Jhin",
        "Author": "Idk who made numbers",
        "URL": "http://www.google.com",
        },
        {"Title": "4", 
        "Score": 1,
        "Date": "4444 44",
        "Publisher": "Jhin",
        "Author": "Idk who made numbers",
        "URL": "http://www.google.com",
        },
        {"Title": "4", 
        "Score": 1,
        "Date": "4444 44",
        "Publisher": "Jhin",
        "Author": "Idk who made numbers",
        "URL": "http://www.google.com",
        },
        {"Title": "4", 
        "Score": 1,
        "Date": "4444 44",
        "Publisher": "Jhin",
        "Author": "Idk who made numbers",
        "URL": "http://www.google.com",
        },
        {"Title": "4", 
        "Score": 1,
        "Date": "4444 44",
        "Publisher": "Jhin",
        "Author": "Idk who made numbers",
        "URL": "http://www.google.com",
        },
        {"Title": "4", 
        "Score": 1,
        "Date": "4444 44",
        "Publisher": "Jhin",
        "Author": "Idk who made numbers",
        "URL": "http://www.google.com",
        },
        {"Title": "Ey", 
        "Score": 3,
        "Date": "1234 11",
        "Publisher": "Me",
        "Author": "Him",
        "URL": "http://www.google.com",
        },
        {"Title": "Ey", 
        "Score": 3,
        "Date": "1234 11",
        "Publisher": "Me",
        "Author": "Him",
        "URL": "http://www.google.com",
        },
        {"Title": "Ey", 
        "Score": 5,
        "Date": "1234 11",
        "Publisher": "Me",
        "Author": "Him",
        "URL": "http://www.google.com",
        },
        {"Title": "Ey", 
        "Score": 9,
        "Date": "1234 11",
        "Publisher": "Me",
        "Author": "Him",
        "URL": "http://www.google.com",
        }
    ]
}

var scortedResult = testData.Cards.reduce(function (acc, curr) {
    acc[curr.Score] = acc[curr.Score] || [];
    acc[curr.Score].push(curr);
    return acc;
}, Object.create(null));

var frequenciesResult = {};

for (var key in scortedResult) {
    var value = scortedResult[key];
    frequenciesResult[key] = scortedResult[key].length
}

var cardJson = testData.Cards;
cardJson.forEach(function(item) {
    item.Color = scoreToColor(item.Score);
});

function scoreToColor(score) {
    var conversion = {
        10: "#1955F2",
        9: "#3053E1",
        8: "#4851CF",
        7: "#604FBD",
        6: "#784CAB",
        5: "#8F4A99",
        4: "#A74887",
        3: "#BE4676",
        2: "#D64464",
        1: "#EE4152",
    }

    return conversion[score];
}

String.prototype.format = function () {
    var i = 0, args = arguments;
    return this.replace(/{}/g, function () {
      return typeof args[i] != 'undefined' ? args[i++] : '';
    });
  };

$(window).ready(function() {
    function hideAllElements() {
        loopDelegate(this, x => x.hide());
    }

    function showAllElements() {
        loopDelegate(this, x => x.show());
    }

    function loopDelegate(self, func) {
        var keys = Object.keys(self.domElements);
        for(var i=0; i<keys.length; i++) {
            func(self.domElements[keys[i]]);
        }
    }

    function clickLinkEvent(event) {
        event.preventDefault();
        let targetPage = event.currentTarget.href;

        chrome.tabs.create({
            url: targetPage,
        });
    }

    var placeholderControl = {
        domElements: {
            instruction: $("#instruction"), 
            loading: $("#loading"), 
            empty: $("#empty"),
            placeholder: $("#placeholder"),
        },
        hideElements: function () {
            hideAllElements.call(this);
        },
        animations: [
            anime ({
                targets: "#loading",
                easing: "cubicBezier(0.215, 0.61, 0.355, 1)",
                translateY: [17,-17],
                direction: 'alternate',
                duration: 750,
                loop: true,
                autoplay: false,
            }),
            anime({
                targets: "#loading",
                backgroundColor: ["rgb(9, 87, 255)", "#F9414B"],
                easing: 'linear',
                direction: "alternate",
                duration: 2000,
                loop: true,
                autoplay: false,
            }),
        ],
        showElement: function(visibleElement) {
            this.hideElements();
            this.domElements.placeholder.show();
            visibleElement.show();

            if(visibleElement == this.domElements.loading) {
                this.animations.forEach(animation => animation.play());
            } else {
                this.animations.forEach(animation => animation.pause());
            }
        },
        init: function() {
            this.hideElements();
            return this;
        }
    }.init();
    
    var settingsControl = {
        domElements: {
            dots: $("#dots"),
            dropdown: $(".dropdown"),
        },
        states: {
            visible: {a:true},
            hidden: {b:false},
        },
        changeState: function(newState) {
            if (newState==this.states.visible) {
                this.domElements.dropdown.show();
                this.domElements.dots.toggleClass("active-target", true);
            } else if (newState==this.states.hidden) {
                this.domElements.dropdown.hide();
                this.domElements.dots.toggleClass("active-target", false);
            }
        },
        toggleStates: function() {
            this.domElements.dots.toggleClass("active-target");
            this.domElements.dropdown.toggle();
        },
        clickEvent: function(event) {
            var parent = event.data.self;
            if($(event.target).is("#dots")) {
                parent.toggleStates();
            } else {
                parent.changeState(parent.states.visible);
            }
        },
        offClickEvent: function(event) {
            var parent = event.data.self;
            target = $(event.target);

            if(!target.closest("#dots").length) {
                parent.changeState(parent.states.hidden);
            }
        },
        init: function () {
            this.domElements.dots.click({self: this}, this.clickEvent);
            $(document).click({self: this}, this.offClickEvent);
            this.changeState(this.states.hidden);
            return this;
        }
    }.init();

    var cardsControl = {
        domElements: {
            cardContainer: $("#card-container"),
            get cards() {
                return $(".card");
            },
            content: $("#items > div.simplebar-wrapper > div.simplebar-mask > div > div > div"),
        },
        clearCards: function() {
            this.domElements.cardContainer.html("");
        },
        changeCards: function(jsonData) {
            var container = this.domElements.cardContainer;

            var templateCard = Handlebars.template(precompiledTemplateCard);
            container.html(templateCard({Cards: jsonData}));
            
            placeholderControl.hideElements();
            var toggleState = this.domElements.content.prop("scrollHeight") > $("#histogram-spacer").prop("offsetHeight");
            container.toggleClass("card-scrollbar-active", toggleState);
            
            this.domElements.cards.slice(0, 6).addClass("slideIn");
        },
        init: function () {
            this.clearCards();

            this.domElements.cardContainer.on("click", "a", clickLinkEvent)

            return this;
        }
    }.init();

    var totalControl = {
        domElements: {
            total: $("#total"),
            totalNumber: $("#total-number"),
        },
        makeVisible: function() {
            showAllElements.call(this);
        },
        makeHidden: function () {
            hideAllElements.call(this);
        },
        _currentValue: 0,
        set currentValue(newValue) {
            this.changeValue(newValue);
            this._currentValue = newValue;
        },
        get currentValue() {
            return this._currentValue;
        },
        changeValue: function(newValue) {
            this.domElements.totalNumber.text(newValue);
        },
        init: function() {
            return this;
        }
    }.init();

    var thisSiteControl = {
        domElements: {
            thisSite: $(".this-site"),
        },
        showThisSite: function(index) {
            this.domElements.thisSite.hide();
            $(this.domElements.thisSite.toArray()[index-1]).show();
        },
        init: function() {
            hideAllElements.call(this);
            return this;
        },
    }.init();

    var scaleControl = {
        maxLengthofHistogram: 152,
        maxLengthOfSelectionLine: 31,
        domElements: {
            selectionLine: $(".selection-line"),
            histogramLine: $(".histogram-line"),
            histogramLineSpacer: $(".histogram-line-spacer"),
            circle: $(".circle"),
        },
        _selectedIndex: 0,
        set selectedIndex(newValue) {
            this.currentIndex = newValue;

            this.domElements.circle.text("");
            this.domElements.selectionLine.css("width", 0);
            $(this.domElements.selectionLine.toArray()[newValue]).css("width", this.maxLengthOfSelectionLine);
            $(this.domElements.circle.toArray()[newValue]).text(newValue+1);
        },
        get selectedIndex() {
            return this.currentIndex;
        },
        setUpHistogram: function(dataDictionary) {
            var valuesOfData = Object.values(dataDictionary);
            var maxValue = valuesOfData.reduce(function(acc, cur) {
                return Math.max(acc, cur);
            });
            for(var key in dataDictionary) {
                dataDictionary[key] = (dataDictionary[key]/maxValue) * this.maxLengthofHistogram;
                $(this.domElements.histogramLine.toArray()[key-1]).width(dataDictionary[key]);
            }
        },
        clickEvent: function() {
            var clickedIndex = $(this).index() - 1;
            var score = clickedIndex + 1;
            scaleControl.selectedIndex = clickedIndex;

            if(score in scortedResult) {
                cardsControl.changeCards(scortedResult[score]);
            } else {
                cardsControl.clearCards();
                placeholderControl.showElement(placeholderControl.domElements.empty);
            }
        },
        hoverOnEvent: function() {
            $(this).text($(this).index());
        },
        hoverOffEvent: function() {
            if(scaleControl.selectedIndex != $(this).index() - 1) {
                $(this).text("");
            }
        },
        init: function() {
            this.domElements.selectionLine.css("width", 0);
            this.domElements.circle.click(this.clickEvent);
            this.domElements.circle.hover(this.hoverOnEvent, this.hoverOffEvent);

            return this;
        }
    }.init();

    var bodyControl = {
        domElements: {
            content: $(".content"),
        },
        minimiseBody: function () {
            this.domElements.content.css("grid-template-columns", "350px 0px 0px");
        },
        maximiseBody: function () {
            this.domElements.content.css("grid-template-columns", "");
        },
        init: function () {
            this.minimiseBody();
            
            return this;
        }
    }.init();

    var dropdownControl = {
        domElements: {
            row: $(".dropdown>a")
        },
        init: function () {
            this.domElements.row.click(clickLinkEvent);
        }
    }.init();

    bodyControl.minimiseBody();
    placeholderControl.showElement(placeholderControl.domElements.loading);

    //stimulate loading
    setTimeout(function () {
        bodyControl.maximiseBody();
        placeholderControl.showElement(placeholderControl.domElements.instruction);
        thisSiteControl.showThisSite(testData.thisPage);
        totalControl.currentValue = cardJson.length;
        scaleControl.setUpHistogram(frequenciesResult);
    }, 300)
});