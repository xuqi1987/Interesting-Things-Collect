/**
 * Created by xuqi on 16/11/8.
 */
/**
 * Created by xuqi on 16/11/5.
 */

'use strict';

var app= angular.module('movieApp', ['ngResource', 'ngRoute'])
    .config(function($routeProvider){
        $routeProvider.when('/list/:action/:param',{

            templateUrl:'view/MovieList.html',

        });

        $routeProvider.when('/downloaded_list/',{

            templateUrl:'view/DownloadList.html',
        });

        $routeProvider.when('/search_list/:key',{

            templateUrl:'view/MovieList.html',
        });

        $routeProvider.when('/player/:name',{

            templateUrl:'view/Player.html',
        });


        $routeProvider.when('/movies/year/:year',{

            templateUrl:'view/MovieList.html',
        });







        $routeProvider.otherwise({redirectTo:'/list/:action/:num'});

        console.log('App called.');
    });