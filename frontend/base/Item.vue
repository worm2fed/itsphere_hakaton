<template>
    <li>
        <div class="ele" :class="{bold: isFolder}" v-if="!isRoot">
          <span @click="toggle" v-if="isFolder ">

            <i v-if="!open" class="fa fa-plus-square-o"></i>
            <i v-if="open" class="fa fa-minus-square-o"></i>
            <i class="fa fa-folder-o"></i>
          </span>
          <router-link :to="'/tag/'+this.resultname.replace(' ','%20')"> {{model.label}} </router-link>

        </div>
<!--         <transition name="slide-fade">-->
        <ul v-show="open || isRoot" v-if="isFolder  ">

          <item
            class="item"
            v-for="model in model.children"
						:key="null"
            :model="model"
            >
          </item>

        </ul>
        <!-- </transition> -->
      </li>
</template>

<script>


import Vue from 'vue';

export default {
    name: 'Item',
    data () {
        return {
            open: True,
        }
    },

    props: ['tree'],

    data: function () {
      return {
        open: false,
        selfpath:'-'
      }
    },
    computed: {
      isFolder: function () {
        return this.model.children &&
          this.model.children.length
      },
      isRoot:function () {
        return !this.model.label
      },


    },
    methods: {
      toggle: function () {
        if (this.isFolder) {
          this.open = !this.open
        }
      },
      //REFACTOR THIS! move to separate file
      cyrLat:function (val) {
        //Если с английского на русский, то передаём вторым параметром true.
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
        )();

        return transliterate(val)
      },
      isCyr:function(val){
        return /[а-яА-ЯЁё]/.test(val)
      },
      pageUrl: function (model) {
        // console.log('val',model)
        return '/'+this.cyrLat(model.label)
      },
      changeType: function () {
        if (!this.isFolder) {
          Vue.set(this.model, 'children', [])
          this.addChild()
          this.open = true
        }
      },
      addChild: function () {
        this.model.children.push({
          name: 'new stuffы'
        })
      }
    },
    created: function () {
    //console.log('created fire')
      //Нужно обработать элементы дерева чтобы построить для каждого элемента ссылку запроса
      var current_name= this.model.parentname ? this.model.parentname : ''
      current_name=this.isCyr(current_name) == true ? 'ru--' + this.cyrLat(current_name) : current_name
      // console.log('currentname',current_name)
      for (var el in this.model.children){
        // для каджого дитя пометим его именем родителя
        var mname=this.model.label ? this.model.label+'/' : ''
        mname=this.isCyr(mname) ? 'ru--' + this.cyrLat(mname) : mname
        this.model.children[el].parentname=current_name + mname
      }
      this.resultname = this.resultname == '' ? this.model.label : current_name
      var model_name=this.isCyr(this.model.label) ? 'ru--' + this.cyrLat(this.model.label) : this.model.label
      this.resultname+=model_name
      this.resultname=this.resultname+"/"

    }

}

</script>

<style>
li{
  list-style: none;
  vertical-align: top;
  display: inline-block;
}
.router-link-active{
  font-weight:bold;
  text-decoration: underline;
}
a{
  color: inherit;
  text-decoration: none;
}
.item{

}

/*TRANSITIONS*/
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0
}

.slide-fade-enter-active {
  transition: all .3s ease;
}
.slide-fade-leave-active {
  transition: all .8s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}
.slide-fade-enter, .slide-fade-leave-to
/* .slide-fade-leave-active for <2.1.8 */ {
  transform: translateX(10px);
  opacity: 0;
}
/*END TRANSITIONS*/
</style>
