<template>
  <el-row :gutter="10">

    <el-col :span="12">
      <div class="grid-content bg-purple">

          <el-tag class="key" type="success">{{key1}}</el-tag>

          <el-tag class="val" ><span v-html="msg(val1)"></span></el-tag>

      </div>


    </el-col>
    <el-col :span="12" v-if="key2">
        <div class="grid-content bg-purple">

          <el-tag class="key" type="success">{{key2}}</el-tag>

          <el-tag class="val" ><span v-html="msg(val2)"></span></el-tag>
      </div>
       </el-col>


  </el-row>
</template>

<script>
  export default {
    name: 'row',

    data() {
      return {

      }

    },

    props: {
        key1: String,
        val1: String,
        key2: String,
        val2: String,

    },


    methods:{

    }
  }


</script>

<style>
  .el-row {
    margin-bottom: 5px;
    &:last-child {
      margin-bottom: 0;
    }
  }

  .el-col {
    border-radius: 4px;
  }

  .bg-purple {
    /* background: rgba(0, 0, 0, 0.5); */
  }

  .grid-content {
    border-radius: 0px;
    min-height: 45px;
    line-height:45px;
    flex: float;
    padding-left: 5px;
  }
  .row-bg {

    background-color: #f9fafc;
  }

  .val{
    float: right;
    margin-top: 6px;
    margin-right:5px;
  }
  .key{
    float: left;
    margin-top: 6px;
    margin-right:5px;
  }
</style>
