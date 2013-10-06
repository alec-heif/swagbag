var mongo = require('mongodb');

var server = new mongo.Server('localhost', 27017, {auto_reconnect: true});
var db = new mongo.Db('swagdb', server, {safe: true});

// TODO: NO EMPTY BAGS OR DUPLICATE NAMES
// TODO: Remove hardcode of demo, get username from request
db.open(function(err, db) {
    if (! err) {
        console.log("Connected to 'swagdb' database");
        db.collection('demo', {safe: true}, function(err, collection) {
            collection.count(function (err, count) {
                if (! err && count === 0) {
                    console.log("The 'demo' collection is empty. Creating it with sample data...");
                    populateDemo();
                }
            });
        });
    }    
});

exports.findAllNames = function(req, res) {
    db.collection('demo', function(err, collection) {
        collection.find({}, {'name': 1, '_id': 0}).toArray(function(err, items) {
            res.send(items.map(function(doc) {
                return doc['name'];
            }));
        });
    });
};

exports.findFreebiesByBag = function(req, res) {
    var name = req.params.name;
    db.collection('demo', function(err, collection) {
        collection.findOne({'name': name}, {'bag': 1, '_id': 0}, function(err, doc) {
            if (doc !== null) {
                res.send(doc['bag']);
            } else {
                res.send({'error': 'No bag with that name found'});
            }
        });
    });    
};

exports.upsertBag = function(req, res) {
    var name = req.params.name;
    var bag = req.body;
    console.log('Upserting bag: ' + name);
    console.log(JSON.stringify(bag));
    db.collection('demo', function(err, collection) {
        collection.update({'name': name}, bag, {upsert: true, safe: true}, function(err, result) {
            if (err) {
                console.log('Error upserting freebie: ' + err);
                res.send({'error':'An error has occurred'});
            } else {
                res.send(bag);
            }
        });
    });
}

exports.deleteBag = function(req, res) {
    var name = req.params.name;
    console.log('Deleting bag: ' + name);
    db.collection('demo', function(err, collection) {
        collection.remove({'name': name}, {safe: true}, function(err, result) {
            if (err) {
                res.send({'error':'An error has occurred - ' + err});
            } else {
                console.log('' + result + ' document(s) deleted');
                res.send({'success': name});
            }
        });
    });
}

/*--------------------------------------------------------------------------------------------------------------------*/
// Populate database with demo data
var populateDemo = function() {
    var demoData = [
    { name: 'NOMMMMM', bag: [   
    { urls: {link: 'http://pantry.twiningsusa.com/', img: 'http://www.mysavings.com/img/link/large/23457.jpg'},
      item: {category: 'Food', type: 'tea'}, name: 'Twinings Tea', brand: 'Twinings' },
    { urls: {link: 'http://www.isatoritech.com/freeeatsmartbar/default.aspx', img: 'http://www.mysavings.com/img/link/large/26726.jpg'},
      item: {category: 'Food', type: 'protein bar'}, name: 'iSatori Protein Bar', brand: 'iSatori',
      restrictions: 'Printable GNC coupon.' } 
    ]},

    { name: 'Back to School', bag: [ 
    { urls: {link: 'http://pantry.twiningsusa.com/', img: 'http://www.mysavings.com/img/link/large/23457.jpg'},
      item: {category: 'Food', type: 'tea'}, name: 'Twinings Tea', brand: 'Twinings' } 
    ]}];
    db.collection('demo', function(err, collection) {
        collection.insert(demoData, {safe: true}, function(err, result) {
            if (err) {
                console.log(err);
            } 
        });
    });
};