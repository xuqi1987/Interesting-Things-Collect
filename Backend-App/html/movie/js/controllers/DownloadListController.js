/**
 * Created by xuqi on 16/12/27.
 */
app.controller('DownloadListController', function($scope,$timeout, $http,$routeParams,moviedataservice) {
    $scope.links = []

    $scope.initList = function(){
        console.log('DownloadListController initlist')

        var update_status = function(){

            moviedataservice.req_downloaded_list().then(function(data) {
                $scope.list_datas = data
                console.log(data)

            },function(data) {
                $scope.list_datas = []
            });

        }


        update_status();

        var updateClock=function(){
            $timeout(function(){
                update_status();
                updateClock();
            },5000);
        };
        updateClock();
    }

    $scope.getstatus = function(status) {
        if(status == 'error')
            return 'danger'
        else if (status == '')
            return 'success'
        else if (status == '')
            return 'info'
    }

    // gets the progress in percentages
    $scope.getProgress = function(d) {
        var percentage = 0
        if (d.verifiedLength)
            percentage = (d.verifiedLength / d.totalLength) * 100 || 0;
        else
            percentage = (d.completedLength / d.totalLength) * 100 || 0;
        percentage = percentage.toFixed(2);
        if(!percentage) percentage = 0;

        return percentage;
    };

    $scope.pause = function(d) {


    };
    $scope.resume = function(d) {

    };
    $scope.restart = function(d) {

    };

    $scope.remove = function(d) {

    };

    $scope.hasStatus = function hasStatus(d, status) {
        return d.status == status;
    };

    $scope.getEta = function(d) {
        return (d.totalLength-d.completedLength) / d.downloadSpeed;
    }


});