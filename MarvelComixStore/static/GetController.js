var GetModel = angular.module("GetModel",['angular-md5']);

GetModel.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

GetModel.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});


GetModel.controller('GetCtrl',function ($scope, $http, md5, $location) {
    console.log($location.absUrl().split('?')[0].split('/')[4]);

    var publickey="1d5365b38cdcd75799f1f05327d55d56"
    var privatekey="55be91fef4d4316e3df0009f00acf6f1e6cb16b3"

    var DateVar=new Date();

    $http({
        method: 'Get',
        url: 'https://gateway.marvel.com:443/v1/public/comics?id='+$location.absUrl().split('?')[0].split('/')[4]+'&apikey='+publickey+'&hash='+md5.createHash(Math.floor(DateVar.getTime()/1000)+privatekey+publickey)+'&ts='+Math.floor(DateVar.getTime()/1000),
        headers: {
           'Content-Type': undefined
        },
        //data:$scope.formModel,
        //transformRequest: angular.identity
    }).then(function (response) {
        $scope.Comic = angular.fromJson(response.data).data.results;
        console.log($scope.Comic);
    });

});