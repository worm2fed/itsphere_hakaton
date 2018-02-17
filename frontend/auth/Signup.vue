<template>
  <div class="">
    <top></top>
    <el-row>
        <el-col :span="8">
            <div class="grid-content bg-purple">&nbsp;</div>
        </el-col>
        <el-col :span="8">
            <div class="grid-content bg-purple-light">
                <el-form ref="form"  label-width="120px">
                    <h2>Mapala.net Регистрация</h2>
                    <p v-if="errors">
											<i v-if="errors.username" class="el-icon-warning">{{ errors.username[0] }}</i>
											<i v-if="errors.email" class="el-icon-warning">{{ errors.email[0] }}</i>
                    </p>


                    <el-form-item label="Имя пользователя">
                        <el-input  placeholder="Введите имя пользователя" v-model="credentials.username"></el-input>
                    </el-form-item>
                    <el-form-item label="Пароль">
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
export default {
  name:'signup',
  data() {
    return {
      credentials: {
        username: '',
        password: ''
      },
      errors: []
    }
  },
  methods: {
    submit() {
      var credentials = {
        username: this.credentials.username,
        password: this.credentials.password
      }
			auth.signup(this, credentials, {name: 'base'})
    }
  },
  components:{
    'top':Top
  }
}
</script>
