[TOC]

![타이틀](https://user-images.githubusercontent.com/52685206/75149911-7033ed80-5746-11ea-82d0-c04e958451d5.PNG)

-----

# Getting Started

## BACKEND(Django) 와 DB(MySQL)

### ★ 실행 환경

* Python 3.7.x
* MySQL 8.0.x



### 0. `back` 폴더에서 진행

* PC 환경에서 실행 시 DB 관리를 위한 MySQL 은 기 설치되어 있음을 가정
* MySQL 의 ID/PW 로 인하여 runserver 구동이 안 될 수 있으므로 실행 전 반드시 ID/PW 일치 여부 확인



### 1. 파이썬 가상환경 생성

```bash
$ python -m venv venv
```



### 2. 파이썬 가상환경 실행

```bash
$ source venv/Scripts/activate
```



### 3. 백엔드와 DB 구동에 필요한 라이브러리 일괄 설치

```bash
(venv)
$ pip install -r requirements.txt
```



### 4. Django 구동(로컬 서버 이용 시)

```bash
(venv)
$ python manage.py runserver
```





## FRONTEND

### ★ 실행 환경

* Vue CLI 4.3.1



### 0. `front` 폴더에서 진행

* npm 과 yarn 은 기 설치되어 있음을 가정



### 1. 라이브러리 설치

```bash
$ npm install
```



### 2. 로컬 서버 실행

#### 1. npm 사용 시

```bash
$ npm run serve
```

#### 2. yarn 사용 시

```bash
$ yarn serve
```

* 두 가지 방법 모두 사용했음에도 구동 실패 시 `npm update` 후 재시도





-----

# 기획 의도

![기획의도1](https://user-images.githubusercontent.com/52685206/75510735-538e0300-5a2f-11ea-9c26-378245c5dcd2.PNG)

![기획의도2](https://user-images.githubusercontent.com/52685206/75510739-5557c680-5a2f-11ea-9f09-b7265fdc89e5.PNG)

![기획의도3](https://user-images.githubusercontent.com/52685206/75510740-5557c680-5a2f-11ea-85c4-ca33c3d947de.PNG)



# 팀 구성 및 역할

![팀구성및역할](https://user-images.githubusercontent.com/52685206/75510741-55f05d00-5a2f-11ea-96d7-16ce9ea0da7c.PNG)



# 개발 환경

![개발환경1](https://user-images.githubusercontent.com/52685206/75510742-5688f380-5a2f-11ea-9499-0044d41ced3a.PNG)

![개발환경2](https://user-images.githubusercontent.com/52685206/75510743-57218a00-5a2f-11ea-86e1-6190472cf04f.PNG)



# 개발 내용

![시스템아키텍처](https://user-images.githubusercontent.com/52685206/75510744-57ba2080-5a2f-11ea-9523-64cd96975c91.PNG)

![ERD](https://user-images.githubusercontent.com/52685206/75510745-57ba2080-5a2f-11ea-9fce-3b496615f671.PNG)

![구현기능목록](https://user-images.githubusercontent.com/52685206/75510746-5852b700-5a2f-11ea-85ee-29b409e49348.PNG)



# 주요 기능

![주요기능1](https://user-images.githubusercontent.com/52685206/75510747-58eb4d80-5a2f-11ea-83d5-7af64b6c60bf.PNG)



![주요기능2](https://user-images.githubusercontent.com/52685206/75510748-58eb4d80-5a2f-11ea-808c-f6503a93bd68.PNG)

![주요기능3](https://user-images.githubusercontent.com/52685206/75510749-5983e400-5a2f-11ea-8153-5887b819034c.PNG)

![주요기능4](https://user-images.githubusercontent.com/52685206/75511007-18400400-5a30-11ea-958f-ab872235d1e3.png)

![주요기능5](https://user-images.githubusercontent.com/52685206/75510753-5ab51100-5a2f-11ea-8309-7e7ba685ccab.PNG)



