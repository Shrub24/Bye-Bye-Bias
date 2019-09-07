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

String.prototype.trunc =
    function( n, useWordBoundary ){
        if (this.length <= n) { return this; }
        var subString = this.substr(0, n-1);
        return (useWordBoundary 
        ? subString.substr(0, subString.lastIndexOf(' ')) 
        : subString) + "&hellip;";
    };

$(window).ready(function() {
    function hideAllElements(self) {
        loopDelegate(self, element => element.hide());
    }

    function showAllElements(self) {
        loopDelegate(self, element => element.show());
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
            active: event.data.active,
        });
    }

    var placeholderControl = {
        domElements: {
            instruction: $("#instruction"), 
            loading: $("#loading"), 
            empty: $("#empty"),
            unknown: $("#unknown"),
            placeholder: $("#placeholder"),
            serverError: $("#serverError"),
        },
        hideElements: function () {
            hideAllElements(this);
        },
        animations: [
            /*
            anime({
                targets: "#loading",
                easing: "cubicBezier(0.215, 0.61, 0.355, 1)",
                translateY: [17,-17],
                direction: 'alternate',
                duration: 750,
                loop: true,
                autoplay: false,
            }),
            */
            /*
            anime({
                targets: "#loading",
                backgroundColor: ["rgb(9, 87, 255)", "#F9414B"],
                easing: 'linear',
                direction: "alternate",
                duration: 2000,
                loop: true,
                autoplay: false,
            }),
            */
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
            var letters = String(this.domElements.loading.text().trim());
            this.domElements.loading.html("");
            
            for(var i=0; i<letters.length; i++) {
                if(letters[i] === " ") {
                    var targetToAppend = "&nbsp;";
                } else {  
                    var targetToAppend = letters[i];
                }
                this.domElements.loading.append( $("<span>").html(targetToAppend).css("animation-delay", 
                    String((i - 20) * 2 * 0.3 / 20) + "s"));
            }
            this.hideElements();
            return this;
        }
    }.init();

    var checkboxControl = {
        domElements: {
            reduceAnimations: $("#reduceAnimations"),
            fetchOnLoad: $("#fetchOnLoad"),
        },
        setStorage: function(event) {
            localStorage.setItem($(event.target).attr('id'), $(this).is(':checked'));
        },
        resetToDefault: function(element, defaultValue) {
            var storageValue = localStorage.getItem(element.attr("id"));
            if(storageValue != "true" && storageValue != "false") {
                localStorage.setItem(element.attr("id"), defaultValue);
            }
            element.prop("checked", $.parseJSON(localStorage.getItem(element.attr("id"))));
        },
        init: function() {
            loopDelegate(this, element => element.click(this.setStorage));
            //Checked boxes are stored as their ID in local storage
            this.resetToDefault(this.domElements.reduceAnimations, true);
            this.resetToDefault(this.domElements.fetchOnLoad, true);
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
            

            if(!$.parseJSON(localStorage.getItem('reduceAnimations'))) {
                this.domElements.cards.slice(0, 6).addClass("slideIn");
            }
        },
        init: function () {
            this.clearCards();

            this.domElements.cardContainer.on("click", "a", {active:false}, clickLinkEvent)

            return this;
        }
    }.init();

    var totalControl = {
        domElements: {
            total: $("#total"),
            totalNumber: $("#total-number"),
        },
        makeVisible: function() {
            showAllElements(this);
        },
        makeHidden: function () {
            hideAllElements(this);
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
            hideAllElements(this);
            return this;
        },
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
            this.domElements.row.click({active: true}, clickLinkEvent);
        }
    }.init();

    var scaleControl = {
        maxLengthofHistogram: 157.8,
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
        setUpHistogram: function(dataDictionary, thisSite) {
            var valuesOfData = Object.values(dataDictionary);
            var maxValue = valuesOfData.reduce(function(acc, cur) {
                return Math.max(acc, cur);
            });
            for(var key in dataDictionary) {
                dataDictionary[key] = (dataDictionary[key]/maxValue) * this.maxLengthofHistogram;
                $(this.domElements.histogramLine.toArray()[key-1]).width(dataDictionary[key]);
            }
            if (dataDictionary[thisSite] == null) {
                $(this.domElements.histogramLine.toArray()[thisSite - 1]).width(5);
            }
        },
        cardData: {},
        clickEvent: function() {
            var clickedIndex = $(this).index() - 1;
            var score = clickedIndex + 1;
            
            if(score in scaleControl.cardData) {
                if(scaleControl.selectedIndex != clickedIndex)
                    cardsControl.changeCards(scaleControl.cardData[score]);
            } else {
                cardsControl.clearCards();
                placeholderControl.showElement(placeholderControl.domElements.empty);
            }

            scaleControl.selectedIndex = clickedIndex;
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
        },
    }.init();
    
    function activatePage(JSONdata) {
        //Parse data
        try {
            var data = JSON.parse(JSONdata);
            if(data.hasOwnProperty("unknown")) {
                data = "unknown";
            }
        } catch (error) {
            var data = JSONdata;
        }

        if(data == "unknown") {
            placeholderControl.showElement(placeholderControl.domElements.unknown);
        } else if (data=="error") {
            placeholderControl.showElement(placeholderControl.domElements.serverError);
        } else if(data != "fetching") {
            //All good to go

            //Organise by score
            var scortedResult = data.Cards.reduce(function (acc, curr) {
                acc[curr.Score] = acc[curr.Score] || [];
                acc[curr.Score].push(curr);
                return acc;
            }, Object.create(null));

            //Oragnise by frequencies
            var frequenciesResult = {};
            for (var key in scortedResult) {
                var value = scortedResult[key];
                frequenciesResult[key] = scortedResult[key].length
            }

            //Note: references the original object Cards
            var cardsWithColors = data.Cards;
            cardsWithColors.forEach(function(item) {
                item.Color = scoreToColor(item.Score);
                item.truncatedTitle = item.Title.trunc(95);
            });

            //Prepare page
            bodyControl.maximiseBody();
            placeholderControl.showElement(placeholderControl.domElements.instruction);
            thisSiteControl.showThisSite(data.thisPage);
            totalControl.currentValue = data.Cards.length;
            scaleControl.cardData = scortedResult;
            scaleControl.setUpHistogram(frequenciesResult, data.thisPage);
        }
    }

    //Show loading setup
    bodyControl.minimiseBody();
    placeholderControl.showElement(placeholderControl.domElements.loading);

    //Check if data has been cached
    var query = { active: true, currentWindow: true };

    chrome.tabs.query(query, function (tabs) {
        var currentTab = tabs[0];
        var data = localStorage.getItem(currentTab.url);
        var backgroundPage = chrome.extension.getBackgroundPage();

        //Data does not exist
        if(data == undefined || data == "fetching") {
            if(data != "fetching") {
                backgroundPage.fetchUrlAndStore(currentTab.url);
            }

            var count = 1;
            $(window).bind('storage', function(event) {
                var newValue = localStorage.getItem(event.originalEvent.key);
                if(event.originalEvent.key == currentTab.url && newValue != "fetching") {
                    if(count < 3) {
                        if(newValue != undefined) {
                            activatePage(localStorage.getItem(event.key));  
                        } else {
                            count += 1;
                            backgroundPage.fetchUrlAndStore(currentTab.url);
                        }
                    } else {
                        activatePage("error");
                    }
                } 
            });
        } else {
            //Cached results exists then immediately parse it
            activatePage(data);
        }
    });
});
