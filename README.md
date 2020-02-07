## ![main](https://user-images.githubusercontent.com/52685206/73918007-002f0600-4904-11ea-800e-2fd950a3781e.png)

### THE AIMS OF THE PROJECT :dart:

* Django, Vue-Router, Vuex, Open API, Docker 에 대한 이해
* SNS 기본 기능(회원가입, 로그인, 프로필 변경, 알림 등) 구현
* “여우별” 만의 차별화 요소 구현
* 새벽에 넘치는 감성을 담는 공간 완성하기



### ENVIRONMENTS :deciduous_tree:

|               OS               |   Language   | Frontend |   Backend    |    DBMS     |
| :----------------------------: | :----------: | :------: | :----------: | :---------: |
| Windows 10 Enterprise (64-bit) | Python 3.7.x |  Vue.js  | Django 3.0.x | MySQL 8.0.x |
|     Ubuntu 18.04 (AWS EC2)     |  JavaScript  |          |              |             |

* DBMS 교체(SQLite3 → MySQL) 이유

  * 단일 사용자 對 복수 사용자 데이터베이스 측면
    * MySQL 은 여러 명의 동시 사용자에 대응하도록 설계
    * MySQL 은 클러스터 및 수평 확장 솔루션을 제공하나 SQLite 는 제공하지 않음
  * MySQL 의 다양한 데이터 형식 제공
    * MySQL 에 비해 SQLite 은 적은 수의 데이터 형식을 제공
    * 예> SQLite 에는 기본 datetime 형식이 존재하지 않아 애플리케이션에서 이러한 형식을 처리해야 함
    * 따라서 애플리케이션이 아닌 데이터베이스에서 datetime 값을 위한 입력을 정규화하고 제약하는데 MySQL 이 더욱 적합
  * MySQL 사용 시 수평 확장 설계 시 더욱 용이
    * SQLite 인스턴스는 단일체이며 독립적이고, 인스턴스 간 기본 동기화 기능 부재
    * SQLite 를 이용하여 DB 여러 개를 연합하거나 클러스터를 만들 수 없음
  * 여러 연결에서 SQLite 를 통한 동시 쓰기 작업 실행 시 성능 문제 발생
    * SQLite 는 쓰기 작업 시 데이터베이스를 잠그므로 여러 동시 쓰기 작업이 실행되는 앱에서는 성능 문제가 발생할 수 있음



### ROLES

|       Frontend       |       Backend       |
| :------------------: | :-----------------: |
| 김홍주, **조선행**** | **이길현***, 조규홍 |

*: 팀장 | **: CTO





<img src="https://user-images.githubusercontent.com/52685206/73917727-5780a680-4903-11ea-969c-c48dd3d8ff10.png" alt="system_architecture"/>





### ER Diagram

<img src="https://user-images.githubusercontent.com/52685206/73899106-ed4e0e80-48ce-11ea-9fe5-df61f8029bfd.png" alt="erd"/>





<img src="https://user-images.githubusercontent.com/52685206/73899976-9269e680-48d1-11ea-8d7b-bf01a1e138ab.png" alt="git_workflow"/>

#### Rules of writing a commit message

1. **핵심: 어느 이슈에 대하여 어떤 일이 이루어졌는지 누구든지 보고 이해할 수 있어야 함**
2. 규칙: `"JIRA ISSUE # | status | 'Message of the issue' "`
   * Sample: `"S02P13B203-14 | -ing | Add FEED templates on sth"`
3. 영문 기준 50자 이내
4. 시작 단어: 동사로
   * In progress: `-ing`
   * Finished: `-ed`

4. 끝에 `.` 붙이지 않음





<img src="https://user-images.githubusercontent.com/52685206/73917713-4e8fd500-4903-11ea-9ccb-b70b38a15480.png" alt="differences"/>



-----

-----



### Screenshot

#### 1. Android

<img src="https://user-images.githubusercontent.com/52685206/73724521-df817780-476e-11ea-8b6f-ddadb806b225.jpg" alt="Screenshot_20200204-164832_Samsung Internet" style="width:50%;" />





#### 2. IPadOS

<img src="https://user-images.githubusercontent.com/52685206/73724519-df817780-476e-11ea-8677-78bcf7b553f7.PNG" alt="IMG_0074" style="width:70%;" />

