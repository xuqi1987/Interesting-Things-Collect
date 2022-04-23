/**
 * Created by xuqi on 16/12/29.
 */
app.controller('PlayerController', function($scope, $http,$routeParams,moviedataservice) {

    $scope.initPlayer = function() {

        url = 'http://x2020-movie.oss-cn-shanghai.aliyuncs.com/'

        // Initialize the Gallery as video carousel:
        blueimp.Gallery([
            {
                title: 'Sintel',
                href: url + $routeParams.name,
                type: 'video/mp4',
                poster: 'https://i.imgur.com/MUSw4Zu.jpg'
            }
        ], {
            container: '#blueimp-video-carousel',
            carousel: true
        })
    }

});