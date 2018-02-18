<template >
<div>
  <Top></Top>
    <div class="profile">
        <el-row>

            <el-col :span="8">
                <div class="grid-content bg-purple">&nbsp;</div>
            </el-col>
            <el-col :span="8">
                <div class="grid-content bg-purple-light">
                    <el-form ref="form"  label-width="120px">
                        <h1> {{ $t("profile.profile") }}</h1>
                        <p v-if="error"><i class="el-icon-warning"></i>Ошибка</p>
                        <el-form-item v-bind:label="$t('profile.username')">
                            <el-input v-model="auth.user.username"></el-input>
                        </el-form-item>
                        <el-form-item v-bind:label="$t('base.password')">
                            <el-input disabled v-model="auth.user.password"></el-input>
                        </el-form-item>
                       <!--  <el-form-item label="Ключ постинга golos.io">
                            <el-input v-model="auth.user.posting_key" placeholder="<SECRET>"></el-input>
                        </el-form-item> -->


                       <!--  <my-upload field="file"
                            @crop-success="cropSuccess"
                            @crop-upload-success="cropUploadSuccess"
                            @crop-upload-fail="cropUploadFail"
                            v-model="show"
                            :width="300"
                            :height="300"
                            url="/api/users/b14ckb0x/set_avatar/"
                            :params="params"
                            :headers="headers"
                            img-format="png">
                        </my-upload> -->


                        <img class="avatar" :src="auth.user.avatar">

                        <div class="avatar-label" v-if="!auth.user.avatar">
                            Загрузите аватар
                        </div>
                        <div class="avatar-label" v-if="auth.user.avatar">
                            Обновите аватар
                        </div>
                        <input type="file" @change="onFileChange">



                        <el-form-item >
                            <el-button  @click="save()" type="primary"> Сохранить </el-button>
                        </el-form-item>

                    </el-form>
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
//import 'babel-polyfill'; // es6 shim
import Vue from 'vue'
// import myUpload from 'vue-image-crop-upload/upload-2.vue';

import Top from '../base/Top.vue'
import auth from '../auth'
import {User} from '../services/services'
import {Avatar} from '../services/services'




export default {
    name: 'Profile',
    data () {
        return {
            error: false,
            auth: auth,
            show: true,
            avatar_file:null,
            image:null,
            params: {
                token: '123456798',
                name: 'avatar'
            },
            headers: {
                smail: '*_~'
            },
            imgDataUrl: '' // the datebase64 url of created image
        }
    },
    components:{
        'Top':Top,
        // 'my-upload': myUpload
    },

    methods:{
      save() {
		User.update({id: this.auth.user.id}, this.auth.user).then(res => {
		  this.auth.user = res.body
            this.$message({
            type: 'info',
                message: `Профиль обновлен`
            })
		}, res => {
			this.error = res.data.error;
			this.$message({
			type: 'error',
		    message: 'неправильный ключ'
			});
		})
      },

      saveAvatar(file) {
        var formData = new FormData();
        formData.append('file', file);
        Avatar.post({id: this.auth.user.id}, formData ).then(res => {
        console.log('RES OK',res)
          auth.user.avatar = res.body
            this.$message({
            type: 'info',
                message: `Аватар обновлен`
            })
        }, res => {
            this.error = res.data.error;
            this.$message({
            type: 'error',
            message: 'Что то пошло не так'
            });
        })
      },



    onFileChange(e) {
        var files = e.target.files || e.dataTransfer.files;
        if (!files.length)
          return;
        this.createImage(files[0]);
    },
    createImage(file) {
        var image = new Image();
        var reader = new FileReader();
        var vm = this;
        reader.onload = (e) => {
          vm.image = e.target.result;
        };
        reader.readAsDataURL(file);

        this.saveAvatar(file)
    },
    removeImage: function (e) {
    this.image = '';
    },



      toggleShow() {
          this.show = !this.show;
      },
      /**
       * crop success
       *
       * [param] imgDataUrl
       * [param] field
       */
      cropSuccess(imgDataUrl, field){
          console.log('-------- crop success --------');
          this.imgDataUrl = imgDataUrl;
      },
      /**
       * upload success
       *
       * [param] jsonData  server api return data, already json encode
       * [param] field
       */
      cropUploadSuccess(jsonData, field){
          console.log('-------- upload success --------');
          console.log(jsonData);
          console.log('field: ' + field);
      },
      /**
       * upload fail
       *
       * [param] status    server api return error status, like 500
       * [param] field
       */
      cropUploadFail(status, field){
          console.log('-------- upload fail --------');
          console.log(status);
          console.log('field: ' + field);
      }
    },
}
</script>
<style  lang="scss">
.profile{
    .avatar-label{
        text-align: center;
    }
    .avatar{
        width: 400px;
        height: 400px;
        display: block;
        margin: 50px auto;
        border-radius: 100%;
        box-shadow: 1px 1px 33px rgba(0,0,0,0.2);
    }
}


</style>
