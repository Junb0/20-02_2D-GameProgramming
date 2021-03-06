# 실행 방법

1. setup.exe 실행

2. 설치 디렉토리 설정
3. 설치된 디렉토리 내부에 실행파일 DQ.exe 로 실행
4. 설치된 디렉토리 내부의 readme.txt 에 조작법 수록

# 1. 게임 소개

#### 제목 : Defender's Quest

저는 20년도 1학기 윈도우 프로그래밍 텀프로젝트로 Defender's Quest 라는 탑뷰형 슈팅 디펜스 게임을 제작했었습니다.

winAPI 기반으로 제작했던 게임이었는데, api특성과 짧은 개발기간 탓에 게임 분량, 퀄리티등이 아쉬웠습니다. 이번 2D게임프로그래밍 텀프로젝트를 통해 pico2D기반으로 리메이크 해볼 예정입니다.

**게임 스크린샷**

![1](https://user-images.githubusercontent.com/56647868/94181878-1281a280-fedb-11ea-96e6-ce88dc7ace2e.PNG)

![2](https://user-images.githubusercontent.com/56647868/94181904-1d3c3780-fedb-11ea-80ec-9d71577a1d88.PNG)

**게임 목적 및 방법**

상하좌우 이동이 가능한 캐릭터를 조작(이동, 공격) 하여 우측에서 소환되는 적들을 막아내 최종 웨이브가 끝날 때 까지 버티는 것이 목적입니다.

웨이브가 시작되면 적들이 소환(웨이브가 지날수록 더 강하고 많은 적들이 몰려옵니다.)되어 좌측으로 이동합니다. 공격 사정거리까지 걸어온 적들은 벽을 향해 공격을 하며 이때 HP가 감소합니다.

적들을 처치하면 골드를 획득하며 골드를 소모하여 공격력 증가, 탄창 용량 증가, 동료 소환, hp 회복등의 행동이 가능합니다. 골드를 더 적게 소모하여 클리어 할 수록 더 많은 보너스 스코어를 얻습니다.



# 2. GameState의 수 및 이름

총 게임 스테이트는 5가지 입니다.

**1. 로고 스테이트**

**2. 타이틀 스테이트**

**3. 인 게임 스테이트**

**4. 환경설정 스테이트**

**5. 게임 결과  스테이트**



# 3. 각 GameState별 설명

### 1. 로고 스테이트

게임 실행시 잠시 로고 이미지가 페이드 인, 페이드 아웃 되는 화면입니다. 로고 표시 이후 타이틀 스테이트로 이동합니다.

**표시할 객체**

- 로고 이미지(KPU 로고 사용할 예정)

**처리할 키/마우스 이벤트**

- 없음

**다른 State로의 이동**

- 일정 시간 이후 자동으로 **타이틀 스테이트로 이동**



### 2. 타이틀 스테이트

게임 타이틀 이미지, 게임시작 버튼, 환경설정 버튼이 존재하는 타이틀 화면입니다.

**표시할 객체**

- 게임 타이틀 이미지
- 게임시작 버튼
- 환경설정 버튼

**처리할 키/마우스 이벤트**

- 게임시작 버튼, 환경설정 버튼 클릭을 위한 마우스 클릭 처리

**다른 State로의 이동**

- 게임시작 버튼 클릭 시 **인 게임 스테이트로 이동**
- 환경설정 버튼 클릭 시 **환경설정 스테이트로 이동**



### 3. 인 게임 스테이트

주인공, 적, UI, 기타 오브젝트들이 표시되며 상호작용 하는 실제 게임화면입니다.

**표시할 객체**

- 주인공 캐릭터
- 주인공 캐릭터 무기
- 주인공 발사 투사체
- 백그라운드 이미지
- 지형 이미지
- 적 캐릭터(3종류)
- 적 발사 투사체
- 벽(지켜야 할 대상)
- 안내 문구(웨이브 시작, 업그레이드 완료 등) UI
- 현재 스코어 UI
- 현재 체력 UI
- 현재 보유 골드 UI
- 무기 이미지 및 남은 탄약수 UI
- 현재 웨이브 UI
- 업그레이드 아이콘 및 가격 UI

**처리할 키/마우스 이벤트**

- 캐릭터 이동을 위한 키보드 입력(상하좌우 화살표 버튼)
- 무기 발사를 위한 키보드 입력(Z키)
- 무기 재장전을 위한 키보드 입력(X키)
- 업그레이드를 위한 키보드 입력(1, 2, 3, 4 숫자키)
- 환경설정 스테이트로 이동을 위한 키보드 입력(ESC키)

**다른 State로의 이동**

- ESC키 입력 시 **환경설정 스테이트로 이동**
- HP 값이 0 이하로 내려갈 시 **게임 결과 스테이트로 이동**(게임오버)
- 모든 웨이브의 적 처치 시 **게임 결과 스테이트로 이동**(승리 및 스코어 결산)



**구현해야 할 요소들**

- 캐릭터 몸체와 무기 개별 상태 적용

* 총알에 맞은 적 경직

- 재장전
  재장전 애니메이션 적용
  재장전 도중 공격 불가

- HP가 **0** 이하로 떨어진 적 사망
  사망 애니메이션 적용
  사망 후 스코어 및 골드 증가
- 골드를 소모하여 업그레이드
  공격력, 탄창 용량, 동료 고용, 한 업그레이드 끝까지 도달 시 추가 보너스 능력치
- 동료 오브젝트
  적이 존재할 때 자동으로 사격
  주인공과 공격력 공유(동일한 총알 오브젝트 생성)
- 각 웨이브 시작 시 적 생성
  웨이브 마다 정해진 범위 내에서 적들이 랜덤 스폰
  스폰 이펙트 애니메이션 존재
- 적 이동
  우측에서 생성된 적들이 점점 좌측으로 걸어감
  특정 범위 내에 들어가면 좌측 벽을 향해 공격
  벽이 공격에 맞으면 UI에 있는 HP 감소

### 4. 환경설정 스테이트

볼륨조절, 난이도 조절(새로 시작시 적용), 타이틀 화면 이동, 뒤로가기 기능을 위한 환경설정 화면입니다.

**표시할 객체**

- 볼륨조절 버튼(0~10까지 좌우 화살표 버튼을 마우스로 클릭하여 조절)
- 난이도 조절 버튼 (Easy, Normal, Hard 버튼 존재, 새로 시작 시 적용)
- 뒤로가기 버튼
- 타이틀 화면으로 이동 버튼

**처리할 키/마우스 이벤트**

- 버튼 클릭을 위한 마우스 입력 처리

**다른 State로의 이동**

- 뒤로가기 버튼 클릭 시 **이전 스테이트(타이틀 스테이트, 인 게임 스테이트)로 이동**
- 타이틀 화면으로 이동 버튼 클릭 시 **타이틀 화면으로 이동**(인 게임에서 현재 게임 포기)



### 5. 게임 결과  스테이트

게임오버, 게임 클리어 시 결과를 출력하는 화면입니다.

**표시할 객체**

- 게임 결과 문구 (GameOver, Game Clear)
- (클리어시) 최종 스코어
- 처치한 적 수
- 획득한 골드
- 소모한 골드
- 타이틀 화면으로 이동 버튼

**처리할 키/마우스 이벤트**

- 타이틀 화면으로 이동 버튼 클릭을 위한 마우스 입력 처리

**다른 State로의 이동**

- 타이틀 화면으로 이동 버튼 클릭 시 **타이틀 화면으로 이동**



### State간 이동 다이어그램

![3](https://user-images.githubusercontent.com/56647868/94181924-275e3600-fedb-11ea-9c3d-272d7b726df7.PNG)

# 4. 필요한 기술

- 현재 2D 게임프로그래밍 과목에서 배우는 기본적인 pico2D 기능 (이미지 출력, 사운드 출력)

- 자료구조 과목에서 배운 여러 자료구조 형태(적, 투사체 관리를 위한 List등)
- 윈도우 프로그래밍 과목에서 구현했던 Defender's Quest 로직

**배울 것으로 기대되는 기술**

- pico2D 혹은 또다른 모듈을 사용한 **사운드 출력**
- 하이스코어 등을 저장할 수 있는 **파이썬 기반 파일 입출력**

- 일반적인 게임 프로그래밍에서 사용되는 **객체 관리**(적, 투사체 등)

**수업에서 다루어 주셨으면 하는 기술**

- 이미지 회전
- Texture Packer 등의 리소스 관리 툴

# 5. 객체 설명

**레이어 구조**
-bg, any, ui 세가지 레이어 존재
-any 레이어에 대부분 주요 오브젝트 저장
-각 객체의 ground 값을 기반으로 필요할 때 정렬
 \- 결과적으로 입체감 있는 레이어링 표현

**Player 객체**
-싱글톤 클래스
-Body, Weapon 싱글톤 클래스로 이루어짐
-Body, Weapon 은 별개로 동작
-Gold, Life 값이 저장됨
-적과 충돌하는 Bullet 을 생성하여 오브젝트 리스트에 추가

**Enemy 객체**
-Enemy 클래스에 기본적인 변수 및 동작 선언 (체력, 공격력, 공격속도, 공격, 이동, idle 등)
-Enemy를 상속받는 세가지 종류의 적 클래스 존재
-각 적마다 공격패턴, 생성 총알 종류 등이 다름
-벽과 부딪히면 player의 life를 감소시키는 총알 오브젝트 생성

**Spawner 객체**
-적 생성 이펙트 표시
-임의의 위치에 적을 생성하는 기능을 함수를 통해 간편하게 접근

**Tower 객체**
-골드를 소모하여 지정된 위치에 소환
-공격 범위에 적이 존재하면 idle -> attack 상태변경
-적을 향해 자동으로 총알 발사

**Bullet 객체**
-대부분의 상호작용의 주체
-종류별 총알 클래스 들이 Bullet 클래스를 상속받음
-플레이어, 타워의 총알 : ingame 스테이트 에서 적과의 충돌체크 후 적의 체력 감소시키고 소멸
-적의 총알 : 벽과의 충돌체크 후 플레이어의 hp를 감소시키고 소멸
-특수 총알은 자식 총알들을 생성시킨 후 소멸

**UI 객체**
-싱글톤 클래스
-플레이어 객체를 참조하여 life, gold, ammo등을 표시
-실제 값과 display값을 구분하여 숫자가 1씩 가감되는 효과


# 6. 개발 일정

•1주차 : Todo 리스트 작성 및 필요 리소스 정리(스프라이트, 사운드)

•2주차 : pico2D 기반 프레임워크 적용 (gfw, gobj, main_state 등), 이미지 출력

•3주차 : 주인공 오브젝트 구현 (Idle, Walk, Fire) 상태별 애니메이션 및 이동, 공격

•4주차 : 적 오브젝트 구현 및 총알과 충돌처리

•5주차 : 웨이브 컨트롤 (json 등으로 웨이브 정보 저장 예정), 업그레이드, 동료 오브젝트 구현

•6주차 : 밸런스 조정 및 디버깅 -> 인 게임 스테이트 완성,
 로고, 타이틀, 환경설정, 게임 결과 스테이트 완성 및 상호간 이동 구현

•7주차 : 디버깅 및 발표자료 제작

•8주차 : 디버깅 및 발표자료 제작 



**11-23일자 진행상황**

-플레이어 조작 및 상황 별 애니메이션 : 100%

-적 오브젝트 구현 및 생성 : 100%

-아군 오브젝트 구현 및 생성 : 100%

-종류별 총알 및 총알의 충돌처리 : 100%

-UI 프레임 및 UI 폰트 표시 : 70%

-밸런싱 및 레벨디자인 : 50%

남은작업

-타이틀 등의 스테이트와 인게임 스테이트간 연결

-웨이브 레벨디자인

-플레이어 능력치, 업그레이드 밸런싱

-배경음악, 효과음



# 발표 동영상 링크

1차 발표 : https://youtu.be/TOXVylcWYkk

2차 발표 : https://youtu.be/OiKccU0-0Ys

최종 발표 : https://youtu.be/PQnJA3ZdoZE