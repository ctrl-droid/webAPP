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

function renderchart(data){
    var date = []
    var amount = []
    var datalen = data.ts.length;
    for(var i = 0; i < datalen; i ++) {
        date.push(moment(data.ts[datalen-i-1]['date']).format('YYYY-MM-DD'));
        amount.push(data.ts[datalen-i-1]['amount']);
    }
    new Chart(document.getElementById("line-chart"), {
        type: 'line',
        data: {
            labels: date,
            datasets: [{
                data: amount,
                label: data.aptinfo['name'],
                borderColor: "#3e95cd",
                fill: false
            }]
        }
    });
}

function aptClick(sn){
    aptInfo_tab(); // 상단 텝 변경
    var postdata = {'sn':sn} // 데이터를 서버로 전달시 JSON 방식으로 전달
    $.ajax({
        type: 'POST',
        url: '/index/showAptInfo',
        data: JSON.stringify(postdata),
        contentType: "application/json",
        success: function(data){
            moveBounds(sn); // 지도의 위치를 변경해줌
            $('#aptInfo_tab').text("'"+ data.aptinfo['name'] + "' 아파트"); // 상단탭 이름 변경
            $('#aptInfo_title').text("'"+ data.aptinfo['name'] + "' 아파트"); // 상단카드 헤더 변경

            // aptInfo_content1 본문 내용 추가
            $('#aptInfo_content1_del').remove(); // 아파트tab html 내용 삭제
            var htmlCode = '';
            htmlCode += '<div id="aptInfo_content1_del">';
            htmlCode += '<center><h5><b>'+ data.aptinfo['address'] +'</b><h5></center>';
            htmlCode += '<article style="color:#0A6EFF">최근 실거래 기준 1개월 평균</article>';
            var strsn = "'" + sn + "'"
            htmlCode += '<article style="float:right">전용면적<select id="select_area" onchange="areaClick('+ strsn +')">';
            for(var i = 0; i < data.uniqArea.length; i ++) {
                htmlCode += '<option>' + data.uniqArea[i] + '</option>';
            }
            htmlCode += '</select></article></div>';
            $('#aptInfo_content1').append(htmlCode);

            dataContent(data);
            content5(data, sn);
        },
        error: function(request, status, error){
            alert('ajax 통신 실패')
            alert(error);
        }
    })
}

function areaClick(sn){
    var langSelect = document.getElementById("select_area");
    var selectText = langSelect.options[langSelect.selectedIndex].text;

    var postdata = {'sn':sn, 'area':selectText} // 데이터를 서버로 전달시 JSON 방식으로 전달
    $.ajax({
        type: 'POST',
        url: '/index/showSelect',
        data: JSON.stringify(postdata),
        contentType: "application/json",
        success: function(data){
            dataContent(data);
        },
        error: function(request, status, error){
            alert('ajax 통신 실패')
            alert(error);
        }
    })
}

function dataContent(data){
    // aptInfo_content2 본문 내용 추가
    $('#aptInfo_content2_del').remove(); // 아파트tab html 내용 삭제
    var htmlCode = '';
    htmlCode += '<div id="aptInfo_content2_del">';
    htmlCode += '<h3 style="color:#0A6EFF"><b>'+ data.avgAmount +'</b></h3></div>';
    $('#aptInfo_content2').append(htmlCode);

    // aptInfo_content3 본문 내용 추가
    $('#aptInfo_content3_del').remove(); // 아파트tab html 내용 삭제
    var htmlCode = '';
    htmlCode += '<div id="aptInfo_content3_del">';
    htmlCode += '<canvas id="line-chart" width="300" height="250"></canvas></div>';
    $('#aptInfo_content3').append(htmlCode);
    renderchart(data); // 초기 차트 그려주기

    // aptInfo_content4 본문 내용 추가
    $('#aptInfo_content4_del').remove(); // 아파트tab html 내용 삭제
    var htmlCode = '';
    htmlCode += '<div id="aptInfo_content4_del">';
    htmlCode += '<table class="table table-striped table-hover">';
    htmlCode += '<thead><tr><th>계약일</th><th>가격</th><th>전용면적</th><th>층</th></tr></thead>';
    htmlCode += '<tbody>';
    for(var i = 0; i < data.ts.length; i ++) {
        var amount = data.ts[i]['amount_str'];
        var date = data.ts[i]['date'];
        var area = data.ts[i]['area'];
        var floor = data.ts[i]['floor'];
        htmlCode += '<tr><td>' + moment(date).format('YYYY-MM-DD') + '</td><td>' + amount + '</td>';
        htmlCode += '<td>' + area + '</td><td>' + floor + '</td></tr>';
    }
    htmlCode += '</tbody></table>';
    htmlCode += '</div>';
    $('#aptInfo_content4').append(htmlCode);
}

function content5(data, sn){
    $('#aptInfo_content5_del').remove(); // 아파트tab html 내용 삭제
    var htmlCode = '';
    htmlCode += '<div id="aptInfo_content5_del">';
    htmlCode += '<div class="card mb-auto"><div class="card-header">게시판</div><div class="card-body">';
    htmlCode += '<div class="input-group">';
    htmlCode += '<input class="form-control" id="board_content" type="text" placeholder="게시글 입력"/>';
    var strsn = "'" + sn + "'";
    htmlCode += '<input class="btn btn-primary" type="button" value="등록!" onclick="boardAdd('+ strsn +')"/></div>';
    htmlCode += '<table class="table table-striped table-hover">';
    htmlCode += '<thead><tr><th>목록</th></tr><thead>';
    htmlCode += '<tbody>';
    for(var i = 0; i < data.boards.length; i ++) {
        var member_id = data.boards[i]['member_id'];
        var code = data.boards[i]['code'];
        var date = data.boards[i]['date'];
        var content = data.boards[i]['content'];
        var strcode = "'" + code + "'";
        loginid

        htmlCode += '<tr><td><div"float:left">id: ' + member_id + '</div><div style="float:right">작성일: '+ moment(date).format('YYYY-MM-DD')
        if(loginid === member_id){
            htmlCode += ' <img src="/static/assets/letter-x.png" onclick="boardDel('+ strsn +','+ strcode +')">';
        }
        htmlCode += '</div><br><br><div>'+ content + '</div>'
        htmlCode += '</td></tr>';
    }
    htmlCode += '</tbody></table>';
    htmlCode += '</div></div>';
    $('#aptInfo_content5').append(htmlCode);
}

function boardAdd(sn){
    var board_content = $('#board_content').val();
    var postdata = {'sn':sn, 'content':board_content} // 데이터를 서버로 전달시 JSON 방식으로 전달

    $.ajax({
        type: 'POST',
        url: '/index/boardAdd',
        data: JSON.stringify(postdata),
        contentType: "application/json",
        success: function(data){
            content5(data, sn)
        },
        error: function(request, status, error){
            alert('로그인 해주세요!')
        }
    })
}

function boardDel(sn, code){
    flag=confirm('정말 삭제 하시겠습니까?')
    if(flag){
        var postdata = {'sn':sn, 'code':code}
        $.ajax({
            type: 'POST',
            url: '/index/boardDel',
            data: JSON.stringify(postdata),
            contentType: "application/json",
            success: function(data){
                content5(data, sn)
            },
            error: function(request, status, error){
                alert('로그인 해주세요!')
            }
        })
    }else{
        alert('탈퇴가 취소 되었습니다')
    }
}

