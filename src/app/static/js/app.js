
//you can inherit application modules here like ngMaterial, custom
var app = angular.module('scheduler', ['ngMaterial']);
//Calendar module
app.controller('cCalendarModule', function($scope, $log){
	$scope.dp = new DayPilot.Calendar("dp");
	$scope.dp.viewType = "Week";
	$scope.dp.theme = 'calendar_g';
	$scope.dp.headerDateFormat = 'dddd';
	$scope.dp.init();
});

//tab module for optimal class selections
app.controller('cTabModule', function($scope, $log){
	var tabs = [
		{ title: 'One', content: "Tabs will become paginated if there isn't enough room for them."},
		{ title: 'Two', content: "You can swipe left and right on a mobile device to change tabs."},
		{ title: 'Three', content: "You can bind the selected tab via the selected attribute on the md-tabs element."},
		{ title: 'Four', content: "If you set the selected tab binding to -1, it will leave no tab selected."},
		{ title: 'Five', content: "If you remove a tab, it will try to select a new one."},
		{ title: 'Six', content: "There's an ink bar that follows the selected tab, you can turn it off if you want."},
		{ title: 'Seven', content: "If you set ng-disabled on a tab, it becomes unselectable. If the currently selected tab becomes disabled, it will try to select the next tab."},
		{ title: 'Eight', content: "If you look at the source, you're using tabs to look at a demo for tabs. Recursion!"},
		{ title: 'Nine', content: "If you set md-theme=\"green\" on the md-tabs element, you'll get green tabs."},
		{ title: 'Ten', content: "If you're still reading this, you should just go check out the API docs for tabs!"}
	],
	selected = null,
	previous = null;
	
	$scope.tabs = tabs;
	$scope.selectedIndex = 0;
	$scope.$watch('selectedIndex', function(current, old){
		previous = selected;
		selected = tabs[current];
		if ( old + 1 && (old != current)) $log.debug('Goodbye ' + previous.title + '!');
		if ( current + 1 )                $log.debug('Hello ' + selected.title + '!');
	});
	$scope.addTab = function (title, view) {
		view = view || title + " Content View";
		tabs.push({ title: title, content: view, disabled: false});
	};
	$scope.removeTab = function (tab) {
		var index = tabs.indexOf(tab);
		tabs.splice(index, 1);
	};
});

//Toggles side Navigation bar on and off
app.controller('cToggleNavigation', function($scope, $mdSidenav, $log){
    $scope.toggleLeft = buildToggler('left');
    $scope.toggleRight = buildToggler('right');
	
	$scope.toggleLeft = function () {
		return $mdSidenav('left').toggle();
	};

	$scope.isSidebarOpen = function() {
		return $mdSidenav('left').isOpen();
	};
	
    function buildToggler(componentId) {
      return function() {
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
});

//Side control options Scheduler/Courses
app.controller('SideCtrl', function ($scope, $log, $http) {
    var self = this;
    self.nav = 'course_info';
	
    self.selectedItemChange = function(text) {
      //$log.info('Text changed to ' + text);
    };

    self.searchTextChange   = function(item) {
      //$log.info('Item changed to ' + JSON.stringify(item));
    };

    self.querySearch = function(query) {
      //$log.info('Query: ' + query);

      //$log.info('Courses: ' + self.courses);
      
      var results = query ? self.courses.filter( createFilterFor(query) ) : self.courses,
          deferred;

      //$log.info('Results: ' + JSON.stringify(results));
      return results;
    };
	
    self.setNav = function(page) {
        console.log("nav = " + page);
        self.nav = page;
    };

    self.getNav = function() {
        return self.nav;
    };

    self.searchTree = function(searchString) {
        if ( 0 == (searchString.length % 3)) {
          $('#course_tree').jstree('search', searchString);
        }
    };

    $('#course_tree').on('changed.jstree', function (e, data) {
        var i, j, r = [];
        for (i = 0, j = data.selected.length; i < j; i++) {
            console.log('Pushing: ' + data.instance.get_node(data.selected[i]).text);
            r.push(data.instance.get_node(data.selected[i]).text);
        }
        console.log('Selected: ' + r.join(', '));
    }).jstree({
        'core': {
            'data': function (obj, cb) {
                $.get("/api/tree/courses_v2", function (data) {
                    cb.call(this, data.results);
                });
            }
        },
        "search": {
            "case_insensitive": true,
            "show_only_matches" : true
        },
        "plugins": ["search"]
    });

    $http.get("get_courses").then(function (response) {
        $log.info("loading get_courses");
        self.courses = response.data.results.map(function(item) {
            return {
                value: item.letter.toLowerCase() + ' ' + item.number,
                short_name: item.letter + ' ' + item.number,
                name: item.name
            };
        });
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
});

//Angular Element Directives
app.directive('tabNavigation', function($log) {
	$log.info("tabNavigationFunction");
	return {
		restrict: 'E',
		templateUrl: 'static/html/tabNavigation.html'
	};
});