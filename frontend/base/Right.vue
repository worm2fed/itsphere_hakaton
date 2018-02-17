<template>
  <aside>

		<!-- Как это должно работать? -->
		<!-- item class="item" :tree="tree"></item> -->
  </aside>
</template>

<script>
import Vue from 'vue';
import Item from './Item.vue'
import {MasterTag} from '../services/services'

export default {
  name: 'right',
  data () {
    return {
      tree: {}
    }
  },
  created: function() {
    MasterTag.tree().then(res => this.tree = res.body)
  },
	components: {
		'Item': Item,
	},
}
</script>

<style lang="scss">
aside {
  display: block;
  width: 100%;
  vertical-align: top;
  top: 48px;
  font-size: 14px;
  background-color: #fff;
  position: fixed;
  z-index:100;
  left: 0;
  > li > ul{
      padding: 0;
      margin: 0;
  }
  .ele{
    width: 100%;
    box-sizing: border-box;
    text-align: left;
  }
}

.active{
    font-weight: bold;
}
</style>
