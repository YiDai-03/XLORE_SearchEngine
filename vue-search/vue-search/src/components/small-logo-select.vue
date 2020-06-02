<template>
	<!-- 选择logo组件 -->
	<div class="logo">
		<img :src="imgSrc">
	</div>
</template>

<script>
	// export defult是es6中的方法，将整个花括号对象暴露出去;
	export default {
		data: function() {
			return {

					imgSrc: require('../assets/logo2.png') ,

			}
		},
		methods: {

		}
	}
</script>

<style>
	ul{
		list-style: none;
		padding: 0;
		margin: 0;
	}

	.logo{
		width: 90px;
		/* height: 140px; */
		/* position: relative; */
    /* margin: auto; */
    margin-left: 0;
    margin-top: -10px;
    float: left;
	}

	.logo img{
		display: block;
		margin: 0;
    width:90px;
		user-select: none; /*文本不能被选择*/
		cursor: pointer;
	}


</style>
