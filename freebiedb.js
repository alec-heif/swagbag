var mongo = require('mongodb');

var server = new mongo.Server('localhost', 27017, {auto_reconnect: true});
var db = new mongo.Db('freebiedb', server, {safe: true});

// TODO: PAGINATION
db.open(function(err, db) {
    if (! err) {
        console.log("Connected to 'freebiedb' database");
        db.collection('freebies', {safe: true}, function(err, collection) {
            collection.count(function (err, count) {
                if (! err && count === 0) {
                    console.log("The 'freebies' collection is empty. Creating it with sample data...");
                    populateFreebies();
                }
            });
        });
    }    
});

// See: http://expressjs.com/api.html 
// req.params can only contain specific IDs assigned by MongoDB for update and delete. 
// req.body will always be the parameters for search, add, and update.
exports.findAll = function(req, res) {
    console.log('Retrieving all freebies');
    db.collection('freebies', function(err, collection) {
        collection.find().toArray(function(err, items) {
            res.send(items);
        });
    });
};

exports.search = function(req, res) {
    var params = req.body; // {} by default
    db.collection('freebies', function(err, collection) {
        collection.find(params).toArray(function(err, items) {
            res.send(items);
        });
    });
};

exports.addFreebie = function(req, res) {
    var freebie = req.body;
    console.log('Adding freebie: ' + JSON.stringify(freebie));
    db.collection('freebies', function(err, collection) {
        collection.insert(freebie, {safe:true}, function(err, result) {
            if (err) {
                res.send({'error':'An error has occurred'});
            } else {
                console.log('Success: ' + JSON.stringify(result[0]));
                res.send(result[0]);
            }
        });
    });
}

exports.updateFreebie = function(req, res) {
    var id = req.params.id;
    var updates = req.body; // e.g. { category: 'Food' }
    console.log('Updating freebie: ' + id);
    console.log(JSON.stringify(updates));
    db.collection('freebies', function(err, collection) {
        collection.update({'_id': new mongo.BSONPure.ObjectID(id)}, {$set: updates}, 
            {safe: true}, function(err, result) {
                if (err) {
                    console.log('Error updating freebie: ' + err);
                    res.send({'error':'An error has occurred'});
                } else {
                    console.log('' + result + ' document(s) updated');
                    res.send(updates);
            }
        });
    });
}

exports.deleteFreebie = function(req, res) {
    var id = req.params.id;
    console.log('Deleting freebie: ' + id);
    db.collection('freebies', function(err, collection) {
        collection.remove({'_id':new mongo.BSONPure.ObjectID(id)}, {safe:true}, function(err, result) {
            if (err) {
                res.send({'error':'An error has occurred - ' + err});
            } else {
                console.log('' + result + ' document(s) deleted');
                res.send(req.params.id);
            }
        });
    });
}

/*--------------------------------------------------------------------------------------------------------------------*/
// Populate database with sample data -- Only used once: the first time the application is started.
// You'd typically not find this code in a real-life app, since the database would already exist.
var populateFreebies = function() {
    var freebies = [
    {   
        urls: {link: 'http://pantry.twiningsusa.com/', img: 'http://www.mysavings.com/img/link/large/23457.jpg'},
        item: {category: 'Food', type: 'tea'},
        name: 'Twinings Tea',
        brand: 'Twinings'
    },
    {   
        urls: {link: 'http://www.isatoritech.com/freeeatsmartbar/default.aspx', img: 'http://www.mysavings.com/img/link/large/26726.jpg'},
        item: {category: 'Food', type: 'protein bar'}, 
        name: 'iSatori Protein Bar',
        brand: 'iSatori',
        restrictions: 'Printable GNC coupon.'
    }
    ];

    db.collection('freebies', function(err, collection) {
        collection.insert(freebies, {safe: true}, function(err, result) {
            if (err) {
                console.log(err);
            }
        });
    });
};