(function () {
'use strict';
// !!!!!!!!!!!!!!!!!!!!! proptypel ineritance
// var parent = {
//   value : "parent_value",
//   credit:{
//     bank : "n25"
//   },
//   walk : function() {
//     consloe.log("walking")
//   }
// };
//
// var child = Object.create(parent);
// console.log("child value", child.value)
// console.log("parent value", child.value)
// console.log("parent credit", parent.credit.bank)
// console.log("child credit", child.credit.bank)
//
// child.value = "child_value"
// child.credit.bank = "dkb"
//
//
// console.log("child value", child.value)
// console.log("parent value", child.value)
// console.log("parent credit", parent.credit.bank)
// console.log("child credit", child.credit.bank)
//
// console.log(parent)
// console.log(child)
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


//************************** impotant***************
// $scope.a = "a"  //local variable
// $scope.b = "b"  //local variable
// $scope.obj.a = "a"  //ponting to the same obj!
// $scope.obj.b = "b" //ponting to the same obj!!!
//
// ng-controllert = controller1 as ctr1
// now what haapend is that the argument "this" is $scope1!!!
// ng-controllert = controller2 as ctr2
// now what haapend is that the argument "this" is $scope2!!!
// ctr1.value independet ctr2.value!
//*********************************************************


  console.log("started");
  var my_app = angular.module('my_app', [])

  my_app.controller('parent', parent);
  parent.$inject = ["$scope"]
  function parent ($scope) {
    $scope.parentValue = 5
    $scope.pc = this
    $scope.pc.parentValue = 2
    console.log("parent", $scope);
  };

  my_app.controller("child", child)
  child.$inject = ["$scope"]
  function child ($scope) {
    // $scope.parentValue = 1
    // $scope.pc = this
    // $scope.pc.parentValue = 2

    console.log("$scope pv", $scope.parentValue);
    console.log("---------------");
    $scope.parentValue = 6
    console.log("$scope pv", $scope.parentValue);
    console.log("child", $scope);

    $scope.pc.parentValue = 56
    console.log("$scope pv", $scope.parentValue);
    console.log("---------------");
    console.log("$scope pv", $scope.parentValue);
    console.log("child", $scope);


  };

})();
