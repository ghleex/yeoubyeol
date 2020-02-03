//기본 화면
import Home from './views/Home.vue'

// 비회원 기능
import AccountSendEmail from './views/Join/AccountSendEmail.vue'
import AccountSendEmailConfirm from './views/Join/AccountSendEmailConfirm.vue'
import AccountCreate from './views/Join/AccountCreate.vue'


// 회원 관리
import UserLogin from './views/User/UserLogin.vue'
import UserPwdSendEmail from './views/User/UserPwdSendEmail.vue'
import UserPwdSendEmailConfirm from './views/User/UserPwdSendEmailConfirm.vue'
import UserPwdChange from './views/User/UserPwdChange.vue'
import UserProfile from './views/User/UserProfile.vue'

//피드
import FeedMain from './views/Feed/FeedMain.vue'

//에러
import EPageNotFound from './views/Error/EPageNotFound.vue'
import EError from './views/Error/EError.vue'

//settings
import Noti from './views/Settings/Notification.vue'
import Follow from './views/Settings/Follow.vue'

//검색
import Search from './views/Search.vue'



const requireAuth = () => (to, from, next) => {
    if(sessionStorage.getItem('AUTH_token')){
    // if (this.$cookies.isKey('auth_cookie')) {
      return next();
    }
    next('/');
  };

const LoginUsersCantAccess = () => (to, from, next) => {
    if(!sessionStorage.getItem('AUTH_token')){
    // if (this.$cookies.isKey('auth_cookie')) {
      return next();
    }
    next('/error');
  };

  

export default [
    {
        path: '/',
        name: '홈',
        component: Home
    },
    //비회원 기능
    {
        path: '/join',
        name: '인증메일 발송',
        component: AccountSendEmail,
        beforeEnter: LoginUsersCantAccess()
    },
    {
        path: '/join/ok',
        component: AccountSendEmailConfirm,
        beforeEnter: LoginUsersCantAccess()
    },
    {
        path: '/join/form/:key',
        name: '회원가입',
        component: AccountCreate,
        beforeEnter: LoginUsersCantAccess()
    },
    //회원 관리
    {
        path: '/user/login',
        name: '로그인',
        component: UserLogin,
        beforeEnter: LoginUsersCantAccess()
    },
    {
        path: '/user/password',
        name: '비밀번호 변경',
        component: UserPwdSendEmail,
        beforeEnter: LoginUsersCantAccess()
    },
    {
        path: '/user/password/ok',
        component: UserPwdSendEmailConfirm,
        beforeEnter: LoginUsersCantAccess()
    },
    {
        path: '/user/password/:key',
        component: UserPwdChange,
        beforeEnter: LoginUsersCantAccess()
    },
    {
        path: '/user/:email',
        name: '프로필',
        component: UserProfile,
        beforeEnter: requireAuth()
        
    },
    //피드
    {
        path: '/feed',
        name: '메인피드',
        component: FeedMain
    },
    //에러
    {
        path: '/404',
        name: 'PageNotFound',
        component: EPageNotFound
    },
    {
        path: '/error',
        name: 'Error',
        component: EError
    },
    
    //settings
    {
        path: '/noti',
        name: '알림',
        component: Noti
    },
    {
        path: '/follow/:email',
        name: '팔로',
        component: Follow
    },

    //검색
    {
        path: '/search',
        name: '검색',
        component: Search
    },
    
    {
        path: '*',
        redirect: '/404'
    },
]