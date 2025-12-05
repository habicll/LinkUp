import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import StatusView from '../views/StatusView.vue'
import LoginView from '../views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import StartView from '@/views/StartView.vue'
import DetailsView from '@/views/DetailsView.vue'
import { useAuthStore } from '@/stores/auth'
import AdminView from '@/views/adminView.vue'
import SignupCView from '@/views/SignupCView.vue'
import CompanieView from '@/views/CompanieView.vue'
import ProfilSeekerView from '@/views/ProfilSeekerView.vue'

import ChoiceView from '@/views/ChoiceView.vue'
import ProfileCompanyView from '@/views/ProfileCompanyView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: StartView,
    },
    {
      path: '/details',
      component: DetailsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/signup',
      component: SignupView,
    },
    {
      path: '/signupCompany',
      component: SignupCView,
    },
    {
      path: '/login',
      component: LoginView,
    },
    {
      path: '/home',
      component: HomeView,
      meta: { requiresAuth: true },

    },
    {
      path: '/status',
      component: StatusView,
      meta: { requiresAuth: true },
    },
    {
      path: '/companie',
      component: CompanieView,
      meta: { requiresAuth: true },
    },
    {
      path: '/choice',
      component: ChoiceView,
      meta: { requiresAuth: true },
    },
    {
      path: '/admin',
      component: StartView,
    },
    {
      path: '/profileCompany',
      component: ProfileCompanyView,
    },
    {
      path: '/profil',
      component: ProfilSeekerView,
    },
  ],
})

//verify if the auth is authendificated
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) next('/login')
  else next()
})

// check if it's the right type for the right acces to a page
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  const type = localStorage.getItem('type')

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next('/login')
  }
  else if (to.path === '/home' && type === 'company') {
    next('/companie')
  }
  else if (to.path === '/companie' && type === 'seeker') {
    next('/home')
  }
  else if (to.path === '/status' && type === 'company') {
    next('/choice')
  }  
  else if (to.path === '/profil' && type === 'company') {
    next('/profileCompany')
  }
  else {
    next()
  }
})



export default router