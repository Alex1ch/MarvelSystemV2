var MasterModel = angular.module('MasterModel',[]);

MasterModel.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

MasterModel.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});


MasterModel.controller('MasterCtrl',function ($scope, $http,$location) {
    //console.log($location.absUrl().split('?')[0].split('/')[4]);

    var GetShort=function(str,len){
        if(str.length>len)
            return str.slice(0,len)+'...';
        else
            return str;
    };

    $scope.CheckMaster=function () {
        var url_chunk=$location.absUrl().split('?')[0].split('/')[3];
        if(url_chunk=='master')return true;
        return false;
    };

    var getComics= function () {
        if($location.absUrl().split('?')[0].split('/')[3]=='master'){
            $http({
                method: 'Get',
                headers: {
                    'Content-Type': undefined
                },
                url: '/getMasterComics/',
                //data:$scope.formModel,
                //transformRequest: angular.identity
            }).then(function (response) {
                $scope.Comics = angular.fromJson(response.data).results;
                console.log($scope.Comics)

                for (var i = 0; i < $scope.Comics.length; i++) {
                    $scope.Comics[i].description = GetShort($scope.Comics[i].description, 200);
                    console.log($scope.Comics[i].description)
                }

            });

        }else {


            $http({
                method: 'Get',
                headers: {
                    'Content-Type': undefined
                },
                url: '/getUserComics/' + $location.absUrl().split('?')[0].split('/')[4],
                //data:$scope.formModel,
                //transformRequest: angular.identity
            }).then(function (response) {
                $scope.Comics = angular.fromJson(response.data).results;
                console.log($scope.Comics)

                for (var i = 0; i < $scope.Comics.length; i++) {
                    $scope.Comics[i].description = GetShort($scope.Comics[i].description, 200);
                    console.log($scope.Comics[i].description)
                }

            });
        }
    };

    $scope.delete=function (id) {
         $http({
            method: 'Get',
            headers: {
               'Content-Type': undefined
            },
            url: '/delete/'+id})
             .then(function (response){
            getComics();
        })
    }

    getComics();
});
