window.Freebie = Backbone.Model.extend({
  urlRoot: "/freebies",

  idAttribute: "_id",

  initialize: function(){
      console.log('This model has been initialized.');
  }

  defaults: {
    urls: {'link': "", 'img': ""},
    item: {"category" : "", "type" : ""},
    name: "",
    brand: "", 
    _id: ""
  }

});

window.FreebieCollection = Backbone.Collection.extend({

    model: Freebie,

    url: "/freebies"

});

