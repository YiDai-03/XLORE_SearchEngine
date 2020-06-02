// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import VueRouter from 'vue-router'
Vue.use(VueRouter)
import panel from './components/search-panel'
import result from './components/result'
import ElementUI from 'element-ui';

import 'element-ui/lib/theme-chalk/index.css';
import vueResource from 'vue-resource'
import axios from 'axios'
Vue.prototype.$axios = axios

Vue.config.productionTip = false

Vue.use(vueResource)
Vue.use(ElementUI)

Vue.prototype.msg = function(msg){
    var msg2 = msg.replace(/\[\[(.+?)\|(.+?)\]\]/g,"<a style=\"text-decoration-line: none\" href=\"https://xlore.org/instance.html?url=http://xlore.org/instance/$1\">$2</a>")
    // var msg2 = msg.replace(/\[\[(.+?)\|(.+?)\]\]/g,"<el-link type=\"primary\">$2</el-link>")
　　return msg2
 }

 Vue.prototype.msg2 = function(msg){
    var msg2 = "<a style=\"text-decoration-line: none\" href=\"https://xlore.org/instance.html?url=" + msg["uri"] + "\">" + msg["名称"] + "</a>"
     // var msg2 = msg.replace(/\[\[(.+?)\|(.+?)\]\]/g,"<el-link type=\"primary\">$2</el-link>")
 　 return msg2
  }
  
 Vue.prototype.msg3 = function(msg){
     var msg3 = "<a class=\"el-icon-link\" style=\"text-decoration-line: none\" href=\"https://xlore.org/instance.html?url=" + msg+ "\"></a>"
      // var msg2 = msg.replace(/\[\[(.+?)\|(.+?)\]\]/g,"<el-link type=\"primary\">$2</el-link>")
  　 return msg3
  }

const routes = [
  {
    path: '/',
    name: 'panel',
    component: panel
  },
  {
    path: '/result',
    name: 'result',
    component: result
  }
]

const router = new VueRouter({routes})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  // template: '<App/>',
  // components: { App },
  router,
})
