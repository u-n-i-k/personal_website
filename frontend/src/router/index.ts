import { createRouter, createWebHistory, RouterView } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PetProjectsView from '../views/PetProjectsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_BASE_URL),
  routes: [
    {
      path: "",
      component: RouterView,
      children: [
        {
          path: '',
          name: 'home',
          component: HomeView
        },
        {
          path: 'other',
          name: 'pet_projects',
          component: PetProjectsView
        }
      ]
    }
  ]
});

export default router