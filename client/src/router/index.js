import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/components/Home';
import Follow from '@/components/Follow';
import Tag from '@/components/Tag';
import Group from '@/components/Group';
import Login from '@/components/Login';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login,
    },
    {
      path: '/home',
      name: 'Home',
      component: Home,
    },
    {
      path: '/follow',
      name: 'Follow',
      component: Follow,
    },
    {
      path: '/tag',
      name: 'Tag',
      component: Tag,
    },
    {
      path: '/group',
      name: 'Group',
      component: Group,
    },
  ],
  mode: 'history',
});
