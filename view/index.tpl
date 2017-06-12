<!DOCTYPE html>
<html lang="zh-cn">
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,Chrome=1">
	<meta name="viewport" content="initial-scale=1, maximum-scale=1, user-scalable=no, width=device-width">
	<script src="http://cdn.bootcss.com/jquery/1.12.4/jquery.min.js"></script>
	<link rel="stylesheet" href="http://cdn.bootcss.com/bootstrap/3.3.0/css/bootstrap.min.css"></link>
	<title>测试一下</title>
</head>
<body style="text-align: center;">
	<h1>{{ENV.headers}}</h1>
	<h2>{{name}}</h2>
	<h3>{{
		if name:
			你好， <b>$(name)</b>
		else:
			<b>Hi! </b> 
	}}</h3>
	<div>
	{{
		for href, link in li:
			<a href='$(href)'>$(link)</a>
	}}
	</div>
	<script src="http://cdn.bootcss.com/bootstrap/3.3.0/js/bootstrap.min.js"></script>
</body>
</html>