//inheriting ngMaterial from Google, and overlay.js

var selected_call_number = [];
var event_sources = [];


$(document).ready(function () {
    // page is now ready, initialize the calendar..
    $('#calendar').fullCalendar({
        // put your options and callbacks here
        defaultView: 'agendaWeek',
        columnFormat: 'dddd',
        weekends: false,
        minTime: '08:00:00',
        maxTime: '21:00:00',
        header: {
            left: false,
            center: false,
            right: false
        },
        height: "parent",
        eventSources: function(){ return event_sources}()
    });
    event_sources = [{

}];

});


(function () {
    'use strict';

    angular.module('scheduler', ['ngMaterial', 'ngDialog'])
        .controller('cTabModule', cTabModule)
        .controller('cToggleNavigation', cToggleNavigation)
        .controller('cSideCtrl', cSideCtrl)
        .directive('tabNavigation', tabNavigation);

    //tab module for optimal class selections
    function cTabModule($scope, $log) {
        var tabs = [
                { title: 'One', content: "Tabs will become paginated if there isn't enough room for them." },
                { title: 'Two', content: "You can swipe left and right on a mobile device to change tabs." },
                { title: 'Three', content: "You can bind the selected tab via the selected attribute on the md-tabs element." },
                { title: 'Four', content: "If you set the selected tab binding to -1, it will leave no tab selected." },
                { title: 'Five', content: "If you remove a tab, it will try to select a new one." },
                { title: 'Six', content: "There's an ink bar that follows the selected tab, you can turn it off if you want." },
                { title: 'Seven', content: "If you set ng-disabled on a tab, it becomes unselectable. If the currently selected tab becomes disabled, it will try to select the next tab." },
                { title: 'Eight', content: "If you look at the source, you're using tabs to look at a demo for tabs. Recursion!" },
                { title: 'Nine', content: "If you set md-theme=\"green\" on the md-tabs element, you'll get green tabs." },
                { title: 'Ten', content: "If you're still reading this, you should just go check out the API docs for tabs!" }
        ],
            selected = null,
            previous = null;

        $scope.tabs = tabs;
        $scope.selectedIndex = 0;
        $scope.$watch('selectedIndex', function (current, old) {
            previous = selected;
            selected = tabs[current];
            if (old + 1 && (old != current)) $log.debug('Goodbye ' + previous.title + '!');
            if (current + 1) $log.debug('Hello ' + selected.title + '!');
        });
        $scope.addTab = function (title, view) {
            view = view || title + " Content View";
            tabs.push({ title: title, content: view, disabled: false });
        };
        $scope.removeTab = function (tab) {
            var index = tabs.indexOf(tab);
            tabs.splice(index, 1);
        };
    }

    //Toggles side Navigation bar on and off
    function cToggleNavigation($scope, $mdSidenav, $log) {
        $scope.toggleLeft = buildToggler('left');

        $scope.toggleLeft = function () {
            return $mdSidenav('left').toggle();
        };

        $scope.isSidebarOpen = function () {
            return $mdSidenav('left').isOpen();
        };

        function buildToggler(componentId) {
            return function () {
                $mdSidenav(componentId).toggle();
            }
        }

        $scope.close = function () {
            // Component lookup should always be available since we are not using `ng-if`
            $mdSidenav('left').close()
                .then(function () {
                    $log.debug("close LEFT is done");
                });
        };
    }

    //Side control options Scheduler/Courses
    function cSideCtrl($scope, $log, ngDialog) {
        var self = this;
        self.nav = 'course_info';
        self.searchTimeout = false;
		self.selectYear = 2016;

        self.semesters = [
            { id: '2016F', name: 'Fall 2016'},
            { id: '2016S', name: 'Spring 2016'},
            { id: '2017F', name: 'Fall 2017'}
        ];
        self.selectedSemester = { id: '2016S', name: 'Spring 2016'};
		
        self.toggleYear = function () {
			self.selectYear === 2016 ? self.selectYear = 2017 : self.selectYear = 2016 ;
        };
		
        self.selectedItemChange = function (text) {
            //$log.info('Text changed to ' + text);
        };

        self.searchTextChange = function (item) {
            //$log.info('Item changed to ' + JSON.stringify(item));
        };

        self.setNav = function (page) {
            console.log("nav = " + page);
            self.nav = page;
        };

        self.getNav = function () {
            return self.nav;
        };

        self.searchTree = function (searchString) {
            if (self.searchTimeout) {
                clearTimeout(self.searchTimeout);
            }
            self.searchTimeout = setTimeout(function () {
                $('#course_tree').jstree('search', searchString);
                //$('#course_tree').jstree(true).search(searchString);
            }, 300);
        };


        $('#course_tree')
			.on('changed.jstree', function (e, data) {
			    var i, j, r = [];
			    for (i = 0, j = data.selected.length; i < j; i++) {
			        console.log('Pushing: ' + data.instance.get_node(data.selected[i]).text);
			        r.push(data.instance.get_node(data.selected[i]).text);
			    }
			    console.log('Selected: ' + r.join(', '));

                $.get("/api/courses/info", { letter : data.node.a_attr['data-letter'], number : data.node.a_attr['data-number']})
                .done(function(data) {

                    console.log(data);
                    var dialog = ngDialog.open({
                                                template: 
													'<p>Course Info:</p>'+
													'<div><p>Name: ' + data.name + '</p><p>' + data.letter + ' ' + data.number +'</p></div>'+
													'<div><p>Description: </p>' + data.details + '</div>'+
													'<div><button class="inline close-this-dialog" ng-click="">Select Class</button></div>',
												className: 'ngdialog-theme-default', 
                                                plain: true, /*Change this to false for external templates */
                                                showClose: false,
                                                closeByDocument: true,
                                                closeByEscape: true,
                                                appendTo: false,
                    });
                });
                

			    
			})
			.jstree({
			    'core': {
			        'data': function (obj, cb) {
			            $.get("/api/courses/tree", function (data) {
			                cb.call(this, data.results);
			            });
			        }
			    },
			    "search": {
			        "case_insensitive": true,
			        "show_only_matches": true,
			        "multiple": false
			    },
			    "plugins": ["search"]
			});

			
        $('#schedule_tree')
			.on('changed.jstree', function (e, data) {
                var call_number;
			    var i, j, r = [];
			    for (i = 0, j = data.selected.length; i < j; i++) {
                    call_number = data.instance.get_node(data.selected[i]).a_attr['call-number']
                    if (call_number){
                        r.push(call_number);
                    }
			    }
			    selected_call_number = r;
                $.post('/api/schedule/combinations', {'call_numbers': r}).done(function (data) {
                    var calendar = $('#calendar');
                    calendar.fullCalendar('removeEvents');
                    calendar.fullCalendar('removeEventSources');
                    calendar.fullCalendar('addEventSource', data);
                    calendar.fullCalendar('refetchEvents');
                });

			})
			.jstree({
			    'core': {
			        'data': function (obj, cb) {
			            $.get("/api/schedule/tree", function (data) {
			                cb.call(this, data.results);
			            });
			        }
			    },
			    "search": {
			        "case_insensitive": true,
			        "show_only_matches": true,
			        "multiple": false
			    },
			    "checkbox": {
			        "keep_selected_style": false
			    },
			    "plugins": ["search", "checkbox"]
			});
        /**
         * Create filter function for a query string
         */
        function createFilterFor(query) {
            var lowercaseQuery = angular.lowercase(query);

            return function filterFn(item) {
                return (item.value.indexOf(lowercaseQuery) === 0) ||
                    (item.name.toLowerCase().indexOf(lowercaseQuery) === 0);
            };
        }
    }

    //Angular Element Directives
    function tabNavigation($log) {
        $log.info("tabNavigationFunction");
        return {
            restrict: 'E',
            templateUrl: 'static/html/tabNavigation.html'
        };
    }

})();
