# fd
> Mommy! what is a file descriptor in Linux?
* try to play the wargame your self but if you are ABSOLUTE beginner, follow this tutorial lin
k: https://www.youtube.com/watch?v=blAxTfcW9VU

>ssh fd@pwnable.kr -p2222 (pw:guest)

题目描述考察`linux`文件描述符

![](/home/r7/screenshots/pwnable.md/2017-05-13_140852.png)

可以看到读取输入的参数，将第一个参数转换为`int`然后减去`0x1234`作为`fd`的值

接下来在`read`函数中，将`fd`作为第一个参数

In linux, 0 is std_input, 1 is std_output, 2 is std_error_output.

在`linux`中文件描述符的定义：`0`是标准输入`1`是标准输出`2`是标准错误输出

![](/home/r7/screenshots/pwnable.md/2017-05-13_201554.png)

而`read`函数的第一个参数接收的就是文件描述符

而`0x1234`的十进制值正好是`4660`所以我们先输入`4660`并接下来输入`LETMEWIN`即可

# collision
>Daddy told me about cool MD5 hash collision today.
I wanna do something like that too!

>ssh col@pwnable.kr -p2222 (pw:guest)

``` c++
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
	int* ip = (int*)p;
	int i;
	int res=0;
	for(i=0; i<5; i++){
		res += ip[i];
	}
	return res;
}

int main(int argc, char* argv[]){
	if(argc<2){
		printf("usage : %s [passcode]\n", argv[0]);
		return 0;
	}
	if(strlen(argv[1]) != 20){
		printf("passcode length should be 20 bytes\n");
		return 0;
	}

	if(hashcode == check_password( argv[1] )){
		system("/bin/cat flag");
		return 0;
	}
	else
		printf("wrong passcode.\n");
	return 0;
}

```

