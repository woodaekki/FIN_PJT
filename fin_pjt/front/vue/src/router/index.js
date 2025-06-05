import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/components/HomeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import ArticleView from '@/views/ArticleView.vue'
import ArticleNotice from '@/views/ArticleNotice.vue'
import ArticleCreateView from '@/views/ArticleCreateView.vue'
import ArticleDetailView from '@/views/ArticleDetailView.vue'
import ArticleEditView from '@/views/ArticleEditView.vue'
import MapView from '@/components/MapView.vue'
import GoldAndSilverView from '@/views/GoldAndSilverView.vue'
import ChatbotView from '@/components/ChatbotView.vue'
import ProductList from '@/components/ProductList.vue'
import ProductRecommend from '@/components/ProductRecommend.vue'
import ProductDetail from '@/components/ProductDetail.vue'
import UserProfileView from '@/views/UserProfileView.vue'
import FinalUserProfile from '@/views/FinalUserProfile.vue'
import UserProfileEdit from '@/views/UserProfileEdit.vue'

import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/login', name: 'login', component: LogInView },
  { path: '/signup', name: 'signup', component: SignUpView },
  { path: '/article', name: 'article', component: ArticleView },
  { path: '/articles/:id', name: 'detail', component: ArticleDetailView },
  { path: '/create', name: 'create', component: ArticleCreateView },
  { path: '/articles/:id/edit', name: 'edit', component: ArticleEditView },
  { path: '/gold_and_silver', name: 'gold_and_silver', component: GoldAndSilverView },
  { path: '/userprofile', name: 'userprofile', component: UserProfileView },
  { path: '/userprofile_edit', name: 'userprofile_edit', component: UserProfileEdit },
  { path: '/userprofile/:id', name: 'final-userprofile', component: FinalUserProfile },
  { path: '/product', name: 'product', component: ProductList },
  { path: '/product-detail/:type/:id', name: 'product-detail', component: ProductDetail, props: true },
  { path: '/map', name: 'map', component: MapView },
  { path: '/chatbot', name: 'chatbot', component: ChatbotView },
  { path: '/recommend', name: 'recommend', component: ProductRecommend },
  { path: '/notice/:id', name: 'notice', component: ArticleNotice}
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// 네비게이션 가드로 서비스 이용 시 회원정보 페이지가 필수적으로 입력되도록 확인
router.beforeEach(function (to, from, next) {
  const accountStore = useAccountStore()

  if (to.name === 'login') {
    next()
    return
  }

  if (to.name === 'signup') {
    next()
    return
  }

  if (to.name === 'userprofile') {
    next()
    return
  }

  // 로그인 안 했으면 로그인으로 보냄
  if (accountStore.isLogin !== true) {
    alert('로그인이 필요합니다.')
    next({ name: 'login' })
    return
  }

  // 로그인 했으면, 프로필 확인 요청 보냄
  axios.get('http://127.0.0.1:8000/api/v1/profile/my_profile/', {
    headers: {
      Authorization: 'Token ' + accountStore.token
    }
  })
    .then(function (response) {
      const profile = response.data

      // 하나라도 비어 있으면 프로필 작성 페이지로 보냄
      if (profile.nickname === null) {
        alert('프로필을 먼저 작성해주세요.')
        next({ name: 'userprofile' })
        return
      }

      if (profile.nickname === '') {
        alert('프로필을 먼저 작성해주세요.')
        next({ name: 'userprofile' })
        return
      }

      if (profile.email === null) {
        alert('프로필을 먼저 작성해주세요.')
        next({ name: 'userprofile' })
        return
      }

      if (profile.email === '') {
        alert('프로필을 먼저 작성해주세요.')
        next({ name: 'userprofile' })
        return
      }

      if (profile.user === null) {
        alert('프로필을 먼저 작성해주세요.')
        next({ name: 'userprofile' })
        return
      }

      if (profile.user === '') {
        alert('프로필을 먼저 작성해주세요.')
        next({ name: 'userprofile' })
        return
      }

      next()
    })
    .catch(function (error) {
      if (error.response && error.response.status === 404) {
        alert('프로필을 먼저 작성해주세요.')
        next({ name: 'userprofile' })
        return
      }

      alert('프로필을 확인하는 중 오류가 발생했습니다.')
      console.log(error)
      next(false)
    })
})

export default router
