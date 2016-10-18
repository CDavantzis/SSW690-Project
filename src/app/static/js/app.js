
//you can inherit application modules here like ngMaterial, custom
var app = angular.module('scheduler', ['ngMaterial']);

app.controller('AppCtrl', function($scope, $mdSidenav, $log){
  $scope.dp = new DayPilot.Calendar("dp");
  $scope.dp.viewType = "Week";
  $scope.dp.theme = 'calendar_g';
  $scope.dp.headerDateFormat = 'dddd';
  $scope.dp.init();

  $scope.toggleLeft = function () {
      return $mdSidenav('left').toggle();
  };

  $scope.isSidebarOpen = function() {
      return $mdSidenav('left').isOpen();
  };
});

app.controller('SideCtrl', function ($scope, $mdSidenav, $log, $http) {
    var self = this;

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

    $scope.close = function () {
        // Component lookup should always be available since we are not using `ng-if`
        $mdSidenav('left').close()
                .then(function () {
                    $log.debug("close LEFT is done");
                });
    };

    self.searchTree = function(searchString) {
        console.log("test:" + searchString);
        $('#tree').jstree('search', searchString);
    };

    $('#tree').on('changed.jstree', function (e, data) {
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
