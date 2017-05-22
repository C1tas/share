
上一篇已经过多赘述，这里就直接切入

还是`attachments.php`

``` php

class attachments {
	private $att_db;
	function __construct() {
		pc_base::load_app_func('global');
		$this->upload_url = pc_base::load_config('system','upload_url');
		$this->upload_path = pc_base::load_config('system','upload_path');		
		$this->imgext = array('jpg','gif','png','bmp','jpeg');
		$this->userid = $_SESSION['userid'] ? $_SESSION['userid'] : (param::get_cookie('_userid') ? param::get_cookie('_userid') : sys_auth($_POST['userid_flash'],'DECODE'));
    		$this->isadmin = $this->admin_username = $_SESSION['roleid'] ? 1 : 0;
		$this->groupid = param::get_cookie('_groupid') ? param::get_cookie('_groupid') : 8;
		//判断是否登录
		if(empty($this->userid)){
			showmessage(L('please_login','','member'));
		}
	}
```

``` php
$this->userid = $_SESSION['userid'] ? $_SESSION['userid'] : (param::get_cookie('_userid') ? param::get_cookie('_userid') : sys_auth($_POST['userid_flash'],'DECODE'));

```

可以看到，这里接受多种`userid`的赋值，但是能够利用的还是那几样，可以像上次`sql`那种`cookie`赋值，也可以post `userid_flash`

至此绕过的登录的验证，关于生成这个`userid`的还是wap模块生成的`siteid`的值


``` php
{"aid":1,"src":"&i=1&m=1&d=1&modelid=1&catid=1&s=.\/phpcms\/modules\/content\/down.ph&f=p%3%252%270C","filename":""}
```
`init`中的safe_replace

``` php
&quotaid&quot:1,&quotsrc&quot:&quot&i=1&m=1&d=1&modelid=1&catid=1&s=./phpcms/modules/content/down.ph&f=p%3%2520C&quot,&quotfilename&quot:&quot&quot
```

此时的`$f=p%3%2520C`

![](/home/r7/screenshots/phpcms_9.6.1_anyfile_download.md/2017-05-08-105553_979x285.png)

可以看到，因为传入了 `$f,$catid,$modelid,$i,$m`成功通过了一系列的初始化检测

![](/home/r7/screenshots/phpcms_9.6.1_anyfile_download.md/2017-05-08-105907_1920x1034.png)

``` php
if(preg_match('/(php|phtml|php3|php4|jsp|dll|asp|cer|asa|shtml|shtm|aspx|asax|cgi|fcgi|pl)(\.|$)/i',$f) || strpos($f, ":\\")!==FALSE || strpos($f,'..')!==FALSE) showmessage(L('url_error'));

if(strpos($f, 'http://') !== FALSE || strpos($f, 'ftp://') !== FALSE || strpos($f, '://') === FALSE)
```

可以看到，这里对`$f`的校验，限制多种危险后缀，以及不能带有协议，以及不能目录跨越

但是无关痛痒，因为我们的路径在`$s`中

![](/home/r7/screenshots/phpcms_9.6.1_anyfile_download.md/2017-05-08-111207_1357x554.png)

可以看到，`$a_k`又被重新加密并传给`modules/content/down.php`中的`download`函数

此处限定的参数正好又有`$i,$d,$s,$m,$f,$modelid`这几个

![](/home/r7/screenshots/phpcms_9.6.1_anyfile_download.md/2017-05-08-114732_1001x81.png)

在`download`函数中，正好整个框架中，仅有这两处采用了相同的`auth_key`

![](/home/r7/screenshots/phpcms_9.6.1_anyfile_download.md/2017-05-08-115135_1369x640.png)

可以看到关键的`$s,$f`的值都成功接收到了。而`parse_str`这种危险函数的滥用在处理接收的参数的位置是十分不可取的

![](/home/r7/screenshots/phpcms_9.6.1_anyfile_download.md/2017-05-08-115635_1164x58.png)

再一次经过`safe_replace`

`$f=p%3C`

![](/home/r7/screenshots/phpcms_9.6.1_anyfile_download.md/2017-05-08-115954_1125x131.png)

如果`$m`有值则直接拼接`$s`,`$fileurl`，而`$fileurl`也就是`$f`

![](/home/r7/screenshots/phpcms_9.6.1_anyfile_download.md/2017-05-08-122632_1141x351.png)

然后经过最后的这个`str_replace`将 `<,>`替换为`''`之后就得到了完整并且正确的`$fileurl`

![](/home/r7/screenshots/phpcms_9.6.1_anyfile_download.md/2017-05-08-123651_861x107.png)

![](/home/r7/screenshots/phpcms_9.6.1_anyfile_download.md/2017-05-08-125003_1189x115.png)

进入`file_down`函数中，已经没有任何的过滤和处理

![](/home/r7/screenshots/phpcms_9.6.1_anyfile_download.md/2017-05-08-125106_1258x380.png)

至此触发漏洞

进行回顾的话就能发现，其实主要原因还是和之前一样
- 使用`str_parse`这种危险函数
- 只是多次的单一调用`safe_replace`函数，而不是在一次中递归执行，这就导致了，可以事先进行多次复写，然后导致绕过
