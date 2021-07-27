/*!
* Start Bootstrap - Blog Post v5.0.2 (https://startbootstrap.com/template/blog-post)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-blog-post/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

// Tab 활성화 변경 처리
$('#aptSearchResult_tab').click(function(){
    aptSearchResult_tab();
})

function aptSearchResult_tab(){
    $('#aptSearchResult_div').show();
    $('#aptInfo_div').hide();
}

$('#aptInfo_tab').click(function(){
    aptInfo_tab();
})

function aptInfo_tab(){
    $('#aptSearchResult_div').hide();
    $('#aptInfo_div').show();
}

// 아파트 검색 AJAX 처리
$('#apt_search_but').click(function(){      // id를 찾아서 클릭 함수 처리
    aptSearchResult();
    aptSearchResult_tab(); // 탭을 검색 결과로 변경
})

$('#apt_search_txt').keydown(function(e) {  // 키입력 처리
    if (e.keyCode == 13) {
        aptSearchResult();
        aptSearchResult_tab(); // 탭을 검색 결과로 변경
    }
})

function aptSearchResult(){
    var apt_search = $('#apt_search_txt').val();   // id에 해당하는 val 값 가져오기
    var postdata = {'apt_search':apt_search} // 데이터를 서버로 전달시 JSON 방식으로 전달

    $('#aptSearchResult_title').text("'"+ apt_search + "' 아파트 검색 결과"); // title 상단 내용 변경
    $('#apt_search_txt').val(''); //검색창 비우기

    $.ajax({
        type: 'POST',
        url: '/index/aptsearch',            // '{{url_for("ajax")}}' 이렇게 요청하면 함수에 대한 URL을 찾아준다.
        data: JSON.stringify(postdata),     // 전송시에 JSON타입으로 전송
        contentType: "application/json",    // 보내는 데이터 타입
        success: function(data){
            $('#aptSearchResult_tbody').remove();
            var htmlCode = '';
            htmlCode += '<tbody id="aptSearchResult_tbody">';
            if(data.aptinfos.length){
                for(var i = 0; i < data.aptinfos.length; i ++) {
                    var sn = data.aptinfos[i]['sn']
                    var name = data.aptinfos[i]['name']
                    sn = "'" + sn + "'"
                    htmlCode += '<tr><td onclick="aptClick('+ sn +')">' + name + '</td></tr>';
                }
            }else{
                htmlCode += '<tr><td>검색 결과가 없습니다.</td></tr>';
            }
            htmlCode += '<tbody>';
            $('#aptSearchResult_table').append(htmlCode);
        },
        error: function(request, status, error){
            alert('ajax 통신 실패')
            alert(error);
        }
    })
}

function aptClick(sn){
    aptInfo_tab();
    var postdata = {'sn':sn} // 데이터를 서버로 전달시 JSON 방식으로 전달
    $.ajax({
        type: 'POST',
        url: '/index/showAptInfo',
        data: JSON.stringify(postdata),
        contentType: "application/json",
        success: function(data){
            $('#aptInfo_tab').text("'"+ data.aptinfo['name'] + "' 아파트"); // 상단탭 이름 변경
            $('#aptInfo_title').text("'"+ data.aptinfo['name'] + "' 아파트"); // 상단카드 헤더 변경
            $('#aptInfo_content').remove(); // 아파트tab html 내용 삭제

            // 본문 내용 추가
            var htmlCode = '';
            htmlCode += '<div id="aptInfo_content">';
            htmlCode += '<center><h5><b>'+ data.aptinfo['address'] +'</b><h5></center>';
            htmlCode += '<article style="color:#0A6EFF">최근 실거래 기준 1개월 평균';
            htmlCode += '<h3><b>10 억 4000</b></h3></article>';

            htmlCode += '<table class="table table-striped table-hover">';
            htmlCode += '<thead><tr><th>계약일</th><th>가격</th><th>전용면적</th><th>층</th></tr></thead>';
            htmlCode += '<tbody>';
            for(var i = 0; i < data.ts.length; i ++) {
                var amount = data.ts[i]['amount']
                var date = data.ts[i]['date']
                var area = data.ts[i]['area']
                var floor = data.ts[i]['floor']
                htmlCode += '<tr><td>' + moment(date).format('YYYY-MM-DD') + '</td><td>' + amount + '</td>';
                htmlCode += '<td>' + area + '</td><td>' + floor + '</td></tr>';
            }
            htmlCode += '</tbody></table></div>';

            $('#aptInfo_body').append(htmlCode);
        },
        error: function(request, status, error){
            alert('ajax 통신 실패')
            alert(error);
        }
    })
}
