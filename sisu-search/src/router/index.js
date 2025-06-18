import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ResultsView from '../views/ResultsView.vue'
import DetailView from '../views/DetailView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/results',
    name: 'results',
    component: ResultsView
  },
  {
    path: '/details/:id',
    name: 'details',
    component: DetailView,
    props: (route) => ({ 
      id: route.params.id,
      query: route.query.q 
    })
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
