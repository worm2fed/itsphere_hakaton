import Vue from 'vue'
import auth from './auth'
import VueRouter from 'vue-router'
import Signup from './auth/Signup.vue'
import Login from './auth/Login.vue'
import Profile from './base/Profile.vue'
import Page from './page/Page.vue'
import PageList from './page/PageList.vue'
import ElementUI from 'element-ui'
import VueCookie from 'vue-cookie'
import VueResource from 'vue-resource'
import VueLazyload from 'vue-lazyload'
import * as VueGoogleMaps from 'vue2-google-maps'
import showdown from 'showdown'

Vue.use(VueRouter)
Vue.use(ElementUI)
Vue.use(VueCookie)
Vue.use(VueResource)
Vue.use(VueLazyload)

Vue.use(VueLazyload, {
  preLoad: 1.3,
  error: 'dist/error.png',
  loading: 'dist/loading.gif',
  attempt: 1
})

Vue.use(VueGoogleMaps, {
	load: {
		key: 'AIzaSyBUggg4I6FWB6sHijJGpXvBDdoZKqi1J7Y',
		libraries: 'places',
	}
});

const NotFound = { template: '<p>Page not found</p>' }
const About = { template: '<p>about page</p>' }

Vue.http.interceptors.push((request, next) => {
	// Добавить хедер авторизации при наличии токена
	let jwt_header = auth.getAuthToken()

	if (jwt_header) {
		request.headers.set('Authorization', jwt_header)
	}

	next()
})

auth.checkAuth()

Vue.http.headers.common['X-CSRFToken'] = VueCookie.get('csrftoken')
Vue.http.headers.common['Access-Control-Allow-Origin'] = 'http://data-asg.goldprice.org'

window.bind = function(func, context) {
  return function() { // (*)
    return func.apply(context, arguments);
  };
}

var converter = new showdown.Converter({
  simplifiedAutoLink: true,
  tables: true
})

Vue.filter('markdown', function (str) {
  return converter.makeHtml(str)
})

var transliterate = (
  function() {
    var
      rus = "щ    ш  ч  ц  й  ё  э  ю  я  х  ж  а б в г д е з и к л м н о п р с т у ф ъ  ы ь".split(/ +/g),
      eng = "shch sh ch cz ij yo ye yu ya kh zh a b v g d e z i k l m n o p r s t u f xx y x".split(/ +/g)
    ;
    return function(text, engToRus) {
      var x;
      for(x = 0; x < rus.length; x++) {
        text = text.split(engToRus ? eng[x] : rus[x]).join(engToRus ? rus[x] : eng[x]);
        text = text.split(engToRus ? eng[x].toUpperCase() : rus[x].toUpperCase()).join(engToRus ? rus[x].toUpperCase() : eng[x].toUpperCase());
      }
      return text;
    }
  }
)()
Vue.filter('latCyr', function (str) {
  var result= transliterate(str,true)
  return result
})
Vue.filter('remove_ru', function (str) {
  if (str.indexOf("ru--") > -1){
    var result=Vue.options.filters.latCyr(str.replace('ru--',''))
    return result
  }
  else {//просто вернем как есть
    return str
  }
})

import moment from 'moment'
// console.log('moment locale',moment.locale())
moment.locale(Vue.cookie.get('locale') || "ru")
// console.log('locale cookie',)

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).fromNow()
  }
})





/*Multilanguage
http://kazupon.github.io/vue-i18n/started.html
Из за бага юзаем пониженную версию in package.json "vue-i18n": "^5.0.3"
The error goes away if I manually force in package.json "vue-i18n": "^5.0.3"
*/

var VueI18n = require('vue-i18n')
import locales from './locales'
// install plugin
Vue.use(VueI18n)
// set lang
Vue.config.lang =  VueCookie.get('locale') ? VueCookie.get('locale') : 'ru'

// set locales
Object.keys(locales).forEach(function (lang) {
  Vue.locale(lang, locales[lang])
})









const routes = [
  {
    path: '/login',
    component: Login,
    beforeEnter: (to, from, next) => {
        if (auth.user.authenticated){
            next('/')
        }
        else{
            next()
        }
    }
  },
  {
    path: '/signup',
    component: Signup,
    beforeEnter: (to, from, next) => {
      //переписать!
        if (auth.user.authenticated){
            next('/')
        }
        else{
            next()
        }
    }

  },
  {
    path: '/profile',
    component: Profile,
    beforeEnter: (to, from, next) => {
      //переписать!
        if (!auth.user.authenticated){
           next()
        }
        else{
           next('/')
        }
    },
    meta: { requiresAuth: true },

  },

  // { path: '/', component: PageList },

  {
    path: '/add/',
		name: 'add',
    component: Page,
    beforeEnter: (to, from, next) => {
      //переписать!
        if (!auth.user.authenticated){
           next()
        }
        else{
           next('/')
        }
    },
    meta: {
      //requiresAuth: true,
      //requiresPostingKey: true
    },
  },
  {
    path: '/',
    component: PageList,
		name: 'base'
  },
  {
    path: '/cat:cat(\[a-zA-Zа-яА-Я0-9\%-_/\]+)',
    component: PageList,
    name:'category'
  },
  {
    //path: '/:url(\[a-zA-Zа-яА-Я0-9\%-_/\]+/\[a-zA-Zа-яА-Я0-9\%-_/\]+)',
	path: '/:user/:permlink',
	name: 'page',
    component: Page,
  },
  {
    path: '/:author/',
		name: 'myBlog',
    component: PageList
  },

  { path: '*', component: NotFound}

]


Vue.http.options.root = '/api/v1';

export const router = new VueRouter({
  routes, // short for routes: routes
  // mode: 'history',
  hashbang: false,
  linkActiveClass: 'active',
  mode: 'history',
  base: __dirname,
})


router.beforeEach((to, from, next) => {
  //Первой идет проверка на то требователен ли url к наличию постинг ключа

 if (to.matched.some(record => record.meta.requiresPostingKey)) {
    if (auth.user.has_posting_key==true){
      next()
    } else {
		alert('Для публикации требуется Private posting key golos.io')
			next('/profile')
		}
  }

  //Второй идет проверка на то требователен ли url к наличию авторизации
  else if (to.matched.some(record => record.meta.requiresAuth)) {
		if (auth.isAuth) {
			next()
		} else {
			next({
				path: '/login',
				query: { redirect: to.fullPath }
			})
		}
  }

  //В любом случае вызывем продолжение навигации
  else {
    next() // make sure to always call next()!
  }

})


const app = new Vue({
  router,
  data: {},
}).$mount('#app')
