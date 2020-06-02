<template>
  <div>
    <div v-if="answer">
      <div  v-for="item in descriptions">
        <el-card class="box-card" >
         <span v-html="msg(item.word)"></span>
         来源：
         <span v-html="msg3(item.uri)"></span>
    </el-card>
    </div>
    </div>
<el-card class="box-card" v-else>
  <div slot="header" class="clearfix">
    <span>{{label}}</span>
    <a class="el-icon-link" style="text-decoration-line: none" :href="uri" ></a>

  </div>
  <el-collapse >

    <el-collapse-item title="描述" >
      <span v-html="msg(description)"></span>
    </el-collapse-item>
    <el-collapse-item title="属性">
        <div v-for = "(item, index) in keys" >
    <row v-if="index%2==0&&index+1<keys.length" v-bind:key1="keys[index]" v-bind:val1="values[index]"
     v-bind:key2="keys[index+1]" v-bind:val2="values[index+1]"></row>
    <row v-if="index%2==0&&index+1==keys.length" v-bind:key1="keys[index]" v-bind:val1="values[index]"></row>
        </div>
    </el-collapse-item>
    <el-collapse-item title="标签">
         <el-tag v-for="(item, index) in classes":key="index" type="success">
           <span v-html="msg2(item)"></span>
           </el-tag>
    </el-collapse-item>
    <el-collapse-item title="相关项">
      <el-tag v-for="(item, index) in relevant":key="index" type="success">
        <span v-html="msg2(item)"></span>
        </el-tag>
    </el-collapse-item>
  </el-collapse>

</el-card>
</div>
</template>

<script>
  import row from "./row.vue"
  export default {
    name: 'card',
    components: {
        row
    },

    data() {
      return {
        answer: false,
        description: "",
        descriptions: [],
        label: "",
        uri: "",
        property: {},
        keys: [],
        values: [],
        relevant: [],
        classes: []
      }

    },

    props: {
        entity: Object
    },

    created() {
        if(this.$props.entity){

          this.property = this.$props.entity;
          if(this.property["tag"] == "answer"){
            this.answer = true;
            this.descriptions = this.property["详情"];
            window.console.log(this.property);
          }
          else{
            this.label =this.property["名称"];
            this.description = this.property["详情"];
            this.relevant = this.property["相关项"];
            this.classes = this.property["标签"];
            this.uri = "https://xlore.org/instance.html?url=" + this.property["锚点"];

            delete this.property["相关项"];
            delete this.property["标签"];
            delete this.property["名称"];
            delete this.property["详情"];
            delete this.property["锚点"];
            delete this.property["rel"];
		delete this.property["entity_class"];
            //delete this.property["score"];
            for(var k in this.property){
              if(this.property[k] == ""){
                delete this.property[k];
              }
            }
            this.keys = Object.keys(this.property)
            this.values = Object.values(this.property)
          }
        }


    },


    methods:{

    }
  }
</script>

<style>
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;

  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    width: 1000px;
    margin-bottom: 30px;
    margin-left: 225px;
  }
</style>
