<template>
    <!-- <div> -->
      <el-container>
        <el-header style="margin-top:10px;"><smallpanel style="display: flex;"></smallpanel></el-header>
         <el-container v-loading="loading" style="margin-top: 50px;" element-loading-background="rgba(250, 250, 250, 0.4)" element-loading-text="拼命搜索中"
            element-loading-spinner="el-icon-loading">
            <el-main style="width:1400px; " >
              <div style = " height:300px" v-if="loading" ></div>
              <div v-for="item in infos">
               <card v-bind:entity="item"></card>
              </div>
            </el-main>

          </el-container>
      </el-container>


</template>

<script>
  import smallpanel from './small-search-panel.vue'
  import card from './card.vue'
  export default {
    name: 'result',
    components: {
      smallpanel, card
    },

    data() {
        return {
          query: 'u',
          loading: true,
          infos:[]
       };
    },

    created: function (){

        this.query = this.$route.query.content;
        this.$axios.get('/api/', {
            params: {
              q: this.query
            },
             dataType: 'jsonp',
              crossDomain: true
          }).then(res => {
            window.console.log(res.data)
            this.infos = res.data;
         
            this.loading = false;

           })

    },

    methods:{
        back(){
            this.$router.push('/')
        }
    }
  }
</script>
