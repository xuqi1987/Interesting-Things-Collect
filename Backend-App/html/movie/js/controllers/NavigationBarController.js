/**
 * Created by admini on 16-12-16.
 */

app.controller('NavigationController', function($scope,$rootScope, $location,$http,moviedataservice) {
    $scope.init = function(){

    }

    $scope.btn_search = function(name){
        $location.path("/list/search/"+name);
    }
});