(function () {
'use strict';

var app = angular.module('tempSystem', []);

app.controller('tempReading', function ($scope) {
  $scope.temperature = "0";
  $scope.required_heating = "1";

  $scope.publish = function (){
    console.log("inside publish");
    var my_temperature = calculate_stuff($scope.temperature)
    $scope.required_heating = my_temperature;
  };

  function calculate_stuff(string){
    var answer = 0;
    answer = parseInt(string) + 2;
    console.log(answer);
    return answer
  };
});

// app.controller('DIC',["$scope", "$filter", DIC]); //second option!
app.controller('DIC', DIC);
DIC.$inject = ["$scope", "$filter"]
 function DIC ($scope, $filter, $injector) {
  $scope.name = "alon"
  $scope.upper = function () {
    console.log("inside upper");
    var upCase = $filter('uppercase');
    $scope.name = upCase($scope.name)
  };
};

app.controller('lec11', lec11);
lec11.$inject = ["$scope", "$filter"]
 function lec11 ($scope, $filter) {
   $scope.state = "alon2"
   $scope.myfun = function () {
     var msg = "this is a new message"
     var output = $filter('uppercase') (msg)
    return (output + "\n" + "this is a new message")
  };

  $scope.button_call = function () {
    $scope.state = "alon1"

  };
};

app.controller('lec14', lec14);
lec14.$inject = ["$scope", "$filter"]
 function lec14 ($scope, $filter) {
   $scope.counter = 0
   $scope.show  = function () {
     console.log($scope) //look the number of watcher
   };
   $scope.up_counter = function () {
     $scope.counter++;
   };
   // digest cycle only being triger if the function is angulare
   //start with $ if not we must use apply for apply for digest to run
   $scope.delay_counter = function () {
     setTimeout(function () {
       $scope.$apply(function (){
         $scope.counter++;
       })
     }, 2000)
   };
  };

  app.controller('lec17', lec17);
  lec14.$inject = ["$scope", "$filter"]
   function lec17 ($scope, $filter) {
     $scope.counter = 0
     $scope.show  = function () {
       console.log($scope) //look the number of watcher
     };
     $scope.up_counter = function () {
       $scope.counter++;
     };
     // digest cycle only being triger if the function is angulare
     //start with $ if not we must use apply for apply for digest to run
     $scope.delay_counter = function () {
       setTimeout(function () {
         $scope.$apply(function (){
           $scope.counter++;
         })
       }, 2000)
     };
    };



})();

//MINIFICATION - process to minimize the code size.
