# 搭建 nginx 基础环境
```
git clone git@github.com:nginx/nginx.git
cd nginx
git checkout release-1.13.2
./auto/configure --prefix=/home/r7/bin/
make
make install
```


# 漏洞入手

# Detail

```

Hello!

A security issue was identified in nginx range filter.  A specially
crafted request might result in an integer overflow and incorrect
processing of ranges, potentially resulting in sensitive information
leak (CVE-2017-7529).

When using nginx with standard modules this allows an attacker to
obtain a cache file header if a response was returned from cache.
In some configurations a cache file header may contain IP address
of the backend server or other sensitive information.

Besides, with 3rd party modules it is potentially possible that
the issue may lead to a denial of service or a disclosure of
a worker process memory.  No such modules are currently known though.

The issue affects nginx 0.5.6 - 1.13.2.
The issue is fixed in nginx 1.13.3, 1.12.1.

For older versions, the following configuration can be used
as a temporary workaround:

    max_ranges 1;

Patch for the issue can be found here:

http://nginx.org/download/patch.2017.ranges.txt


-- 
Maxim Dounin
http://nginx.org/

```

patch 

```
diffsrc/http/modules/ngx_http_range_filter_module.c b/src/http/modules/ngx_http_range_filter_module.c
--- src/http/modules/ngx_http_range_filter_module.c
+++ src/http/modules/ngx_http_range_filter_module.c
@@ -377,6 +377,10 @@ ngx_http_range_parse(ngx_http_request_t 
             range->start = start;
             range->end = end;
 
+            if (size > NGX_MAX_OFF_T_VALUE - (end - start)) {
+                return NGX_HTTP_RANGE_NOT_SATISFIABLE;
+            }
+
             size += end - start;
 
             if (ranges-- == 0) {
```

我们根据这个patch 的内容，进行该版本内的源码阅读发现

该处patch所在函数是`ngx_http_range_parse`
位于`/home/r7/source-make/nginx/src/http/modules/ngx_http_range_filter_module.c` #269

核心起点

```
p = r->headers_in.range->value.data + 6 // +6的意义在于偏移掉`Range:`这6个字符
```


```
    for ( ;; ) {
        start = 0;
        end = 0;
        suffix = 0;

        while (*p == ' ') { p++; }

        if (*p != '-') {
            if (*p < '0' || *p > '9') {
                return NGX_HTTP_RANGE_NOT_SATISFIABLE;
            }

            while (*p >= '0' && *p <= '9') {
                if (start >= cutoff && (start > cutoff || *p - '0' > cutlim)) {
                    return NGX_HTTP_RANGE_NOT_SATISFIABLE;
                }

                start = start * 10 + *p++ - '0';
            }

            while (*p == ' ') { p++; }

            if (*p++ != '-') {
                return NGX_HTTP_RANGE_NOT_SATISFIABLE;
            }

            while (*p == ' ') { p++; }

            if (*p == ',' || *p == '\0') {
                end = content_length;
                goto found;
            }

        } else {
            suffix = 1;
            p++;
        }

        if (*p < '0' || *p > '9') {
            return NGX_HTTP_RANGE_NOT_SATISFIABLE;
        }

        while (*p >= '0' && *p <= '9') {
            if (end >= cutoff && (end > cutoff || *p - '0' > cutlim)) {
                return NGX_HTTP_RANGE_NOT_SATISFIABLE;
            }

            end = end * 10 + *p++ - '0';
        }

        while (*p == ' ') { p++; }

        if (*p != ',' && *p != '\0') {
            return NGX_HTTP_RANGE_NOT_SATISFIABLE;
        }

        if (suffix) {
            start = content_length - end;
            end = content_length - 1;
        }

        if (end >= content_length) {
            end = content_length;

        } else {
            end++;
        }

    found:

        if (start < end) {
            range = ngx_array_push(&ctx->ranges);
            if (range == NULL) {
                return NGX_ERROR;
            }

            range->start = start;
            range->end = end;

            size += end - start;

            if (ranges-- == 0) {
                return NGX_DECLINED;
            }

        } else if (start == 0) {
            return NGX_DECLINED;
        }

        if (*p++ != ',') {
            break;
        }
    }
```

这个大for里面分割SSSS-EEEEE这种

Range: bytes=-403,-9223372036854775407

这种构造

使得
papyload需要满足两个要求：

A + B = 0x7FFFFFFFFFFFFFFF + content_lenth (返回的字节数）
A = content_length + x （其中x是我们想要读取的字节数）
上面得payload中，A为403，B为9223372036854775407，读取的字节数为400，content_length为3。

目前尚未确定此处成因
# 逻辑流程

