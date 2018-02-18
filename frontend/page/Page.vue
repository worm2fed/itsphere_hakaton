  <template >
<div>
  <Top></Top>


  <div class="page_wrapper">
<!--     <Right v-if="!this.editor_mode"></Right> -->
    <!--
    <div class="blockchain"> {{page.blockchain}} </div>
    <div class="author"> {{page.author}} </div>
    <div class="created_at"> {{page.created_at}} </div>
    <div class="image"> {{page.image}} </div>
    <div class="miniature"> {{page.miniature}} </div>
    <div class="golos"> {{page.golos}} </div>
    <div class="permlink"> {{page.permlink}} </div>
    <div class="tags"> {{page.tags}} </div>
    <div class="updated_at"> {{page.updated_at}} </div>
    <div class="voters"> {{page.voters}} </div>
    -->
    <div class="page">

      <div v-if="editor_mode">

        <h1 class="edit_header">Добавление проекта</h1>
        <el-form
          :model="page"
          :rules="rules"
          ref="ruleForm"
          label-width="120px"
          class="demo-ruleForm">

          <el-form-item label="Название проекта" prop="title">
            <el-input v-model="page.title"></el-input>
          </el-form-item>
          <el-form-item label="Описание проекта" prop="body">
              <textarea v-on:keyup="mark_preview()" type="text" id="mark_edit" class="mark_edit" v-model="page.body"></textarea>
          </el-form-item>
          <el-form-item label="Категория">
           <!--  <el-input :value="page.master_tag" v-model="ruleForm.selected_master_tag"></el-input> -->
            <div class="block"  v-if="this.treeData">
             <!--  <el-cascader

              :disabled="!this.editor_mode"
                expand-trigger="hover"
                :options="this.treeData"
                :show-all-levels=false
                :clearable=false
				:props="{value: 'id', label: 'name'}"
                placeholder="Выберите категорию"
				v-model="master_tag_default">
              </el-cascader> -->
            </div>
          </el-form-item>

          <!--
		  <input type="file" @change="sync">
          <el-button @click="post_image()">Загрузить фото</el-button>
		  <br>
		  <br> -->

          <!--  <el-button type="text">Отмена</el-button> -->

           <el-upload
           action="/post_image/"
           type="drag"
           :drag="true"
           list-type="picture"
           :multiple="true"
           :on-remove="uploadRemove"
           :on-success="uploadSuccess"
		   :file-list="page.uploaded_images"
		   :headers="{'X-CSRFToken': $http.headers.common['X-CSRFToken']}"
           >
           <i class="el-icon-upload"></i>
           <div class="el-dragger__text">Переместите сюда фотографию <em>или нажмите загрузить</em></div>
           <div class="el-upload__tip" slot="tip">jpg/png files with a size less than 500kb</div>
           </el-upload>


          <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')">Опубликовать</el-button>
            <el-button @click="resetForm('ruleForm')">Очистить</el-button>
          </el-form-item>
        </el-form>
    </div>


      <h1 v-if="!this.editor_mode"> {{page.title}} </h1>
	  <img v-if="!this.editor_mode" :src="page.image">
      <div v-if="!editor_mode">{{page.position_text}}</div>
      <p v-if="error"><i class="el-icon-warning"></i>Ошибка {{error}}</p>

      <!-- Юзаем для поля ввода адреса
      https://github.com/gocanto/google-autocomplete
      Для времени
      https://github.com/egoist/vue-timeago -->
     <!--  <div style="color:blue;height: 2em">
          <transition name="fade">
              <div v-if="this.postdelay>0"> syncing...</div>
          </transition>
      </div> -->
      <div class="table">
        <div v-if="page_editable()">режим</div><br>
        <el-switch
          v-if="page_editable()"
          v-model="editor_mode"
          off-color="#ff4949" on-color="#13ce66"
          on-text="РЕДАКТОР"
          off-text="ПРОСМОТР "
          :width=120>
        </el-switch>
        <div>

        </div>
        <div>

        </div>

        <div>
          Теги<br>

		  <!-- TODO Зафиксить
          <el-tag v-if="!editor_mode" :key="tag" v-for="tag in page.tags">
            {{tag | remove_ru}}
          </el-tag>
          <div v-if="editor_mode">
		  -->

			<!--

            <el-tag
              :key="tag"
              v-for="tag in page.tags"
              :closable="true"
              :close-transition="false"
              @close="handleClose(tag)">
                {{tag}}
              </el-tag>
              <el-input
                class="input-new-tag"
                v-if="inputVisible"
                v-model="inputValue"
                ref="saveTagInput"
                size="mini"
                @keyup.enter.native="handleInputConfirm"
                @blur="handleInputConfirm"
              >
              </el-input>
              <el-button v-else class="button-new-tag" size="small" @click="showInput"> + добавить тег
              </el-button>

			  -->

			<el-select v-model="page.tags" multiple placeholder="Select">
				<el-option
				  v-for="tag in tags"
					:key="tag.id"
				  :label="tag.name"
				  :value="tag.id">
				</el-option>
			</el-select>

          </div>
        </div>

        <div v-if="!editor_mode">
          <el-popover
                ref="popover1"
                placement="top-start"
                title="Понравилось"
                width="200"
                trigger="hover"
                :content="this.page.voters | arrstr ">
          </el-popover>
          <el-button v-popover:popover1>
            поддержали:{{this.page.voters ? this.page.voters.length : null }}
          </el-button>
          <el-button  v-on:click="vote()">
            <i class="fa fa-heart "></i>
          </el-button>
        </div>


      </div>

        <article v-bind:class="{ mark_preview: this.editor_mode, page_view: !this.editor_mode  }" class="" v-html="mark_view">
        </article>


        <comments
					class="comments"
					v-for="comment in comments"
					:key="comment.id"
					:model="comment">
				</comments>

    </div>
  </div>
</div>



</template>

<script>
import Vue from 'vue'
import Top from '../base/Top.vue'
import Right from '../base/Right.vue'
import auth from '../auth'
import Comments from './Comments.vue'
import InputTag from 'vue-input-tag'
import {Page, MasterTag, Tag, Comment} from '../services/services'

Vue.filter('arrstr', function (arr) {
  var result = ''
  for (let i in arr) {
      result += arr[i] +', '
  }
  return result
})


  // WIKIMAPIA KE
  // http://api.wikimapia.org/?function=place.search&key=AEA2D008-A526DFAA-52530F99-C6113416-8CD3EC01-A43E3213-A2DBD696-64F1457C&q=Таганай
export default {
  name: 'Page',
  data () {
    return {
	  page: {},
	  tags: [],
		auth: auth,
		comments: [],
	  master_tag_default: [],
      editor_mode: false,
      new_page_mode:false,
      center: {lat: 0.0, lng: 0.0},
      markers:[],//JSON.parse(data.markers),
      mark_view:"",
      postdelay:null,
      error:false,
      //*INPUT TAG REFACTOR*//
      inputVisible: false,
      inputValue: '',
      treeData:[],
      /*FORM RULES*/
      ruleForm: {
          title: '',
          body: '',
          selected_master_tag:'',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          //position_text:'',
      },
      rules: {
        title: [
          { required: true, message: 'Пожалуйста, введите название', trigger: 'blur' },
          { min: 3, max: 255, message: 'Название от 3 to 255', trigger: 'blur' }
        ],
        // position_text: [
        //   { required: true, message: 'Пожайлуйста введиде адрес', trigger: 'blur' },
        //   { min: 3, max: 255, message: 'Название от 3 to 255', trigger: 'blur' }
        // ],
        body: [
          { required: true, message: 'Содержимое не может быть пустым', trigger: 'blur' }
        ],
        master_tag_default: [
          { required: true, message: 'Выберите основную категорию', trigger: 'blur' }
        ],


        // region: [
        //   { required: true, message: 'Please select Activity zone', trigger: 'change' }
        // ],
        // date1: [
        //   { type: 'date', required: true, message: 'Please pick a date', trigger: 'change' }
        // ],
        // date2: [
        //   { type: 'date', required: true, message: 'Please pick a time', trigger: 'change' }
        // ],
        // type: [
        //   { type: 'array', required: true, message: 'Please select at least one activity type', trigger: 'change' }
        // ],
        // resource: [
        //   { required: true, message: 'Please select activity resource', trigger: 'change' }
        // ],

      }
    }
  },
  components:{
      'Top':Top,
      'Right':Right,
      'input-tag':InputTag,
      'comments':Comments,
      //'gmap-map':GmapMap
  },
  methods:{
  	setMasterTag() {
  		let mtId = this.page.master_tag
  		MasterTag.ancestors({id: mtId}).then(res => {
  			this.master_tag_default = res.body
  			this.master_tag_default.push(mtId)
  		})
  	},

      uploadSuccess(image) {
        // console.log('suc',image)

     		this.page.images.push(image.id)
        this.insertAtCaret('mark_edit','![img](IMAGE_URL)'.replace('IMAGE_URL',image.url))

        var event = new Event('change');
        var text_input=document.querySelector('#mark_edit')
        text_input.dispatchEvent(event);
        this.page.body=text_input.value
        this.mark_preview()
        console.log('text_input',text_input)

      },
  	uploadRemove(image, ls) {
  		this.page.images = ls.map(i => {
  			if(i.id !== undefined) { return i.id }
  		})
  	},
    handleChange(value) {
        var x=value[value.length-1]
        this.page.master_tag=parseInt(x);
        this.ruleForm.selected_master_tag=x.toString();
    },
    mark_preview () {
      this.ruleForm.body=this.page.body
      this.mark_view=Vue.options.filters.markdown(this.page.body)
    },
    page_editable () {
      try{
		  return this.new_page_mode ? this.new_page_mode : this.page.author==auth.user.username // && this.page.status !== 2
        }
      catch (err){
        return this.new_page_mode
      }
    },

    initPage () {
      if (this.$route.path=="/add/"){
      //Если пришли на страницу добавления
        this.page={
          tags:[],
          status:0,
          position_text:'',
          selected_master_tag:[],
		  images: [],
        }
        this.mark_preview()
        this.editor_mode=true
        this.new_page_mode=true
        this.page.status=0
      } else {
					Page.get({permlink: this.$route.params.permlink}).then(res => {
						this.page = res.body

						Comment.get({page: this.page.id}).then(res => {
							this.comments = res.body
						})

						this.setPlace()
						this.setMasterTag()
						this.mark_preview()

					})
				}
    },
    savePage () {
      this.error = null;

	  var last_element = this.master_tag_default[this.master_tag_default.length - 1]
	  this.page.master_tag = last_element

	  // TODO Разделить добавление и обновление на 2 роута
	  if (this.$route.path=="/add/") {
		  Page.save({permlink: this.page.permlink}, this.page).then(res => {
			this.$message({type: 'success', message: 'сохранено'})
		  }).catch(res => {
			  this.error = data;
			  this.error.form = JSON.parse(data.form)
		  })
		} else {
			Page.update({permlink: this.page.permlink}, this.page).then(res => {
				this.$message({type: 'success', message: 'сохранено'})
			}).catch(res => {
			  this.error = data;
			  this.error.form = JSON.parse(data.form)
		  })
		}
    },

    publishPage() {
      this.page.status=1
      this.savePage()
    },
    vote () {
			let voter = this.page.voters.find(id => id == auth.user.id)

      if (auth.isAuth) {
				if(!voter) {
					// upvote
					this.page.voters.push(this.auth.user.id)
				} else {
					this.page.voters = this.page.voters.filter(id => id != auth.user.id)
				}

				Page.update({permlink: this.page.permlink}, this.page).then(res => {
					this.$message({type: 'success', message: 'голос принят'})
					}, res => {
            this.$message({type: 'error', message: 'like error'})
					})
				}
      else {
        this.$message({
            type: 'warning',
            message: 'для того чтобы голосовать, нужно сначала авторизоваться'
        })
      }
    },
	updatePlace(place) {

	},
    setPlace() {

    },
    getCoords(){



    },
    tagChanged(tags){
        this.page.tags=tags
    },
    getStatus(n) {
        var n=this.page.status //убрать протестить
        var dict={
            0:'набросок',
            1:'публикуется',
            2:'опубликовано'
        }
        return dict[n]
    },
    /*INPUT TAG*/
    handleClose(tag) {
      this.page.tags.splice(this.page.tags.indexOf(tag), 1);
    },
    showInput() {
      this.inputVisible = true;
      this.$nextTick(_ => {
        this.$refs.saveTagInput.$refs.input.focus();
      });
    },
    handleInputConfirm() {
      let inputValue = this.inputValue;
      if (inputValue) {
        this.page.tags.push(inputValue);
      }
      this.inputVisible = false;
      this.inputValue = '';
    },
    /*    ______
       / ____/___  _________ ___
      / /_  / __ \/ ___/ __ `__ \
     / __/ / /_/ / /  / / / / / /
    /_/    \____/_/  /_/ /_/ /_/
    methods*/
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          //this.page.title=this.ruleForm.title
          //this.page.body=this.ruleForm.body
          this.publishPage()
        } else {
          this.$message({
              type: 'error',
              message: `форма содержит ошибку`
          });
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    insertAtCaret(areaId, text) {
      var txtarea = document.getElementById(areaId);
      if (!txtarea) { return; }

      var scrollPos = txtarea.scrollTop;
      var strPos = 0;
      var br = ((txtarea.selectionStart || txtarea.selectionStart == '0') ?
        "ff" : (document.selection ? "ie" : false ) );
      if (br == "ie") {
        txtarea.focus();
        var range = document.selection.createRange();
        range.moveStart ('character', -txtarea.value.length);
        strPos = range.text.length;
      } else if (br == "ff") {
        strPos = txtarea.selectionStart;
      }

      var front = (txtarea.value).substring(0, strPos);
      var back = (txtarea.value).substring(strPos, txtarea.value.length);
      txtarea.value = front + text + back;
      strPos = strPos + text.length;
      if (br == "ie") {
        txtarea.focus();
        var ieRange = document.selection.createRange();
        ieRange.moveStart ('character', -txtarea.value.length);
        ieRange.moveStart ('character', strPos);
        ieRange.moveEnd ('character', 0);
        ieRange.select();
      } else if (br == "ff") {
        txtarea.selectionStart = strPos;
        txtarea.selectionEnd = strPos;
        txtarea.focus();
      }

      txtarea.scrollTop = scrollPos;
    },


  },
  watch: {
    mark_view : function () {
      var fu =(function(){
        this.postdelay=null;
      }).bind(this)
      if (this.postdelay==null){
         this.postdelay = setTimeout(fu,3000)
      }
      else{
        //console.log('just watching setting',this.postdelay)
        clearTimeout(this.postdelay)
        this.postdelay=null;
        this.postdelay = setTimeout(fu,3000)
      }
    },
    $route: function( ){
      this.initPage()
    }
  },
  created: function () {
    this.initPage();

	Tag.get().then(res => this.tags = res.body)
    MasterTag.tree().then(res => this.treeData = res.body)

  //Укажем вывбранный мастертег
  //this.page.selected_master_tag=[this.page.master_tag]


    // if (data.page) {

    //   // Если из джанги из шаблона при изначальном заходе пришли данные
    //   //this.page=data.page
    //   //delete(data)
    // }
    // else{

    // }

    // `this` points to the vm instance
    /*
    let position={}
    navigator.geolocation.getCurrentPosition(function(position) {
      // Get the coordinates of the current position.

      this.position={'lat':position.coords.latitude,'lng':position.coords.longitude}
      // position={'label':'YOU','position':{'lat':position.coords.latitude,'lng':position.coords.longitude} }
      position = {
          position:{'lat':position.coords.latitude,'lng':position.coords.longitude} ,
         statusText: "Hauptgebäude der ETH Zürich",
          draggable: true,

        }
      // this.markers=[]
      this.markers.push(position)
    }.bind(this));
    */
    //получим юзера
  },

  mounted()
  {
          //Set an event listener for 'setAddress'.
      // Vuemit.listen('setAddress', this.onAddressChanged);
  },
}
</script>


<style lang="scss">
body, h1 , h2 , h3 , p{
    font-family: 'Didact Gothic', sans-serif;
}
input{
  width: 100%;
  border-radius: 6px;
  height: 30px;
  border: 1px solid #cecece;
  padding-left: 10px;
  font-size: 18px;
}

.vue-map-container {

    left: 0;
    top: 0;
    z-index: 0;
    width:  100%;
    height:250px;
}
.vue-street-view-pano-container{
    width: 100%;
    height: 300px;
}
.gmnoprint{

}
/*Настройки редактора*/
p{
  clear: both;
  font-size: 18px;
}
.vue-input-tag-wrapper.read-only {
    border: none;
}

.page_wrapper{

  position: relative;
 width: 80%;
 margin: auto;
  aside > li {
      margin-top: -240px!important;
  }
}
.page{
  display: block;
  box-sizing: border-box;
  box-sizing: border-box;
  width: 100%;
  .fa-plus{
    cursor: pointer;
  }
    .page_title_input, .txtAutocomplete{
        width: 100%;
    }
    .fa-heart{
        cursor: pointer;
        &:hover{
            text-shadow: 0px 0px 10px  rgba(0,0,0,0.9);
        }
    }
  .el-switch {
      z-index: 0;
  }
  img{
    width: 100%;
    max-width: 100%;
    height: auto;
  }
  .edit_header{
      background-color: #36d7b7;
      color: #fff;

      display: block;
      width: 100%;
      height: 1.5em;
      padding-left: 20px;
      text-shadow: 1px 1px 1px rgba(0,0,0,0.4);
      box-sizing: border-box;
  }
  .page_editor{
    width: 50%;
    display: inline-block;
    float: left;

  }
  .mark_edit{
    margin: 0px;
    width: 100%;
    display: inline-block;
    float: left;
    height: 500px;
    padding: 10px;
    box-sizing: border-box;
    background: url(http://i.stack.imgur.com/ynxjD.png) repeat-y;
    line-height: 25px;
    padding: 2px 10px;
    border: solid 1px #ddd;

  }
  .mark_preview{
    display: inline-block;
    box-sizing: border-box;
    float: left;
    margin: 0px;
    width: 49%;
    padding: 10px;
    img{
      box-sizing: border-box;
      padding: 10px;
      width: 100%;
    }
    .page_view{
      width: 100%;
    }
  }
  .is-disabled .el-icon-caret-bottom{
    display: none;
  }
  .el-input.is-disabled .el-input__inner{
    background: none;
    border: none;
  }
}


/*TRANSITIONS*/
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0
}

</style>
