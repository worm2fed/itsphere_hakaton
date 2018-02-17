<!-- <style src="vue2-animate/dist/vue2-animate.min.css"></style>
 --><template>
  <div id="app" >
  <div class="search-box">
   <el-autocomplete
     v-model="state4"
     :fetch-suggestions="querySearchAsync"
     placeholder="Search"
     resize="both"
     @select="handleSelect"
   ></el-autocomplete>

  </div>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.5.2/animate.min.css"><!--TODO move to local buildin stylesheet-->
    <Top></Top>




    <div class="wrapper">
      <div class="page-list">
        <div v-if="loading" class="loader">
          <i class="el-icon-loading"></i>
        </div>
        <!-- <transition-group name="fade" tag="ul"> -->
        <div>

        <div v-if="this.author" class="profile">
          <img :src="author.avatar" alt="" class="author_avatar">
          <div class="username">
            @{{author.username}}
          </div>
          <div v-if="self_blog_view==true" class="self_blog_view_buttons">
            <div class="half">
              <i class="fa fa-bitcoin"></i> Кошелек
            </div>
            <div class="half">

              <router-link :to="'/profile'">
                  <div v-if="auth.isAuth"  >
                      <div >
                       <i class="fa fa-gear"></i>  Настройки
                      </div>
                  </div>
              </router-link>



            </div>
          </div>

        </div>

          <div v-if="pages.length==0">...</div>
          <div  class="article animated" v-for="page in pages" :id="'page_id_'+ page.id" v-bind:key="page">
            <div>
              <img class="post-image" :src="getFirstImage(page.body)" alt="">
            </div>
            <img :src="page.miniature"/>

            <div class="post-preview">
              <div class="post-info">
              <div class="avatar">
                <img :src="page.author_ava" alt="" >

              </div>

                  <div class="head">
                    <router-link :to=" '/'+ page.author"> {{page.author}}</router-link>  <i class="fa fa-map-marker" v-if="page.position_text"> {{page.position_text}}</i>
                    <br/>
                    <i class="fa fa-date" ></i>{{page.created_at || page.updated_at | formatDate}}
                    <br/>
                  </div>
              </div>


              <div class="bottom">
              <div class="full">
                <router-link :to="{name: 'page', params: {user: page.author, permlink: page.permlink} }">
                  <h2>{{page.title}}</h2>
                  <span>
                    {{page.body.replace(/<\/?[^>]+(>|$)/g, "")}}
                  </span>
                </router-link>
              </div>

                <div class="comments one-fourth">
                  <i class="fa fa-comment-o"></i>&nbsp;{{page.comments.length}}&nbsp;{{page.comments.length | sayCommentsLength}}
                </div>
                <div class="comments one-fourth">

                  <a v-on:click="share('vkontakte',getPageUrl(page), page.title,'IMG_PATH', 'page.body Mapala.net Everyone can travel'  )"> <i class="fa fa-share"></i> Рассказать</a>
                  Поддержало {{page.voters.length}}
                </div>
                <div class="half">
                  <div class="button" v-on:click="vote(page)">
                    <i class="fa fa-dot-circle-o"></i>
                    <span>Поддержать</span> | <i class="fa fa-rub"></i> {{page.total_pending_payout_value}}
                  </div>
                </div>

              </div>



            </div>


            <!-- <div class="dummy-image" v-lazy:background-image="imgObj"></div> -->
            <div class="content">

              <!-- <i class="fa fa-tags" aria-hidden="true"></i> <el-tag v-for="tag in page.tags" type="primary"> <router-link :to="'/tag/'+tag">{{tag | remove_ru }}</router-link></el-tag> -->




              <div class="stat">
               <!-- {{$t('page.upvoters')}}  -->
                <div ></div>
              </div>
              <!-- <div class="voters">
                <div class="voter" v-for="voter in page.voters" >
                    <div v-on:click="navigate(voter.username)">
                     {{voter.username}}
                    </div>
                </div>
              </div> -->

            </div>
          </div>
        </div>

      </div>
			<!-- TODO Разобрать что должен делать -->
      <Right></Right>
    </div>
    <mugen-scroll tag="mu" :handler="fetchPage" :should-handle="!loading">
      &nbsp;
    </mugen-scroll>
    </div>
</template>
<script>
import Vue from 'vue'
import auth from '../auth'
import Top from '../base/Top.vue'
import Right from '../base/Right.vue'
import InputTag from 'vue-input-tag'
import finance from '../services/finance'
import MugenScroll from 'vue-mugen-scroll'
import {Page} from '../services/services'
import {User} from '../services/services'
var VueScrollTo = require('vue-scrollto');
Vue.use(VueScrollTo)



Vue.filter('sayCommentsLength', function(value) {

    if (value==0){
      return 'Комментарев'
    }
    else if (value==1){
      return 'Комментарий'
    }
    else if (value==2){
      return 'Комментария'
    }
    else if (value==5){
      return 'Комментариев'
    }
    return "XXX  ---"
})


export default {
  name: 'PageList',
  data () {
    return {
      center: {
        lat: 10.0,
        lng: 10.20
      },
      position: {},
      author:null,
      blog_view:false,
      self_blog_view:false,
      my_zoom_size:5,
      markers:null,
      bounds:null,
      markers_loaded:false,
      user_marker:{
        lat: 10.0,
        lng: 0.0
      },
      auth: auth,
     // markers:[],
      // currency_sbd:finance.currency.sbd,
      pages: [],
      nex_page: 1,
      currency_sbd:null,
      loading: true,
      imgObj: {
        src: '/static/dist/logo.png',
        error: '/static/dist/logo.png',
        loading: '/static/dist/logo.png'
      },
      state4:''
    }
  },
  components: {
    'Top': Top,
    'Right': Right,
    'input-tag': InputTag,
    'mugen-scroll': MugenScroll,
    'VueScrollTo':VueScrollTo,
  },

  methods: {
    share(network_name, purl, ptitle, pimg, text){

    if (network_name=="vkontakte"){
      var vkontakte=function(purl, ptitle, pimg, text) {
        var url  = 'http://vkontakte.ru/share.php?';
        url += 'url='          + encodeURIComponent(purl);
        url += '&title='       + encodeURIComponent(ptitle);
        url += '&description=' + encodeURIComponent(text);
        url += '&image='       + encodeURIComponent(pimg);
        url += '&noparse=true';
        window.open(url,'','toolbar=0,status=0,width=626,height=436');
      }
      vkontakte(purl, ptitle, pimg, text)
    }



    },


    navigate:function(voter){
      this.$router.push('/'+voter)
    },


    fetchPage () {
			this.loading = true

			let params = {}
			params.papage = this.nex_page
			if (!this.nex_page) { return }
			// Если на транице пользователя
			let author = this.$route.params.author
			if (author) {
        params.author__username = author
        this.blog_view=true
        if(this.$route.params.author==auth.user.username){
          this.self_blog_view=true;
        }
        else{
          this.self_blog_view=false;
        }
        var result=User.get({username:author}).then(res => {
           //console.log(username,'-->', res.body[0].avatar)
           var profile=res.body[0]
           //console.log('------> got:',ava)
           this.author=profile
        })

      }
      else{
        this.blog_view=false
      }
			Page.get(params).then(res => {
                this.pages = this.pages.concat(res.body.results)
        		this.loading = false
        		this.nex_page = res.body.next
			})
    },
    getPageUrl(page){
      return('http://'+window.location.hostname+'/'+page.author+'/'+page.permlink)
    },
    getFirstImage(body){
      try{
        var m,
            urls = [],
            //str = '<img src="http://site.org/one.jpg />\n <img src="http://site.org/two.jpg />',
            rex = /<img[^>]+src="?([^"\s]+)"?\s*\/>/g;
            //res='/\b(https?:\/\/\S*?\.(?:png|jpe?g|gif)(?:\?(?:(?:(?:[\w_-]+=[\w_-]+)(?:&[\w_-]+=[\w_-]+)*)|(?:[\w_-]+)))?)\b/'
        while ( m = rex.exec( body ) ) {
            urls.push( m[1] );
        }
        // console.log('URL_________>', urls );
          if (urls.length>0){
            return urls[0]
          }
          //var res = body.match(reg)
          //console.log('res',res)
      }
      catch(err){

      }
      return 'https://s13.postimg.org/ror54hqyv/logo-small.png'
    },
    getAvatar(page){
    var username= page.author
      var result=User.get({username:username}).then(res => {
         //console.log(username,'-->', res.body[0].avatar)
         var ava=res.body[0].avatar
         page.author_ava=ava
         console.log('ava',ava,page)
         page.avatar=ava
         return ava
      })

    },

    vote (page) {
      let voter = page.voters.find(id => id == auth.user.id)

      if (auth.isAuth) {
        if(!voter) {
          // upvote
          page.voters.push(this.auth.user.id)
        } else {
          page.voters = page.voters.filter(id => id != auth.user.id)
        }

        Page.update({permlink: page.permlink}, page).then(res => {
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


    scrollTo(page_id) {
      //Выполняет скролл к странице и мигает анимацией
      var options = {
          // container: 'app',
          // easing: VueScrollTo.easing['ease-in'],
          offset: -60,
          onDone: function() {
            // scrolling is done
          },
          onCancel: function() {
            // scrolling has been interrupted
          }
      }
      VueScrollTo.scrollTo('#page_id_'+page_id, 500, options)
      var elem=document.querySelector('#page_id_'+page_id)
      elem.classList.remove('flash')
      setTimeout(()=>elem.classList.add('flash'),100)
      // elem.classList.toggle('flash')
      //animated flash
    },
    /*MAP*/
    fitBounds() {
    return 0
      if (this.bounds==null){
        this.bounds=new google.maps.LatLngBounds()
      }
      //this.my_zoom_size=4
      console.log('fit bounds call')
      if (this.markers.length>0){

        var m=null
        for (m in this.markers){
          bounds.extend({
            lat: this.markers[m].position.lat,
            lng: this.markers[m].position.lng
          })
          console.log('bounds EXTENDED ',this.markers[m].position.lat ,this.markers[m].position.lng)
        }
        //Теперь создадим точку чтобы совсем близко не зумило
        //var extendPoint1 = new google.maps.LatLng(b.getNorthEast().lat() + 0.01, b.getNorthEast().lng() + 0.01);
        //var extendPoint2 = new google.maps.LatLng(b.getNorthEast().lat() - 0.01, b.getNorthEast().lng() - 0.01);
        //b.extend(extendPoint1);
        //b.extend(extendPoint2);


        this.$refs.mmm.fitBounds(bounds);

        this.$refs.mmm.panToBounds(b);
        console.log('ZOOM CHANG??',this.my_zoom_size)
      }

    },

    //SEARCHBOX
    loadAll() {
      return [
        { "value": "Задания", "link": "https://github.com/vuejs/vue" },
        { "value": "Впечатления", "link": "https://github.com/ElemeFE/element" },
        { "value": "Где я?", "link": "https://github.com/ElemeFE/cooking" },
        { "value": "Развлечения", "link": "https://github.com/ElemeFE/mint-ui" },
        { "value": "События", "link": "https://github.com/vuejs/vuex" },
       ];
    },
    querySearchAsync(queryString, cb) {
      var links = this.links;
      var results = queryString ? links.filter(this.createFilter(queryString)) : links;

      clearTimeout(this.timeout);
      this.timeout = setTimeout(() => {
        cb(results);
      }, 3000 * Math.random());
    },
    createFilter(queryString) {
      return (link) => {
        return (link.value.indexOf(queryString.toLowerCase()) === 0);
      };
    },
    handleSelect(item) {
      console.log(item);
    }
  },
  beforeRouteUpdate (to, from, next) {
     this.page_num=1
     next()
  },

  watch: {
		'$route'() {
      this.author=null;
			this.nex_page = 1
			this.pages = []
			this.fetchPage()
		},

  },
  computed:{

  },
  created: function () {
    // Get the coordinates of the current position.
    let position={}
    navigator.geolocation.getCurrentPosition(function(position) {

      // console.log('position.coords',position.coords)
      this.position={'lat':position.coords.latitude,'lng':position.coords.longitude}
      // position={'label':'YOU','position':{'lat':position.coords.latitude,'lng':position.coords.longitude} }
      position = {
        position:{
          'lat':position.coords.latitude,
          'lng':position.coords.longitude
        },
        statusText: "USER",
        draggable: true,
      }
      //this.markers=[]
      //this.user_marker=position

    // this.center=this.position

     auth.user.position=position
     // this.center={'lat':parseFloat(position.lat),'lng':parseFloat(position.lng)}
     this.fitBounds()
    }.bind(this));

    finance.getCurrency(this)

    this.fetchPage()
  },
  mounted(){
		this.links = this.loadAll();
  }

}
</script>
<style lang="scss">

$blue: #6d9ee1;

.button{
  background-color: $blue;
  color: #e5e5e5;
  text-align: center;
  padding: 10px;
  border-radius: 4px;
  &:hover{
    color: #fff;
  }
}
.voter-list{

}
.el-icon-loading{
  text-align: center;
  vertical-align: middle;
  display: block!important;
  margin-top: 50%!important;
}

body, html{
    padding: 0;
    margin: 0;
}
/*Microframework*/
.one-fourth{
  width:25%;
  display: inline-block;
  float: left;
}
.half{
  width:50%;
  display: inline-block;
  float: left;
}
.full{
  width: 100%;
  display: block;
  clear: both;
  a{
    color: #000!important;
    &:hover{
      text-decoration: none!important;
    }
  }
  h2{
    &:hover{
      text-decoration: underline!important;
    }
  }
}
.table {
  >*{
    display: table-cell;
  }
  display: table;
  width:100%;
}
.infopanel{
  >*{
    text-align: center;
  }
}
/*end Microframework*/



/*
.el-dropdown {

    color: #fff!important;
    font-size: 14px;
    padding: 10px;
}
 */
.page-list{

  display: block;
  width: 100%;
  padding: 23px;
  box-sizing: border-box;
  .profile{
    background: #fff;
    display: block;

    border-radius: 10px;
    margin-bottom: 35px;
    .username{
      color:#485465;
      font-size: 26px;
      text-align: center;
    }
  }
  .author_avatar{
    width: 200px;
    height: 200px;
    border-radius: 200px;
    display: block;
    margin: auto;
  }
  .self_blog_view_buttons{
    text-align: center;
    margin: 10px;
    display: inline-block;
    width: 100%;
  }


  .article{
    display: inline-block;
    clear: both;
    box-shadow: 0px 0px 43px rgba(0, 0, 0, 0.1);
    border-bottom: 2px solid #eee;
    cursor: pointer;
    border-radius: 5px;
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 10px;
    background-color: #fff;
    h1{
      padding: 0;
      margin: 0 0 5px 0;
      font-size: 24px;
    }
    a{
      /* color: inherit; */
    }
    .body{
      min-height: 100px;
    }

    .post-preview{

      .post-info{
        box-shadow: 0 0 7px 0 rgba(0, 0, 0, 0.33);
        border-radius: 5px;
        display: table;
        position: relative;
        width: 95%;
        background: #fff;
        top: -55px;
        margin: 10px auto -40px auto;
        clear: both;
        min-height: 150px;
        box-sizing: border-box;
        padding: 10px;
        img{
          width: 50px;
          height: 50px;
          float: left;
          display: inline-block;

        }
        .avatar{

          display: table-cell;
          >img{
            border-radius: 50px;
          }
        }
        .head{
          padding: 0 10px;
          box-sizing: border-box;
          vertical-align: top;
          display:table-cell;
        }
      }
      .comments{
        font-size: 12px;
      }
      .bottom{
        padding: 0 22px;
        margin-bottom: 15px;
        width: 100%;
        box-sizing: border-box;
        display: inline-block;
      }
    }

    .post-image{
      width: 100%;
      height: 400px;
      object-fit: cover;
    }

    .dummy-image{
     display: inline-block;
     width: 20%;
     height: 140px;
     background-size: contain;
     background-repeat: no-repeat;
     background-position: 50%;
    }
    img{
     float: left;

     height: auto;
     vertical-align: middle;


    }

    img[lazy*="error"], img[lazy*="loading"]{
      display: none;
    }
    img[lazy*="loaded"] + .dummy-image{
      display: none;
    }
    .content{
      float: right;
      display: inline-block;
      width: 80%;
      overflow: hidden;
      height: auto;
    }


  }

  a{
    color: #337ab7;
    text-decoration: none;
    &:hover{
      text-decoration: underline;
    }
  }
}


article
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0
}
</style>

<style lang="scss" scoped>
.voter-list{
 width: 48%;
    position: fixed!important;
    left: 52%!important;
    border: 1px solid #ccc;
    box-sizing: border-box;
    top: 50%!important;

}
.stat{
  display: inline-block;
  float: left;
  box-sizing: border-box;
  padding-right: 15px;
  text-align: right;
  width: 20%;
}
.voters{
  display: inline-block;
  float: left;
  box-sizing: border-box;
  height: 40px;
  width: 80%;
  border:1px dotted #aaa;
  overflow: scroll;
  &:hover{
   position: relative;
   top: 0;
   right: 0;
   border: 1px solid #eaeaea;
   height: 200px;
   background-color: #ffffff;
   margin-top: -160px;
   box-shadow: 1px 1px 20px rgba(0,0,0,0.2) inset;
   padding: 2px;
   border-radius: 10px…;
  }

}
.voter{
  display: inline-block!important;
  float: left!important;
  margin-left: 5px;
  &:hover{
    background-color: #ccc;

  }
}
  .vue-map-container{
    left: 0;
    top: 0;
    position: fixed;
    z-index: 0;
    width: 100%;
    height: 100vw;
  }
  .wrapper{
    display: block;
    z-index: 10;
    position: relative;
    width: 38%;
    padding-left: 3%;

  }
  .loader{
   height: 100vw;
   display: block;
   z-index: 10;
   width: 49%;
   text-align: center;
   vertical-align: middle;
   position: fixed;
  }

  .search-box{
    position: fixed;
    right: 1%;
    width: 48%;
    top: 80px;
    z-index: 10;
    input{
      width: 100%;
    }
    .el-autocomplete, .el-dropdown {

        width: 100%;
    }
  }
</style>
