// http://www.knockmeout.net/2012/05/using-ko-native-pubsub.html
// http://knockoutjs.com/documentation/fn.html
var messageBus = new ko.subscribable();

var featureRequests = ko.observableArray();
var clients = ko.observableArray();
var productAreas = ko.observableArray();

// List feature requests
ko.components.register('list-feature-request', {
    viewModel: function(params) {
        self.featureRequests = params.featureRequests
    },
    template: { require: 'text!static/knockout-templates/list-feature-request.html' }
});

// Create feature request
ko.components.register('create-feature-request', {
    viewModel: function(params) {
        self.title = ko.observable();
        self.description = ko.observable();
        self.targetDate = ko.observable();
        self.priority = ko.observable();
        self.selectedClient = ko.observable();
        self.selectedProductArea = ko.observable();

        self.clients = params.clients;
        self.productAreas = params.productAreas;
        self.create = function() {
            messageBus.notifySubscribers({
                title: self.title(),
                description: self.description(),
                targetDate: self.targetDate(),
                priority: self.priority(),
                clientId: self.selectedClient(),
                productAreaId: self.selectedProductArea()
            }, 'create');
            self.clear();
        };
        self.clear = function() {
            self.title("");
            self.description("");
            self.targetDate("");
            self.priority("");
        }
    },
    template: { require: 'text!static/knockout-templates/create-feature-request.html' }
});

messageBus.subscribe(function(formData) {
    jQuery.post({
        url: 'create_feature_request',
        data: formData,
        success: function(serverResponseData) {
            if(serverResponseData.status == 'ok') {
                fetch_feature_requests();
            } else {
                // Handle error here
            }
        }
    });
}, null, "create");

jQuery(function() {
    ko.applyBindings();

    jQuery.getJSON('fetch_clients', function(data) {
        ko.utils.arrayPushAll(clients, data);
    });

    fetch_feature_requests();

    jQuery.getJSON('fetch_product_areas', function(data) {
        ko.utils.arrayPushAll(productAreas, data);
    });
});

function fetch_feature_requests() {
    featureRequests.removeAll();
    jQuery.getJSON('fetch_feature_requests', function(data) {
        ko.utils.arrayPushAll(featureRequests, data);
    });
}