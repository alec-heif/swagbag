var AppRouter = Backbone.Router.extend({

    routes: {
        ""                  : "home",
        "freebies"	            : "list",
        "freebies/page?=:page"	: "list"
    },

    initialize: function () {
        this.headerView = new HeaderView();
        $('.header').html(this.headerView.el);
    },

    home: function (id) {
        if (!this.homeView) {
            this.homeView = new HomeView();
        }
        $('#content').html(this.homeView.el);
        this.headerView.selectMenuItem('home-menu');
    },

	list: function(page) {
        var p = page ? parseInt(page, 10) : 1;
        var freebieList = new WineCollection();
        freebieList.fetch({success: function(){
            $("#content").html(new FreebieListView({model: freebieList, page: p}).el);
        }});
        this.headerView.selectMenuItem('home-menu');
    }
});

utils.loadTemplate(['HomeView', 'HeaderView'], function() {
    app = new AppRouter();
    Backbone.history.start();
});