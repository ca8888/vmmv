(function () {
'use strict';

var shop1  = [ "milk", "bagmilk", "my_milk", "schoco milk", "chocolate" , "tee"];

var shop2 = [
{
  name: "milk",
  quantity: "2"
},
{
  name: "chocolate",
  quantity: "2"
},
{
  name: "tee",
  quantity: "2"
}
]

var app2 = angular.module('repeatme', [])
app2.controller('lec16', lec16);
lec16.$inject = ["$scope", "$filter"]
function lec16 ($scope) {
  $scope.shop1 = shop1;
  $scope.shop2 = shop2;
  $scope.bummer = "aldp;"
  $scope.add_to_list = function() {
    var new_item = {
      name : $scope.new_item_name,
      quantity : $scope.new_item_quantity
    };
  $scope.shop2.push(new_item);
  }

  // var serched_value = "milk"
  // function exist(value) {
  //   return value.indexOf(serched_value) !== -1;
  // }
  // $scope.resault = $scope.shop1.filter(exsit)
}

app2.controller("lec19", lec19)
lec19.inject = ['lec19']
function lec19 ($scope) {
  $scope.try = "gfgfd";
};


var number_array = [1, 2, 3, 4, 5, 6]

function isBigEnough(value) {
  return value >= 3;
}

var filtered_array = number_array.filter(isBigEnough)
console.log("filtered array :", filtered_array)



})();
