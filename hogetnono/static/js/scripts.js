/*!
* Start Bootstrap - Blog Post v5.0.2 (https://startbootstrap.com/template/blog-post)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-blog-post/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

var mapContainer = document.getElementById('map'), // 지도를 표시할 div
    mapOption = {
        center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨
    };

var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

// 주소로 좌표를 검색합니다
var geocoder = new kakao.maps.services.Geocoder();



/*
for (var i = 0; i < aptinfos.length; i ++){
    alert(aptinfos[])
}*/

geocoder.addressSearch('서울 서초구 서초대로46길 42', function(result, status) {
    // 정상적으로 검색이 완료됐으면
     if (status === kakao.maps.services.Status.OK) {
        coords = new kakao.maps.LatLng(result[0].y, result[0].x);
        //alert(coords);
     }
});

/*
// 마커를 표시할 위치와 내용을 가지고 있는 객체 배열입니다
var positions = [
    {
        content: '<div>아파트이름1 <br/> 주소</div>',
        latlng: new kakao.maps.LatLng(33.450705, 126.570677)
    },
    {
        content: '<div>아파트이름2 <br/> 주소</div>',
        latlng: new kakao.maps.LatLng(33.450936, 126.569477)
    },
    {
        content: '<div>아파트이름3 <br/> 주소</div>',
        latlng: new kakao.maps.LatLng(33.450879, 126.569940)
    },
    {
        content: '<div>아파트이름4 <br/> 주소</div>',
        latlng: new kakao.maps.LatLng(33.451393, 126.570738)
    }
];

for (var i = 0; i < positions.length; i ++) {
    // 마커를 생성합니다
    var marker = new kakao.maps.Marker({
        map: map, // 마커를 표시할 지도
        position: positions[i].latlng // 마커의 위치
    });
}
*/