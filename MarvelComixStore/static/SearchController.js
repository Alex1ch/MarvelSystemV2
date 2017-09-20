var SearchModel = angular.module("SearchModel",['angular-md5']);

SearchModel.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

SearchModel.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

SearchModel.controller('SearchCtrl',function ($scope, $http, md5) {
    $scope.formModel = new FormData();

    var publickey="1d5365b38cdcd75799f1f05327d55d56"
    var privatekey="55be91fef4d4316e3df0009f00acf6f1e6cb16b3"

    $scope.Comics=[];

    $scope.keywords="";
    $scope.searchkey="";

    $scope.tags=[];

    $scope.added=[];

    $scope.pagenum=1;

    $scope.pages = [];

    $scope.thispage=1;

    $scope.offset=0;

    $scope.check_comics=function(object){
        for(i=0;i<$scope.added.length;i++) {
            if (object.ean.toString() == $scope.added[i]) {
                return false;
            }
        }
        return true;
    };

    $scope.ChangePage=function (page) {
        var DateVar=new Date();

        $scope.searchkey=$scope.keywords;

        $scope.offset=20*($scope.thispage-1);

        $http({
            method: 'Get',
            url: 'https://gateway.marvel.com:443/v1/public/comics?titleStartsWith='+$scope.keywords+'&offset='+$scope.offset+'&apikey='+publickey+'&hash='+md5.createHash(Math.floor(DateVar.getTime()/1000)+privatekey+publickey)+'&ts='+Math.floor(DateVar.getTime()/1000),
            headers: {
               'Content-Type': undefined
            },
            //data:$scope.formModel,
            //transformRequest: angular.identity
        }).then(function (response) {
            var response_obj=angular.fromJson(response.data);
            $scope.Comics = response_obj.data.results;
            console.log(response_obj);
            $scope.thispage=page;
        });
    }

    $scope.Reset=function () {
        $scope.keywords="";
        $scope.selectedItem=$scope.items[0];
    };

    $scope.OnTagsClick=function (tag) {
        $scope.keywords=$scope.tags[tag-1].name;
        $scope.OnSubmit();
    };

    var getAdded=function () {

        $http({method:'GET',url:'/get_added/'}).then(function (response) {
            $scope.added=response.data.toString().split('\n');
            console.log($scope.added)
        });
    };

    $scope.AddItem=function (ean) {
        $http( {method: 'GET', url: 'add/'+ean.toString()}).then(function (response) {
            getAdded();
        })
    };


    $scope.DeleteItem=function (ean) {
        $http( {method: 'GET', url: 'delete/'+ean.toString()}).then(function (response) {
            getAdded();
        })
    };
    
    $scope.GetShort=function(str,len){
        if(str.length>len)
            return str.slice(0,len)+'...';
        else
            return str;
    };

    $scope.GetDate= function (str) {
        var date=new Date(str);
        date.getDate();
        return date.getUTCDate()+"."+date.getUTCMonth()+"."+date.getUTCFullYear();
    };
    
    $scope.OnSubmit=function () {
        var DateVar=new Date();

        $scope.offset=0;

        $scope.searchkey=$scope.keywords;

        $http({
            method: 'Get',
            url: 'https://gateway.marvel.com:443/v1/public/comics?titleStartsWith='+$scope.keywords+'&offset='+$scope.offset+'&apikey='+publickey+'&hash='+md5.createHash(Math.floor(DateVar.getTime()/1000)+privatekey+publickey)+'&ts='+Math.floor(DateVar.getTime()/1000),
            headers: {
               'Content-Type': undefined
            },
            //data:$scope.formModel,
            //transformRequest: angular.identity
        }).then(function (response) {
            var response_obj=angular.fromJson(response.data);
            $scope.Comics = response_obj.data.results;
            console.log(response_obj);
            if(response_obj.data.total/20%1==0)
                $scope.pagenum=Math.floor(response_obj.data.total/20);
            else
                $scope.pagenum=Math.floor(response_obj.data.total/20)+1;
            console.log($scope.pagenum)
            $scope.pages=[];
            for(i=0;i<$scope.pagenum;i++){
                $scope.pages.push(i+1);
            }
            $scope.thispage=1;
        });
        $scope.formModel=new FormData();
    }

});

