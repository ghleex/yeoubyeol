# 공통 PJT: 웹 모바일 :office:

## Sub PJT Ⅲ: SNS 심화 기능 및 웹 큐레이션 기능 구현  :city_sunset:

### 1. 목표

* Vue-Roter, Vuex, Open API, Docker 에 대한 이해
* SNS 기본 기능(회원가입, 로그인, 프로필 변경, 알림 등) 구현
* 새벽 시간에만 만들 수 있는 감성을 담는 공간 완성하기



### 2. 환경 :deciduous_tree:

|               OS               |   Language   | Frontend |   Backend    |    DBMS     |
| :----------------------------: | :----------: | :------: | :----------: | :---------: |
| Windows 10 Enterprise (64-bit) | Python 3.7.x |  Vue.js  | Django 3.0.x | MySQL 8.0.x |
|     Ubuntu 18.04 (AWS EC2)     |  JavaScript  |          |              |             |

* DBMS 교체(SQLite3 → MySQL) 이유

  * 단일 사용자 對 복수 사용자 데이터베이스 측면
    * SQLite 는 데스크톱 또는 모바일 앱과 같이 동시 사용자가 한 명인 애플리케이션에 가장 적합
    * MySQL 과 마리아DB는 여러 명의 동시 사용자에 대응하도록 설계
    * MySQL 과 마리아DB는 클러스터 및 수평 확장 솔루션을 제공하나 SQLite 는 제공하지 않음
  * MySQL 의 다양한 데이터 형식 제공
    * MySQL 에 비해 SQLite 은 적은 수의 데이터 형식을 제공
    * 예> SQLite 에는 기본 datetime 형식이 존재하지 않아 애플리케이션에서 이러한 형식을 처리해야 함
    * 따라서 애플리케이션이 아닌 데이터베이스에서 datetime 값을 위한 입력을 정규화하고 제약하는데 MySQL 이 더욱 적합
  * MySQL 사용 시 수평 확장 설계 시 더욱 용이
    * SQLite 인스턴스는 단일체이며 독립적이고, 인스턴스 간 기본 동기화 기능 부재
    * SQLite 를 이용하여 DB 여러 개를 연합하거나 클러스터를 만들 수 없음
  * 여러 연결에서 SQLite 를 통한 동시 쓰기 작업 실행 시 성능 문제 발생
    * SQLite 는 쓰기 작업 시 데이터베이스를 잠그므로 여러 동시 쓰기 작업이 실행되는 앱에서는 성능 문제가 발생할 수 있음



### 3. 역할

|       Frontend       |       Backend       |
| :------------------: | :-----------------: |
| 김홍주, **조선행**** | **이길현***, 조규홍 |

*: 팀장 | **: CTO



### 4. System Architecture

![system_architecture](https://user-images.githubusercontent.com/52685206/73622923-59860380-467e-11ea-99e6-90881f1f614c.png) 



### 5. ER Diagram

<img src="https://user-images.githubusercontent.com/52685206/73625718-580e0880-4689-11ea-9e6c-f97c9b845baf.png" alt="erd" style="width: 70%; height: 70%;" />



### 6. Git Workflow (기능별로 세분화하여 수정 예정)

![git_workflow](https://user-images.githubusercontent.com/52685206/73424672-e1b09400-4372-11ea-9f27-163147f844d2.png)





-----



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

