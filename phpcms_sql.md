# phpcms v9.6.0 sql inject

phpcms 采用mvc

数据库查询函数有

get_one

select

query

这样三种

那么挖掘sql注入最终总是要经过这几个函数的，那么我们去寻找这几个函数所在的位置

先减小难度，通常前台sql的危险系数大，所以着重找前台的sql

那么mvc架构下

(phpcmsv9 文档)[http://v9.help.phpcms.cn/html/2010/structure_0928/71.html]

!(图示)[~/screenshot/2017-04-21_5x732.png]

那么我们搜索的点肯定集中在phpcms_dir/phpcms/modules/*

grep 提取文件名
grep -rn "select(" * | cut -d":" -f 1
