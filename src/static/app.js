var featureRequests = ko.observableArray();
var clients = ko.observableArray();
var productAreas = ko.observableArray();

function pageViewModel() {
    var self = this;
    // http://www.knockmeout.net/2012/05/using-ko-native-pubsub.html
    // http://knockoutjs.com/documentation/fn.html
    self.messageBus = new ko.subscribable();
    self.messageBus.subscribe(function(data) {
        jQuery.post({
            url: 'create_feature_request',
            data: data,
            success: function(serverResponseData) {
                if (serverResponseData.status == 'ok') {
                    fetch_feature_requests();
                    self.messageBus.notifySubscribers({}, "clear");
                } else {
                    alert(serverResponseData.status);
                }
            }
        }).fail(function() {
            alert("Error creating feature request. You might be passing invalid input.");
        })
    }, {}, "create");
}
var vm = new pageViewModel();
jQuery(function() {
    ko.applyBindings(vm);
    jQuery.getJSON('fetch_clients', function(data) {
        ko.utils.arrayPushAll(clients, data);
    });
    fetch_feature_requests();
    jQuery.getJSON('fetch_product_areas', function(data) {
        ko.utils.arrayPushAll(productAreas, data);
    });
});
ko.components.register('list-feature-request', {
    viewModel: function(params) {
        var self = this;
        self.featureRequests = params.featureRequests
    },
    template: { require: 'text!static/knockout-templates/list-feature-request.html' }
});
ko.components.register('create-feature-request', {
    viewModel: function(params) {
        var self = this;
        self.title = ko.observable();
        self.description = ko.observable();
        self.targetDate = ko.observable();
        self.priority = ko.observable();
        self.selectedClient = ko.observable();
        self.selectedProductArea = ko.observable();
        self.clients = params.clients;
        self.productAreas = params.productAreas;
        self.messageBus = params.messageBus;
        self.create = function() {
            data = {
                title: self.title(),
                description: self.description(),
                targetDate: self.targetDate(),
                priority: self.priority(),
                clientId: self.selectedClient(),
                productAreaId: self.selectedProductArea()
            };
            self.messageBus.notifySubscribers(data, 'create');
        };
        // These are the equivalent of functions, using the message bus
        self.messageBus.subscribe(function(data) {
            self.title("");
            self.description("");
            self.targetDate("");
            self.priority("");
        }, {}, "clear");
    },
    template: { require: 'text!static/knockout-templates/create-feature-request.html' }
});

function fetch_feature_requests() {
    featureRequests.removeAll();
    jQuery.getJSON('fetch_feature_requests', function(data) {
        ko.utils.arrayPushAll(featureRequests, data);
    });
}