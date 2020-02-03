# 공통 PJT: 웹 모바일 :office:

## Sub PJT Ⅲ: SNS 심화 기능 및 웹 큐레이션 기능 구현  :city_sunset:

### 1. 목표

* Vue-Roter, Vuex, Open API, Docker 에 대한 이해
* SNS 기본 기능(회원가입, 로그인, 프로필 변경, 알림 등) 구현
* 새벽 시간에만 만들 수 있는 감성을 담는 공간 완성하기



### 2. 환경 :deciduous_tree:

|               OS               |   Language   | Frontend |   Backend    |     DBMS      |
| :----------------------------: | :----------: | :------: | :----------: | :-----------: |
| Windows 10 Enterprise (64-bit) | Python 3.7.x |  Vue.js  | Django 3.0.x |    SQLite3    |
|     Ubuntu 18.04 (AWS EC2)     |  JavaScript  |          |              | (MySQL 8.0.x) |

* SQLite3 → MySQL 교체 고려 이유

  * 단일 사용자 대 복수 사용자 데이터베이스
    * SQLite는 데스크톱 또는 모바일 앱과 같이 동시 사용자가 한 명인 애플리케이션에 가장 적합하다. MySQL과 마리아DB는 여러 명의 동시 사용자에 대응하도록 설계됐다. 또한 MySQL과 마리아DB는 클러스터 및 수평 확장 솔루션을 제공할 수 있지만 SQLite는 할 수 없다.

  * 강한 데이터 형식 지정 필요
    * SQLite의 데이터 형식은 비교적 소수이다. 예를 들어 기본 datetime 형식이 없다. 따라서 애플리케이션에서 이러한 형식을 처리해야 한다. 애플리케이션이 아닌 데이터베이스에서 datetime 값을 위한 입력을 정규화하고 제약 필요
  * 수평 확장 설계 필요
    * SQLite 인스턴스는 단일체이며 독립적이고, 인스턴스 간 기본 동기화 기능이 없다. 또한 여러 개를 연합하거나 클러스터를 만들 수 없기 때문
  * 여러 연결에서의 동시 쓰기 작업 실행 시 성능 문제 발생
    * SQLite는 쓰기 작업 시 데이터베이스를 잠그므로 여러 동시 쓰기 작업이 실행되는 앱에서는 성능 문제가 발생할 수 있기 때문



### 3. 역할

|    Frontend    |       Backend       |
| :------------: | :-----------------: |
| 김홍주, 조선행 | **이길현***, 조규홍 |

*: 팀장



### 4. ER Diagram (알림센터 모델링 보완 후 확정 게시)

TBA





### 5. Git Workflow (기능별로 세분화하여 수정 예정)

![git_workflow](https://user-images.githubusercontent.com/52685206/73424672-e1b09400-4372-11ea-9f27-163147f844d2.png)



### Screenshot

#### 1. Mobile @ Android

<img src="https://user-images.githubusercontent.com/52685206/73453138-bb104e80-43ae-11ea-946e-de54e9845c94.jpg" alt="Screenshot_20200130-214239_Samsung Internet" style="width: 50%; height: 50%;" />

<img src="https://user-images.githubusercontent.com/52685206/73453140-bc417b80-43ae-11ea-81e6-ae27c2ba9a14.jpg" alt="Screenshot_20200130-214247_Samsung Internet" style="width: 50%; height: 50%;" />

<img src="https://user-images.githubusercontent.com/52685206/73453142-bcda1200-43ae-11ea-9e36-0e3c9063a5a1.jpg" alt="Screenshot_20200130-214300_Samsung Internet" style="width: 50%; height: 50%;" />

<img src="https://user-images.githubusercontent.com/52685206/73453145-be0b3f00-43ae-11ea-8861-55b8c54658a4.jpg" alt="Screenshot_20200130-214311_Samsung Internet" style="width: 50%; height: 50%;" />





#### 2. Mobile @ IPadOS

<img src="https://user-images.githubusercontent.com/52685206/73453064-9320eb00-43ae-11ea-8d3b-56c4678c7368.jpg" alt="Image from iOS - 1" style="width: 50%; height: 50%;" />

<img src="https://user-images.githubusercontent.com/52685206/73453065-94521800-43ae-11ea-8a8f-6c2ccc78cb00.png" alt="Image from iOS - 2" style="width: 50%; height: 50%;" />

<img src="https://user-images.githubusercontent.com/52685206/73453073-96b47200-43ae-11ea-8cfe-748a32ff3c99.png" alt="Image from iOS - 3" style="width:50%; height:50%" />

