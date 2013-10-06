var express = require('express');
var path = require('path');
var http = require('http');
var freebies = require('./freebiedb');
var swag = require('./swagdb');

var app = express();

app.configure(function () {
    app.set('port', process.env.PORT || 8888);
    app.use(express.logger('dev'));  /* 'default', 'short', 'tiny', 'dev' */
    app.use(express.bodyParser());
    app.use(express.static(path.join(__dirname, 'public')));
});

app.get('/freebies', freebies.findAll);
app.get('/search', freebies.search)
app.post('/freebieDataMiner', freebies.upsertFreebie);
app.get('/bags', swag.findAllNames);
app.get('/bags/:name', swag.findFreebiesByBag); 
app.post('/bags/:name', swag.upsertBag);
app.delete('/bags/:name', swag.deleteBag);


app.listen(app.get('port'));
console.log("Server running on port 8888!!");