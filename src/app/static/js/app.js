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
        header: false,
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
        .controller('cOverlayCtrl', cOverlayCtrl)
        .directive('tabNavigation', tabNavigation);

    //tab module for optimal class selections
    function cTabModule($scope, $log, $rootScope) {
        var tabs = [{title : 'Option 1', disabled : true},
                    {title : 'Option 2', disabled : true},
                    {title : 'Option 3', disabled : true},
                    {title : 'Option 4', disabled : true},
                    {title : 'Option 5', disabled : true},
                    {title : 'Option 6', disabled : true},
                    {title : 'Option 7', disabled : true},
                    {title : 'Option 8', disabled : true},
                    {title : 'Option 9', disabled : true},
                    {title : 'Option 10', disabled : true}
                ];
        var selected = null;
        var previous = null;

        $scope.tabs = tabs;
        $scope.selectedIndex = 0;
        $rootScope.selectedOption = 0;
        $scope.$watch('selectedIndex', function (current, old) {
            $rootScope.selectedOption = current - 1;
            $log.info($rootScope.selectedOption);

            $rootScope.$emit('onOptionChange');
        });

        $rootScope.$on('addTabs', function(event, args) {
            $log.info('cTabModule.onEvent:' + args);

            // clear array
            //$scope.tabs = [];
            var total_tabs = parseInt(args);
            var i;
            for (i = 0; i < total_tabs; i++) {
                //$scope.addTab('Option ' + (i + 1));
                if (i >= 10) {
                    break;
                }

                $scope.tabs[i].disabled = false;
            }
            $log.info($scope.tabs);
            //$('#stev-content-tab').load(document.URL +  ' #stev-content-tab');
        });


        $scope.addTab = function (title) {
            $log.info('title:' + title);
            $scope.tabs.push({ title: title, disabled: false });
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
    function cSideCtrl($scope, $log, $rootScope, ngDialog) {
        var self = this;
        self.nav = 'course_info';
        self.searchTimeout = false;
		self.selectYear = 2016;

        self.semesters = [
            { id: '2016F', name: 'Fall 2016'},
            { id: '2016S', name: 'Spring 2017'},
            { id: '2017F', name: 'Fall 2017'}
        ];
        self.selectedSemester = { id: '2016S', name: 'Spring 2016'};
		
        self.setSemester = function () {
			$log.info('setSemester:' + self.selectedSemester.name);
            $.get("/api/schedule/tree", { semester : self.selectedSemester.id }, function (data) {
                        $('#schedule_tree').jstree(true).settings.core.data = data.results;
                        $('#schedule_tree').jstree(true).refresh();
            });
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

        self.clearSelected = function() {
            $('#schedule_tree').jstree(true).deselect_all();
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
                                                    '<div ng-controller="cOverlayCtrl as overlay">' +
													'<p>Course Info:</p>'+
													'<div><p>Name: ' + data.name + '</p><p>' + data.letter + ' ' + data.number +'</p></div>'+
													'<div><p>Description: </p>' + data.details + '</div>'+
                                                    '<br />' +
													'<div><button class="inline close-this-dialog" ng-click="overlay.selectCourseCb(\'' + data.letter.replace( /^#\?/, "" ) + '\',' + data.number + ')">Select Class</button></div>' +
                                                    '</div>',
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

        $rootScope.$on('onOptionChange', function(event) {
            if ($rootScope.selectedOption > -1) {
                $log.info('onOptionChange');
                var calendar = $('#calendar');
                calendar.fullCalendar('removeEvents');
                calendar.fullCalendar('removeEventSources');
                calendar.fullCalendar('addEventSource', $rootScope.calendarData[$rootScope.selectedOption]);
                calendar.fullCalendar('refetchEvents');
                calendar.fullCalendar('rerenderEvents');

                $log.info('setting event source to');
                $log.info($rootScope.calendarData[$rootScope.selectedOption]);
            }
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
                $log.info('selectedSemester:' + self.selectedSemester.id);
                $.post('/api/schedule/combinations', {'semester': self.selectedSemester.id, 'call_numbers': r}).done(function (data) {

                    $rootScope.calendarData = data;
                    $rootScope.$emit('addTabs', $rootScope.calendarData.length);
                    
                    var calendar = $('#calendar');
                    calendar.fullCalendar('removeEvents');
                    calendar.fullCalendar('removeEventSources');
                    calendar.fullCalendar('addEventSource', $rootScope.calendarData[$rootScope.selectedOption]);
                    calendar.fullCalendar('refetchEvents');
                    calendar.fullCalendar('rerenderEvents');
                });

			})
			.jstree({
			    'core': {
			        'data': function (obj, cb) {
			            $.get("/api/schedule/tree", { semester : self.selectedSemester.id }, function (data) {
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
			        "keep_selected_style": false,
                    "check_callback": true
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

    // overlay controller
    function cOverlayCtrl($scope, $log) {
        var self = this;
        self.selectCourseCb = function(course_letter, course_number) {
            $log.info('selectCourseCb:' + course_letter + course_number);
            $('#schedule_tree').jstree(true).select_node(course_letter + ' ' + course_number);
        };
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
