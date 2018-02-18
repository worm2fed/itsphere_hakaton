<template class="left">
<div>
  <div class="top">

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-default/index.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/element-ui/2.2.0/theme-chalk/index.css">

    <link href="https://fonts.googleapis.com/css?family=Didact+Gothic" rel="stylesheet">

    <nav class="top-nav">
      <router-link class="ele logo-wrap" :to="'/'" >
        <img class="logo" src="../assets/logo.png" alt="">

       ITSPHERE v0.7beta
      </router-link>
      <a href="https://golos.io/@itsphere"><div class="goloslink">Мы на Голосе</div></a>
      <div class="description">Приложение по подбору специалистов для реализации IT проектов</div>
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


  <div v-if="categories && categories.length>0" class="categories">
    <div class="link" v-for="cat in categories" >
      <router-link  :to="{ name: 'category', params: { cat: cat.id }} ">
          {{cat.name}}
      </router-link>
    </div>

  </div>

  </div>

</div>


</template>

<script>
import Vue from 'vue';
import auth from '../auth'

import {Category} from '../services/services';

import {
    icon,
} from 'vue-fontawesome';
 export default {
   data() {
     return {
       auth: auth,
       categories:[],
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
    Category.get().then(res => {
      this.categories = res.body
    })

   },
 }
</script>



<style>
  .el-form-item__label{
    padding: 7px!important;
    line-height: 1em!important;
  }

</style>
<style lang="scss">

.categories{
  background-color:#36d7b7;
  display: inline-block;
  width: 100%;
  .link {
    display: inline-block;
    color: #fff;
    margin-left: 10px;
    a {
      color: #fff;
      text-decoration:none;
      &:hover{
        color: #000;
      }
    }
  }

}

.goloslink {
  display: inline-block;
  background: #36d7b7;
  padding: 1%;
}
.description {
  display: block;
  margin-left: 4%;
  margin-bottom: 1%;
}
.el-dropdown {

    color: #ffffff;
}
.lang_switcher{
  display: inline-block;
  font-weight: bold;
  padding: 0px 10px
}
#app{
    padding-top: 10%;

}
.content-wrap{
    width: 80%;
    display: block;
    margin: auto;
}

h2{
    background-color: #36d7b7;
    color: #fff;

    display: block;
    width: 100%;
    height: 1.5em;
    padding-left: 20px;
    text-shadow: 1px 1px 1px rgba(0,0,0,0.4);
    box-sizing: border-box;
}

.ele{
  border-radius: 15px;
  display: inline-block;

  padding: 5px 10px;
  text-align: center;
  margin-bottom: 5px;
  cursor: pointer;
    text-decoration: none;
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
  color: #fff;

  /* Permalink - use to edit and share this gradient: http://colorzilla.com/gradient-editor/#7abcff+0,60abf8+44,4096ee+100;Blue+3D+%2314 */
  background-color: #000;
  border-bottom: #080808;
  padding: 8px 0px 5px 0px;

  .avatar{
    width: 25px;
    height: 25px;
    border-radius: 25px;
  }

  .login-box{
    display: table;
    float: left;
    width: 25%;
    color: #fff;
    margin-top: 1em;

    a {
        display: table-cell;
        color: #fff;
        text-decoration: none;
    }

  }
  .top-nav{
    display: inline-block;
    width: 75%;
    float: left;
    a{
        color: #fff;
        text-decoration: none;
    }
    .ele{
      font-weight: normal;
    }
  }
}



.top .logo-wrap{
  padding: 1px 10px;
  font-size: 25px;
}
.top .ele b{

  vertical-align: middle;
}
.logo{
  width: 50px;
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
