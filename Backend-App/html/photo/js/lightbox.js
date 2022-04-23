/*
 * blueimp Gallery Demo JS
 * https://github.com/blueimp/Gallery
 *
 * Copyright 2013, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/* global blueimp, $ */

$(function () {
  'use strict'

    // load image
    $.ajax({
      type: "GET",
      url:'http://x2020.top/photolist/',
      dataType: 'json',
      // esponse中，包含了 Access-Control-Allow-Origin 这个header，并且它的值里有我们自己的域名时，浏览器才允许我们拿到它页面的数据进行下一步处理。
      success: function(data){
        var json = eval(data); //数组 
        $.each(data, function(indx, item){

          console.log('<a href="./'+item[0]+ '.jpg" title="徐一恒"><img src=./thumbnails/' + item[0] + '.jpg alt="徐一恒"></a>')
          $("#links").append('<a href="./'+item[0]+ '.jpg" title="徐一恒"><img src=./thumbnails/' + item[0] + '.jpg alt="徐一恒"></a>')
        });
      }
    })


   document.getElementById('links').onclick = function (event) {
    event = event || window.event;

    var target = event.target || event.srcElement,
    link = target.src ? target.parentNode : target,

    options = {index: link, event: event},

    links = this.getElementsByTagName('a');
    console.log(links)
    blueimp.Gallery(links, options);
  };
})



// $(function () {
//   'use strict'

//   $.ajax({
//       type: "GET",
//       url:'http://x2020.top/photolist/',
//       dataType: 'json',
//       // esponse中，包含了 Access-Control-Allow-Origin 这个header，并且它的值里有我们自己的域名时，浏览器才允许我们拿到它页面的数据进行下一步处理。
//       success: function(data){
//         var carouselLinks = []
//         var json = eval(data); //数组 
//         $.each(data, function(indx, item){

//           carouselLinks.push({
//             href: '../' + item[0] + '.jpg',
//             title: ''
//           })          
//         });

//       blueimp.Gallery(carouselLinks, {
//       container: '#blueimp-image-carousel',
//       carousel: true
//       })
        
//       }
//     })
//   })

  // .done(function (result) {
  //     var carouselLinks = []
  //     console.log(result)
  //     $.each(result, function (index, photo) {
  //     baseUrl = photo
  //     console.log(baseUrl)
  //     carouselLinks.push({
  //       href: baseUrl,
  //       title: ''
  //     })
  //   })
    // blueimp.Gallery(carouselLinks, {
    // container: '#blueimp-image-carousel',
    // carousel: true
    // })


  // // Load demo images from flickr:
  // $.ajax({
  //   // Flickr API is SSL only:
  //   // https://code.flickr.net/2014/04/30/flickr-api-going-ssl-only-on-june-27th-2014/
  //   url: 'https://api.flickr.com/services/rest/',
  //   data: {
  //     format: 'json',
  //     method: 'flickr.interestingness.getList',
  //     api_key: '7617adae70159d09ba78cfec73c13be3' // jshint ignore:line
  //   },
  //   dataType: 'jsonp',
  //   jsonp: 'jsoncallback'
  // }).done(function (result) {
  //   var carouselLinks = []
  //   var linksContainer = $('#links')
  //   var baseUrl
  //   // Add the demo images as links with thumbnails to the page:
  //   $.each(result.photos.photo, function (index, photo) {
  //     baseUrl = 'https://farm' + photo.farm + '.static.flickr.com/' +
  //     photo.server + '/' + photo.id + '_' + photo.secret
  //     $('<a/>')
  //       .append($('<img>').prop('src', baseUrl + '_s.jpg'))
  //       .prop('href', baseUrl + '_b.jpg')
  //       .prop('title', photo.title)
  //       .attr('data-gallery', '')
  //       .appendTo(linksContainer)
  //     carouselLinks.push({
  //       href: baseUrl + '_c.jpg',
  //       title: photo.title
  //     })
  //   })
  //   // Initialize the Gallery as image carousel:
  //   blueimp.Gallery(carouselLinks, {
  //     container: '#blueimp-image-carousel',
  //     carousel: true
  //   })
  // })
  // var uInt8Array = new Uint8Array('db/weixin.db');
  // var db = new SQL.Database(uInt8Array);
  // var contents = db.exec("SELECT * FROM photo");
  // var carouselLinks = []
  // carouselLinks.push(
  // {
  //   href:'http://x2020.top/i8kHD2mZmL5H6RyCgG_qllBXA8TccTO2mB8U8ZrLCqRKYnR5YxCEHcIyE8w13s-e.jpg',
  //   title:'test'
  // })
  //   carouselLinks.push(
  // {
  //   href:'http://x2020.top/i8kHD2mZmL5H6RyCgG_qllBXA8TccTO2mB8U8ZrLCqRKYnR5YxCEHcIyE8w13s-e.jpg',
  //   title:'test'
  // })
  // Initialize the Gallery as image carousel:
  // blueimp.Gallery(carouselLinks, {
  //     container: '#blueimp-image-carousel',
  //     carousel: true
  //   })

  // Initialize the Gallery as video carousel:
  // blueimp.Gallery([
  //   {
  //     title: 'Sintel',
  //     href: 'https://archive.org/download/Sintel/sintel-2048-surround_512kb.mp4',
  //     type: 'video/mp4',
  //     poster: 'https://i.imgur.com/MUSw4Zu.jpg'
  //   },
  //   {
  //     title: 'Big Buck Bunny',
  //     href: 'https://upload.wikimedia.org/wikipedia/commons/7/75/' +
  //       'Big_Buck_Bunny_Trailer_400p.ogg',
  //     type: 'video/ogg',
  //     poster: 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/' +
  //       'Big.Buck.Bunny.-.Opening.Screen.png/' +
  //       '800px-Big.Buck.Bunny.-.Opening.Screen.png'
  //   },
  //   {
  //     title: 'Elephants Dream',
  //     href: 'https://upload.wikimedia.org/wikipedia/commons/transcoded/8/83/' +
  //       'Elephants_Dream_%28high_quality%29.ogv/' +
  //       'Elephants_Dream_%28high_quality%29.ogv.360p.webm',
  //     type: 'video/webm',
  //     poster: 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/' +
  //       'Elephants_Dream_s1_proog.jpg/800px-Elephants_Dream_s1_proog.jpg'
  //   },
  //   {
  //     title: 'LES TWINS - An Industry Ahead',
  //     type: 'text/html',
  //     youtube: 'zi4CIXpx7Bg'
  //   },
  //   {
  //     title: 'KN1GHT - Last Moon',
  //     type: 'text/html',
  //     vimeo: '73686146',
  //     poster: 'https://secure-a.vimeocdn.com/ts/448/835/448835699_960.jpg'
  //   }
  // ], {
  //   container: '#blueimp-video-carousel',
  //   carousel: true
  // })
