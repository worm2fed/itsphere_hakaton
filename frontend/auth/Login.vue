™<template>
    <div class="">
        <top></top>
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
                      <el-button  @click="submit()" type="primary">Войти</el-button>
                    </el-form-item>
                  </el-form>
              </div>
          </el-col>
          <el-col :span="8">
              <div class="grid-content bg-purple">&nbsp;</div>
          </el-col>
        </el-row>
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
				error: ''
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
</style>

