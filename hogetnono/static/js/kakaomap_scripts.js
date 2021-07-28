// 초기 지도 셋팅
var mapContainer = document.getElementById('map'), // 지도를 표시할 div
    mapOption = {
        center: new kakao.maps.LatLng(37.56648949810302, 126.97795671261468), // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨
    };

var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

var imageSrc = "/static/assets/home-location-marker.png"; // 마커 이미지 경로
var imageSize = new kakao.maps.Size(35, 35); // 마커 이미지 크기
var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); // 마커 이미지를 생성

// 머커 생성 및 이벤트 등록
for(var i=0; i<aptinfos.length; i++){
    var coords = new kakao.maps.LatLng(aptinfos[i]['gps']['y'], aptinfos[i]['gps']['x']); // kakomap에서 사용하는 위,경도 객체로 변환
    var marker = new kakao.maps.Marker({ // 마커를 생성
        map: map, // 마커를 표시할 지도
        position: coords, // 마커를 표시할 위치
        title : aptinfos[i]['name'], // 마커의 타이틀, 마커에 마우스를 올리면 타이틀이 표시됩니다
        image : markerImage, // 마커 이미지
        clickable: true
    });
    bounds[aptinfos[i]['location_code']].extend(coords); // 지역에 따라 표시 영역 확장

    // 마커 객체에 사용자 이벤트를 등록한다.
    kakao.maps.event.addListener(marker, 'click', makeOutListener(aptinfos[i]['sn']));
};

// 이벤트 발생시 실행할 함수
function makeOutListener(data) {
    return function() {
        aptClick(data);
    };
}

// 지역code로 검색하여 지도 이동 트리거를 발생
function setBounds(code) {
    map.setBounds(bounds[code]);
}

function moveBounds(sn) {
    for(var i=0; i<aptinfos.length; i++){
        if(aptinfos[i]['sn'] === sn){
            var movebound = new kakao.maps.LatLngBounds()
            movebound.extend(new kakao.maps.LatLng(aptinfos[i]['gps']['y'], aptinfos[i]['gps']['x']));
            map.setBounds(movebound);
        }
    }
}
