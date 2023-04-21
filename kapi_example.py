import kapi 

#로그인 쿠키값 지정
kapi.vcookie = '쿠키값 입력할것!'

#로그인 여부 확인
print(kapi.isloged()) #True 또는 False 반환

#게시글 작성하기
#컨텐츠 list 제외하고 나머지는 기본값 세팅 있음
#writestr(컨텐츠 list, 글 공개 범위, 모두 댓글 허용, 필독, 공유 허용, 위치 첨부, url 첨부)
#글 공개 범위 : 'M' = 나만 보기, 'F' = 친구공개, 'A' = 전체공개 (우리끼리 보기는 귀찮아서 안넣음, 값은 'P' )
#위치 첨부 양식
locarr = {
        'name': '표시할 위치', 
        'location_id': 'da_1',
        'latitude': 61.1762605,
        'longitude':-44.457894
    }
#url 첨부 양식
urlarr = {
        'title': "링크 제목 텍스트",
        'description': "링크 설명 텍스트",
        'host': "링크 주소 텍스트",
        'image':["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTikctOXtlw4U1stsgcs7TyEgIrcF_4Sq8wnbyzlALEJeXuzTF0AMiAWMYAONNQLFcXLIc&usqp=CAU"], #이미지 주소, 외부 이미지도 가능
        'url': "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=7s", #클릭시 접속될 url 주소
        'is_opengraph': True,
        'requested_url': "",
        'richscrap': {},
        'section': "",
        'site_name': "",
        'type': "website",
        'view_type': ""
    }
#텍스트 리스트 양식
maincontent = []
maincontent.append({"type":"text","text":'일반 텍스트'})
maincontent.append({"type":"hashtag","text":'해시태그 텍스트',"hashtag_type":"","hashtag_type_id":""})
maincontent.append({"type":"profile","id":'_e1b530',"text":'태그 텍스트'})
#kapi.writestr(maincontent) 
print(kapi.writestr(maincontent,'F',True,False,True,locarr,urlarr) ) #작성 성공시 작성된 글 id, 실패시 None 반환

#게시글 공유하기
print(kapi.sharecontent('_e1b530.GIiBsrwuwAA',maincontent,'F',True,False,True,locarr)) #위에꺼랑 똑같음, 공유할 게시글 id 필요, url 첨부 불가능, 성공시 작성된 글 id, 실패시 None 반환

#게시글 삭제하기
print(kapi.deletestr('_e1b530.GIiBsrwuwAA')) #게시글 id 넣어야함, 삭제 성공시 True, 실패시 False 반환

#게시글 설정하기
print(kapi.setstr('_e1b530.GIiBsrwuwAA','F',True,False,True)) #게시글의 공개범위, 친댓, 공유, 필독 설정 변경

#친구 요청 불러오기
print(kapi.getinvite()) #친구 요청 온 목록만 반환

#친구 요청 수락하기
print(kapi.acceptinvite('_e1b530')) #수락할 유저 id 넣어야함, 실패시 None 반환

#유저 프로필 불러오기
print(kapi.getprofile('_e1b530')) #불러올 유저 id 넣어야함

#피드에 새로운 글이 있는지 확인하기
print(kapi.hasnewfeed()) #있으면 True, 없으면 False 반환

#피드 불러오기
print(kapi.getfeed()) #피드 목록 불러옴, 실패시 None 반환

#댓글 작성하기
subcontent = []
subcontent.append({"type":"text","text":"기본 텍스트"})
subcontent.append({"type":"profile","id":'_e1b530',"text":'태그 텍스트'})
print(kapi.writecomment('_e1b530.GIiBsrwuwAA',subcontent,'돌망구!')) #성공시 True, 실패시 False 반환
#kapi.writecomment(게시글 id ,텍스트 list ,알림창에 뜰 미리보기 텍스트)

#게시글에 느낌 달기
print(kapi.addemotion('_e1b530.GIiBsrwuwAA',1)) #성공시 True, 실패시 False 반환
#kapi.addemotion(게시글 id ,느낌 코드)
#좋아요 멋져요 기뻐요 슬퍼요 힘내요 순서대로 0 1 2 3 4

#친구 목록 불러오기
print(kapi.getfriend()) #성공시 친구 목록, 실패시 None 반환

#친구 삭제하기
print(kapi.remfriend('_e1b530')) #request 응답코드 반환

#한줄소개 설정하기
print(kapi.setstatus('돌망구!')) #성공시 True, 실패시 False 반환

#소식받기, 소식받기 해제
print(kapi.followuser('_e1b530')) 
print(kapi.unfollowuser('_e1b530'))
#성공시 True, 실패시 False 반환

#이미지 불러오기
kapi.loadimg('이미지 url') #이미지를 cv2로 로드해 반환