<template class="left">
<div>
  <div class="top">

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-default/index.css">
    <link href="https://fonts.googleapis.com/css?family=Didact+Gothic" rel="stylesheet">

    <nav class="top-nav">
      <router-link class="ele logo-wrap" :to="'/'" >
        <img class="logo" src="../assets/logo.png" alt="">

       ITSPHERE
      </router-link>
    </nav>

    <nav class="login-box">

      <router-link :to="'/add/'" v-if="auth.isAuth">
       <i class="fa fa-plus"></i>
      Добавить
      </router-link>


      <el-dropdown trigger="click" :hide-on-click="false">
        <span class="el-dropdown-link">

          <div v-if="!auth.isAuth">
              <vf-icon icon="user-circle-o" fixed/>
              присоединиться <i class="el-icon-caret-bottom el-icon--right"></i>
          </div>

          <div  v-if="auth.isAuth">
              <vf-icon v-if="!auth.user.avatar" icon="user-circle" fixed/>
              <img class="avatar" :src="auth.user.avatar" alt="">
              {{auth.user.username}} <i class="el-icon-caret-bottom el-icon--right"></i>
          </div>

        </span>
        <el-dropdown-menu slot="dropdown">
          <router-link :to="'/profile'">
              <el-dropdown-item divided v-if="auth.isAuth"  >
                  <div >
                    <i class="fa fa-gear"></i>{{ $t("profile.profile") }}
                  </div>
              </el-dropdown-item>
          </router-link>
          <router-link :to="'/login'" v-if="!auth.isAuth">
              <el-dropdown-item>
                  <vf-icon icon="sign-in" fixed/>
                  войти
              </el-dropdown-item>
              </router-link>
              <router-link :to="'/signup'" v-if="!auth.isAuth">
          <el-dropdown-item>

                <vf-icon icon="user-circle-o" fixed/>
               зарегистрироваться

          </el-dropdown-item>
          </router-link>


          <el-dropdown-item disabled>ICO</el-dropdown-item>
          <el-dropdown-item divided v-if="auth.isAuth">
              <div @click="logout()" >
                {{ $t("base.logout") }}
              </div>
          </el-dropdown-item>

        </el-dropdown-menu>
      </el-dropdown>
  <!--https://github.com/samturrell/vue-breadcrumbs -->

      <div class="">


      </div>
    </nav>
  </div>

</div>


</template>

<script>
import Vue from 'vue';
import auth from '../auth'

import {
    icon,
} from 'vue-fontawesome';
 export default {
   data() {
     return {
       auth: auth,
     }
   },
   methods: {
     logout() {
       auth.logout(this)
     },
     changeLocale() {
      Vue.config.lang == 'en' ? Vue.config.lang = 'ru' : Vue.config.lang = 'en'
      this.auth.user.locale=Vue.config.lang
     },
   },
   components: {
    'vf-icon': icon,

   },
   created() {
		this.auth.user=auth.user
   },
 }
</script>

<style lang="scss">
.el-dropdown {

    color: #ffffff;
}
.lang_switcher{
  display: inline-block;
  font-weight: bold;
  padding: 0px 10px
}
#app{
    padding-top: 2%;
}

.ele{
  border-radius: 15px;
  display: inline-block;

  padding: 5px 10px;
  text-align: center;
  margin-bottom: 5px;
  cursor: pointer;
  font-family: 'Helvetica','Verdana','Arial'
}
.el-dropdown{
    cursor: pointer;
}
.top{
  position: fixed;
  top: 0;
  display: table;
  z-index: 12;
  width: 100%;
  color: #f6f7f7;


  /* Permalink - use to edit and share this gradient: http://colorzilla.com/gradient-editor/#7abcff+0,60abf8+44,4096ee+100;Blue+3D+%2314 */
  background-color: #495565;
  border-bottom: #080808;
  padding: 8px 0px 5px 0px;

  .avatar{
    width: 25px;
    height: 25px;
    border-radius: 25px;
  }

  .login-box{
    display: inline-block;
    float: left;
    width: 25%;
    color: #fff;

  }
  .top-nav{
    display: inline-block;
    width: 75%;
    float: left;
    .ele{
      font-weight: normal;
    }
  }
}



.top .logo-wrap{
  padding: 1px 10px;
}
.top .ele b{

  vertical-align: middle;
}
.logo{
  width: 30px;
  height: auto;
  font-weight: normal;
  vertical-align: middle;
}


</style>
<style scoped>


  .el-dropdown {
    color: #fff;
  }
</style>
