/**
 * Created by admini on 16-12-16.
 */

app.controller('MovieListController', function($scope, $http,$routeParams,moviedataservice) {
    console.log("MovieListController")
    $scope.links = []

    $scope.initList  = function(){
        if ($routeParams.action == "new_update"){
            moviedataservice.req_new_update_list().then(function(data) {
                $scope.list_datas = data
            },function(data) {
                $scope.list_datas = []
            });
        }
        else if ($routeParams.action == "year"){
            moviedataservice.req_year_list($routeParams.param).then(function(data) {
                $scope.list_datas = data
            },function(data) {
                $scope.list_datas = []
            });
        }
        else if ($routeParams.action == "cate"){
            moviedataservice.req_cate_list($routeParams.param).then(function(data) {
                $scope.list_datas = data
            },function(data) {
                $scope.list_datas = []
            });
        }
        else if ($routeParams.action == "search") {
            console.log("ssss")
            moviedataservice.req_search_list($routeParams.param).then(function(data) {
                $scope.list_datas = data
            },function(data) {
                $scope.list_datas = []
            });
        }
    };

    $scope.copylink = function(url,index) {

    };


    $scope.download = function(url,linkid){
        moviedataservice.req_start_download(linkid).then(function(data){

        },function(data) {

        });
    };

    $scope.play = function(url,linkid) {
        console.log(url)
    };

    $scope.load_detail_info = function(movie,index,html_text) {
        // set info to html
        $('#detail_info'+index).html(html_text)
        // load link
        moviedataservice.req_links(movie).then(function(data) {
            $scope.download_links =data
        },function(data) {
            console.log(data)
        });


        new Clipboard('#btn_cpylink_'+index, {
            text: function() {
                return url;
            }
        });
    };


    $scope.getfilename = function(path)
    {
        var pos1 = path.lastIndexOf('/');
        var pos2 = path.lastIndexOf('\\');
        var pos  = Math.max(pos1, pos2)
        if( pos<0 )
            return path;
        else
            return path.substring(pos+1);
    }

    $scope.loadimage = function(index,url) {

        //loading参数
        var opts = {
            lines: 12 // The number of lines to draw
            , length: 6 // The length of each line
            , width: 6 // The line thickness
            , radius: 10 // The radius of the inner circle
            , scale: 1 // Scales overall size of the spinner
            , corners: 1 // Corner roundness (0..1)
            , color: '#333' // #rgb or #rrggbb or array of colors
            , opacity: 0.25 // Opacity of the lines
            , rotate: 0 // The rotation offset
            , direction: 1 // 1: clockwise, -1: counterclockwise
            , speed: 1 // Rounds per second
            , trail: 48 // Afterglow percentage
            , fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
            , zIndex: 99999 // The z-index (defaults to 2000000000)
            , className: 'spinner' // The CSS class to assign to the spinner
            , top: '50%' // Top position relative to parent
            , right: '50%' // Left position relative to parent
            , shadow: false // Whether to render a shadow
            , hwaccel: false // Whether to use hardware acceleration
            , position: 'absolute' // Element positioning
        };

        var target = $("#image"+index)

        var spinner = new Spinner(opts).spin(target);

        var surl=url + '?x-oss-process=image/resize,m_fill,h_370,w_250';

        function imgLoadAsync(url){
            return new Promise(function(resolve,reject){
                var img=new Image();
                img.onload=function(){
                    resolve(img);
                }
                img.onerror=function(){
                    img.src = "http://x2020-movie.oss-cn-shanghai.aliyuncs.com/NotFind.jpg?x-oss-process=image/resize,m_pad,h_370,w_250,color_ffffff"
                    reject(img);
                }
                img.src=url;


            });
        }

        imgLoadAsync(surl).then(function(data){
            spinner.stop();
            $("#image"+index).append(data);
        },function(data) {
            $("#image"+index).append(data);
        })
    };


});
