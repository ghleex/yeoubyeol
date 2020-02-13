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
import UserProfile from './views/User/UserProfile.vue'
import UserProfileSettings from '@/views/User/UserProfileSettings.vue'

//피드
import FeedMain from './views/Feed/FeedMain.vue'
import FeedCreateUpdate from '@/views/Feed/FeedCreateUpdate.vue'
import FeedComment from '@/views/Feed/FeedComment.vue'

//명예의 전당
import FeedOfFame from '@/views/Feed/FeedOfFame.vue'

//에러
import EPageNotFound from './views/Error/EPageNotFound.vue'
import EError from './views/Error/EError.vue'

//settings
import Noti from './views/Settings/Notification.vue'
import Follow from './views/Settings/Follow.vue'

//검색
import Search from './views/Search.vue'
import FeedSearchResultByKeyword from './views/Feed/FeedSearchResultByKeyword.vue'
import hongjuLab2 from './views/hongjuLab2.vue'

var value1 = document.cookie.match('(^|;) ?' + 'auth_cookie' + '=([^;]*)(;|$)');
var cookie1 = value1? value1[2] : null;

var value2 = document.cookie.match('(^|;) ?' + 'refresh_cookie' + '=([^;]*)(;|$)');
var cookie2 = value2? value2[2] : null;

const requireAuth = () => (to, from, next) => {
    if(cookie1 && cookie2){
    // if (this.$cookies.isKey('auth_cookie')) {
      return next();
    } else {
        alert('로그인이 필요합니다.')
        next('/');
    }
  };

const LoginUsersCantAccess = () => (to, from, next) => {
    if(!cookie1 || !cookie2){
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
        // beforeEnter: LoginUsersCantAccess()
    },
    {
        path: '/join/ok',
        component: AccountSendEmailConfirm,
        // beforeEnter: LoginUsersCantAccess()
    },
    {
        path: '/join/form/:key',
        name: '회원가입',
        component: AccountCreate,
        // beforeEnter: LoginUsersCantAccess()
    },
    //회원 관리
    {
        path: '/user/login',
        name: '로그인',
        component: UserLogin,
        // beforeEnter: LoginUsersCantAccess()
    },
    {
        path: '/user/password',
        name: '비밀번호 변경',
        component: UserPwdSendEmail,
        // beforeEnter: LoginUsersCantAccess()
    },
    {
        path: '/user/password/ok',
        component: UserPwdSendEmailConfirm,
        // beforeEnter: LoginUsersCantAccess()
    },
    {
        path: '/user/:email',
        name: '프로필',
        component: UserProfile,
        // beforeEnter: requireAuth()
        
    },
    {
        path: '/user/:email/settings',
        name: '프로필 변경',
        component: UserProfileSettings,
        // beforeEnter: requireAuth()
    },
    //피드
    {
        path: '/feed',
        name: '메인피드',
        component: FeedMain,
        // beforeEnter: requireAuth()
    },
    {
        path: '/feed/up',
        name: '피드 저장',
        component: FeedCreateUpdate,
        // beforeEnter: requireAuth()
    },
    {
        path: '/feed/:id',
        name: '댓글',
        component: FeedComment,
        // beforeEnter: requireAuth()
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
        component: Noti,
        // beforeEnter: requireAuth()
    },
    {
        path: '/follow/:email',
        name: '팔로',
        component: Follow,
        // beforeEnter: requireAuth()
    },

    //검색
    {
        path: '/search',
        name: '검색',
        component: Search,
        // beforeEnter: requireAuth()
    },
    {
        path: '/search/:keyword',
        name: '검색 결과',
        component: FeedSearchResultByKeyword,
        // beforeEnter: requireAuth()
    },
    
    {
        path: '*',
        redirect: '/404'
    },
    //홍주의 실험실...
    {
        path: '/lab2',
        name: '홍주랩실2',
        component: hongjuLab2
    },
    {
        path: '/fame',
        name: '명예의 전당',
        component: FeedOfFame,
        // beforeEnter: requireAuth()
    },
    {
        path: '/trend',
        name: '트렌드',
        component: FeedMain,
        // beforeEnter: requireAuth()
    }
]