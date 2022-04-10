<h2>Target site</h2>
<h3>사이트 소개</h3>
시디즈 - 의자 쇼핑몰(https://www.sidiz.com/)
<h3>사이트 선정 이유</h3>
깔끔한 UI와 더불어 적당한 시각적 효과가 들어가 적절하게 동적인 홈페이지입니다. 많은 이미지를 깔끔하고 감각적으로 배치해서 유저가 보기에 편하고 감각적인 느낌을 줍니다. 정적이라고 느껴질 수 있는 홈페이지를 시각적인 효과로 조금 더 풍부하게 만들 수 있는 연습을 할 수 있을 것 같았습니다.

<h2>초기기획 & ERD</h2>
<h3>ERD</h3>
<image src='https://user-images.githubusercontent.com/89664413/162617906-b9670b30-9179-4ce8-98c1-a5df125c120a.png'/>

<h3>User flow</h3>
<h3>초기기획 및 구현 목표</h3>
회원가입/로그인, 제품리스트, 제품상세, 장바구니

<h2>개발기간 및 팀원</h2>
<h3>개발기간</h3>
개발기간 : 3/28 ~ 4/8
<h3>개발인원 및 파트</h3>
팀원 : <프론트엔드> 구본희, 김경현, 김민수, 김재도 </br> 
      <백엔드> 박지훈, 황정현

<h2>적용 기술 및 구현 기능</h2>
<h3>기술 스택</h3>
python, django, mysql, AWS, JWT, Bcrypt
<h3>구현기능</h3>
회원가입/로그인, 제품리스트, 제품상세, 장바구니, 스마트 파인더
<h2>API 기능정의서</h2>
엔드포인트별 기능 정의</br>

1. USERS</br>
    1) 회원가입 POST :8000/users/signup  :정규식을 이용한 유효성 검사, bcrypt를 패스워드 암호화</br>
    2) 로그인 POST :8000/users/signin  : bcrypt를 이용한 암호체크, jwt를 이용한 토큰 발행</br>
    
2. Carts</br>
    1) 장바구니 담기 POST :8000/carts.   :get_or_created를 이용한 장바구니 등록</br>
    2) 장바구니 불러오기 GET :8000/carts
    3) 장바구니 수량 업데이트 PATCH :8000/carts/{cart_id} :Path parameter를 이용하여 해당 장바구니의 수량 수정 </br>
    4) 장바구니 삭제 DELETE :8000/carts?id={cart_id}&id={cart_id} :Query parameter를 이용하여 해당하는 장바구니들을 선택 삭제 </br>
  
3. Products</br>
GET 요청에 의한 정보 호출, Q객체 를 이용한 다중 필터 검색, end_point 따라서 다른 정보 호출 </br>
    1) products/   => 카테고리별 상품 목록 호출</br>
    2) products/<int:products_id> => 제품 상세보기</br>
    3) products/smart(qs) => Query String 에 의한 필터</br>

<h2>시연 영상</h2>
