var Freebie = Backbone.Model.extend({
  initialize: function(){
      console.log('This model has been initialized.');
  }

  defaults: {
    urls: {'', ''},
    item: {"category" : "", "type" : ""},
    name: "",
    brand: "", 
    _id: ""
  }

});

// We can then create our own concrete instance of a (Todo) model
// with no values at all:
var freebie1 = new Freebie();
var freebie1Attributes = freebie1.toJSON();
// Following logs: {}
console.log(JSON.stringify(todo1));

// or with some arbitrary data:
var todo2 = new Todo({
  title: 'Check the attributes of both model instances in the console.',
  completed: true
});

// Following logs: {"title":"Check the attributes of both model instances in the console.","completed":true}
console.log(JSON.stringify(todo2));

var todo3 = new Todo({
  title: 'This todo is done, so take no action on this one.',
  completed: true
});

// Following logs: {"title":"This todo is done, so take no action on this one.","completed":true} 
console.log(JSON.stringify(todo3));