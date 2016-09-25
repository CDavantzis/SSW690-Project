

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

app.controller('SideCtrl', function ($scope, $mdSidenav, $log) {
    $scope.close = function () {
      // Component lookup should always be available since we are not using `ng-if`
      $mdSidenav('left').close()
        .then(function () {
          $log.debug("close LEFT is done");
        });
   	};
});