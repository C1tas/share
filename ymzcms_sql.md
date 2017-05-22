
select 

find

query

total

sql_execute

insert

update

delete



application/attachment/controller/api.class.php

$this->userid = isset($_SESSION['adminid']) ? $_SESSION['adminid'] : (isset($_SESSION['_userid']) ? $_SESSION['_userid'] : 0);
$this->username = isset($_SESSION['adminname']) ? $_SESSION['adminname'] : (isset($_SESSION['_username']) ? $_SESSION['_username'] : '');
$this->isadmin = isset($_SESSION['roleid']) ? 1 : 0;
$this->groupid = get_cookie('_groupid') ? intval(get_cookie('groupid')) : 0;

index/index/*
guestbook/index/*
commet/index/*
api/index/*
member/myhome/*
mobile/index/*
search/index/*

待验证的点

index/index/show -> index/index/_check_readpoint 这个protacted方法

member_content
not unset post and then insert it 


comment/index => _check_auth 越权
同时后台关闭未登录用户评论


member/index/login => M('point')->point_add

index/index/show => 越权
