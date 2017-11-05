// http://www.knockmeout.net/2012/05/using-ko-native-pubsub.html
// http://knockoutjs.com/documentation/fn.html
var messageBus = new ko.subscribable();

var featureRequests = ko.observableArray();

// List feature requests
ko.components.register('list-feature-request', {
    viewModel: function(params) {
        self.featureRequests = params.featureRequests
        self.title = ko.observableArray();
    },
    template: { require: 'text!static/knockout-templates/list-feature-request.html' }
});

// Create feature request
ko.components.register('create-feature-request', {
    viewModel: function(params) {
        self.title = ko.observable();
        self.description = ko.observable();
        self.clients = [
            { id: 0, name: "Client A" },
            { id: 1, name: "Client B" },
            { id: 2, name: "Client C" }
        ];
        self.productAreas = [
            { id: 0, name: "Area A" },
            { id: 1, name: "Area B" },
            { id: 2, name: "Area C" },
            { id: 3, name: "Area D" }
        ];
        self.create = function() {
            messageBus.notifySubscribers({
                id: 0,
                title: self.title(),
                description: self.description()
            }, 'create');
            self.clear();
        };
        self.clear = function() {
            self.title("");
            self.description("");
        }
    },
    template: { require: 'text!static/knockout-templates/create-feature-request.html' }
});

messageBus.subscribe(function(value) {
    featureRequests.push(value);
}, null, "create");

jQuery(function() {
    ko.applyBindings();
});