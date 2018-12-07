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

var app3 = angular.module('app3', [])
app3.controller('AddItmeController', AddItmeController);


//service - a way to share data across AddItmeControlleras
// service only get created when someone inside the controller use it
//AddItmeController.$inject = ["myservice"]

function AddItmeController (myservice) {
  var itemAdd = this

  itemAdd.itemName = "";
  itemAdd.itemNumber = "";

  itemAdd.addItem = function() {
    myservice.addItem(itemAdd.itemName, itemAdd.itemNumber)
    };
  }


app3.service('myservice', myservice)
function myservice ()
{
  var service = this
  var items = []

  service.addItem = function (Name, Number)
  {
    var item = {
      name: Name,
      number: Number
    };
    items.push(item)
  }

  service.getItems = function()
  {
    return items
  }

  service.removeItem = function (index)
  {
    console.log("started");
    items.splice(index, 1);
  }
}

app3.controller('ShowListController', ShowListController);
ShowListController.$inject = ["myservice"]
function ShowListController (myservice)
 {
    var showList = this
    showList.items = myservice.getItems()

    showList.remove_Item = function (index)
    {
      myservice.removeItem(index)
    }
  }



})();
