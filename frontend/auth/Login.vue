™<template>
    <div >
        <top></top>
        <div class="content-wrap">
        <el-row>
          <el-col :span="8">
              <div class="grid-content bg-purple">&nbsp;</div>
          </el-col>
          <el-col :span="8">
              <div class="grid-content bg-purple-light">
                  <el-form ref="form"  label-width="120px">
                  <h2>{{$t('base.sitename')}} Вход</h2>
                  <p v-if="error"> <i class="el-icon-warning"></i> Неправильный логин или пароль</p>
                    <el-form-item v-bind:label="$t('profile.username')">
                      <el-input  placeholder="Введите имя пользователя" v-model="credentials.username"></el-input>
                    </el-form-item>
                    <el-form-item  v-bind:label="$t('base.password')">
                     <el-input type="password" placeholder="Введите пароль"  v-model="credentials.password"></el-input>
                    </el-form-item>
                    <el-form-item >
                      <el-button  v-on:keyup.enter="submit()"  @click="submit()" type="primary">Войти</el-button>
                    </el-form-item>
                  </el-form>

                  <div v-if="errors && errors.hasOwnProperty('username')"  >
                   Неправильное имя пользователя

                  </div>
                  <div v-if="errors && errors.hasOwnProperty('password')"  >
                   Неправильный пароль

                  </div>

                  <div v-if="errors && errors.hasOwnProperty(' non_field_errors')"  >
                   Неправильный пароль или имя пользователя

                  </div>


              </div>
          </el-col>
          <el-col :span="8">
              <div class="grid-content bg-purple">&nbsp;</div>
          </el-col>
        </el-row>
        </div>
    </div>
</template>

<script>
import auth from '../auth'
import Top from '../base/Top.vue'
import { router } from '../main'

export default {
	data () {
			return {
				auth: auth,
				credentials: {
					username: '',
					password: ''
				},
				errors: ''
			}
	},
		methods: {
			submit () {
				let credentials = {
					username: this.credentials.username,
					password: this.credentials.password
				}

				auth.login(this, credentials, {name: 'base'})

			}
		},
		components: {
			'top': Top
		}
}
</script>
<style lang="scss">
    .el-form h2{
        text-align: center;
    }
    .el-button--primary{
        background-color: #36d7b7!important;
        color: #fff;
        box-shadow: 1px 1px 1px rgba(0,0,0,0.4);
    }
</style>

