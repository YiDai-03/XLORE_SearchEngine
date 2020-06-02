<template>
	<!-- 选择logo组件 -->
	<div class="main-logo">
		<img :src="imgSrc">
	</div>
</template>

<script>
	// export defult是es6中的方法，将整个花括号对象暴露出去;
	export default {
		data: function() {
			return {

					imgSrc: require('../assets/logo.png') ,

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

	.main-logo{
		position: relative;
    margin: auto;
	}

	.main-logo img{
		display: block;
		margin: 0 auto;
    width: 300px;
		user-select: none; /*文本不能被选择*/
		cursor: pointer;
	}


</style>
