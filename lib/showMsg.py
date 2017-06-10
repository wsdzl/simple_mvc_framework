def showMsg(msg, isAutoGo=False, url = ''):
	if not url:
		url = 'javascript:history.back(-1);'
	if msg == '404':
		msg = '页面不存在！'
	page = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-CN">
<head>'''
	if isAutoGo:
		page += '<meta http-equiv="refresh" content="1.25;url=%s" />' % url
	page += '''<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=0.7">
<title>提示信息</title>
<style type="text/css">
<!--
body {
	background-color:#F7F7F7;
	font-family: Arial;
	font-size: 12px;
	line-height: 150%;
	text-align: center;
}
.main {
	background-color:#FFFFFF;
	font-size: 12px;
	color: #666666;
	display: inline-block;
	margin:60px auto 0px;
	border-radius: 10px;
	padding:30px 10px;
	list-style:none;
	border:#DFDFDF 1px solid;
}
.main p {
	line-height: 18px;
	margin: 5px 20px;
}
-->
</style>
</head>
<body>
<div class="main">
<p style="color:#6a6a6a;font-weight:bold;font-size:22px;line-height:2em">'''
	page += msg + '</p>'
	if isAutoGo:
		page += '<p style="margin-left:25px">自动跳转中……</p>'
	else:
		page += '<p><a href="%s">&laquo;点击返回</a></p>' % url
	page += '</div></body></html>'
	return page.encode('utf-8')