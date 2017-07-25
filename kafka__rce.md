# XXX漏洞分析报告

author: xxx@360CERT

## 背景介绍

Apache Kafka 是开源的Apache流处理平台由 Apache编写采用scala与java。

该项目旨在于提供一个统一的、高吞吐量的、低延迟的实时数据处理平台

## 漏洞概述

`org.apache.kafka.connect.storage.FileOffsetBackingStore` 这个`class`拥有一个反序列化操作,在执行
`FileOffsetBackingStore`对象的`start`方法时候会触发并反序列恶意序列化对象，导致代码执行

因为`Kafka`是一个开源的框架，如果用户在使用的过程中实现了类似实例化`FileOffsetBackingStore`这个对象，并且传入参数受到控制的业务逻辑的话就会受到该漏洞的影响

## 漏洞详情

### 影响版本
Apache Kafka 

0.10.0.0 -> 0.11.0.0(latest)

均受到影响

## 漏洞细节分析

首先生成一个恶意的对象，这个对象在反序列化后就会执行恶意代码，此处采用`ysoserial.payloads.Jdk7u21`这个开源框架中的方法，直接产生一个恶意对象

![](/home/r7/screenshots/kafka_rce.md/2017-07-19_160622.png)

生成这个恶意对象后，将这个对象序列化，然后存储成一个文件，漏洞是`FileOffsetBackingStore`这个只接受文件的class出的所以需要传入这个文件

可以看到我们将执行的命令是`touch 360CERT`创建一个名为`360CERT`的文件

接下来给即将实例化的`FileOffsetBackingStore`对象做一些初始化设置，将要读取的文件路径传入

![](/home/r7/screenshots/kafka_rce.md/2017-07-19_160928.png)

调用`configure`方法后

![](/home/r7/screenshots/kafka_rce.md/2017-07-19_161146.png)

会设置`this.file`这个属性的值，为我们传入的文件

调用`start`方法后

![](/home/r7/screenshots/kafka_rce.md/2017-07-19_161327.png)

![](/home/r7/screenshots/kafka_rce.md/2017-07-19_161405.png)

所以直接进入`load`方法

![](/home/r7/screenshots/kafka_rce.md/2017-07-19_161505.png)

可以看到这里将`this.file`的值读取到`is`中，这里就是我们构造的恶意序列化的对象

而接下来调用的`readObject()`方法正好会分序列化这个对象

![](/home/r7/screenshots/kafka_rce.md/2017-07-19_161707.png)

![](/home/r7/screenshots/kafka_rce.md/2017-07-19_161738.png)

可以看到`360CERT`这个文件已经被我们创建了







