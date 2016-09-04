---
version: 0.10

date:2016.08.28

---

# 豆瓣book api代理接口文档


项目: 提供根据`isbn` 来请求相关的豆瓣API获取相应图书信息的接口

目前挂靠于 **`douproxy.note-show.com`** 下，示例 [http://douproxy.note-show.com/api/v2.0/book/isbn/9787302275954](http://douproxy.note-show.com/api/v2.0/book/isbn/9787302275954) 
## 介绍

 源代码在`./douban/` 目录下

 相关的豆瓣API的版本有2个，即返回的数据类型有2种，两种API对应文件分别是
 
- `apiv2.py` 称为`v2`格式
- `apiv2_frodo.py` 称为`v2frodo`格式

而系统提供的API版本目前分为3个
 
 - `v1.0` 使用搜索(`search.py`)得到`bookid`，然后调用`v2`返回豆瓣`v2`格式数据
 - `v1.1` 调用豆瓣`v2frodo`api 得到`bookid`,然后调用`v2`返回`v2`格式数据
 - `v2.0` 调用豆瓣`v2frodo`api ,返回该格式数据

### 请求与返回
  
#### 请求

  使用`http`请求，返回数据为`json`格式

  目前提供
  
  `GET` `/api/{version}/book/isbn/{isbn}`
  
  `GET` `/api/{version}/book/{bookid}`(`v1.1` 版本没有此api)
  
  以及 `v1.0` 中单独的api

  `GET` `/api/v1.0/book/name/{name }`

  其中`version`即上面提到的`v1.0`,`v1.1`,`v2.0`三种
  
  `isbn`即图书的isbn编号,例如: `9787302275954`
  
  相关链接示例:
  
  `http://douproxy.note-show.com/api/v1.1/book/isbn/9787302275954`
 
#### 返回  
 返回的json数据格式为
 
 ```json
 {
  "msg": "成功了",
  "code": 100000,
  "data": {
  	......
  	},
  "version": 1.1
}
 ```
 其中`version`为版本号(float),`code` 为返回码(int)，`msg`为相应的信息(string)
 
`data`是相应的数据(object / null)

**`code-msg`** 表

 code  |     msg    | 意义
-------|------------|------
100000 | 成功了      | 请求成功
200504 | 请求超时了呀 | 请求豆瓣API超时
200403 | 被屏蔽了呢	  | 搜索被屏蔽
200404 | 没找到这个哎 | 404
200999 | 未知错误 	  | 未知错误(可能豆瓣API改动)


## 部署

### python 版本

python2 python3 皆可

### 依赖

- `requests`
- `pyquery` （仅`v1.0`使用）
- `weppy`

依赖安装 使用 `pip install -r requirements.txt`即可

或者单个安装

```sh
pip install requests
pip install pyquery
pip install weppy
```
必要时候`sudo`

### 配置

需要修改 `const.py` 的部分代码来配置

```python
const.PORT = 8001
const.ALLOW_HOST = '0.0.0.0'
```
PORT 指定访问端口，

ALLOW_HOST 指定可以访问的IP，`0.0.0.0`表示任意IP皆可访问，

建议不要使用`0.0.0.0`,根据情况设置

### 运行

直接 `python douproxy.py`即可，linux 可以开始`screen`运行

## `data` 字段解释

这里就不准备填表格了

给出data 内部各个字段的说明

相关字段后隔一段空白，即这个字段的说明

```python
{
  "images": {
    "medium": "http://img3.douban.com/mpic/s9108113.jpg",    中等尺寸的封面图
    "large": "http://img3.douban.com/lpic/s9108113.jpg",     大封面图
    "small": "http://img3.douban.com/spic/s9108113.jpg"      小封面图
  },
  "price": "38.00元",      价格
  "tags": [                标签数组（按照count多少排序的）
    {
      "name": "机器学习",   标签
      "title": "机器学习",  显示的标签
      "count": 1136        被多少人标记为这个标签
    },
    {
      "name": "统计学习",
      "title": "统计学习",
      "count": 992
    },
    {
      "name": "数据挖掘",
      "title": "数据挖掘",
      "count": 381
    },
    {
      "name": "统计",
      "title": "统计",
      "count": 350
    },
    {
      "name": "统计学",
      "title": "统计学",
      "count": 332
    },
    {
      "name": "数学",
      "title": "数学",
      "count": 303
    },
    {
      "name": "MachineLearning",
      "title": "MachineLearning",
      "count": 257
    },
    {
      "name": "计算机",
      "title": "计算机",
      "count": 254
    }
  ],
  "binding": "",         未知
  "origin_title": "",    原始名称可以，不用
  "alt_title": "",       更改名称，不用
  "pages": "235",        页数
  "id": "10590856",      bookid，可以不用
  "isbn13": "9787302275954",  13位的isbn
  "url": "http://api.douban.com/v2/book/10590856",        豆瓣链接，可以不用
  "translator": [],      译者，作者名字的字符串
  "subtitle": "",        子标题，可以不用
  "isbn10": "7302275955", 10位isbn
  "alt": "https://book.douban.com/subject/10590856/",     未知
  "publisher": "清华大学出版社",		出版社
  "image": "http://img3.douban.com/mpic/s9108113.jpg",    封面图
  "author_intro": "李航 日本京都大学电气工程系毕业，日本东京大学计算机科学博士。曾任职于日本NEC公司中央研究所，微软亚洲研究院高级研究员及主任研究员，现任华为诺亚方舟实验室首席科学家。北京大学、南开大学、西安交通大学客座教授。研究方向包括信息检索、自然语言处理、统计机器学习及数据挖掘。",
                 作者介绍
  "rating": {       评分
    "max": 10,      最高
    "min": 0,       最低
    "average": "8.9", 平均
    "numRaters": 736  评分人数
  },
  "title": "统计学习方法",    书名
  "catalog": "第1章 统计学习方法概论\n1.1 统计学习\n1.2 监督学习\n1.3 统计学习三要素\n1.4 模型评估与模型选择\n1.5 i~则化与交叉验证\n1.6 泛化能力\n1.7 生成模型与判别模型\n1.8 分类问题\n1.9 标注问题\n1.10 回归问题\n本章概要\n继续阅读\n习题\n参考文献\n第2章 感知机\n2.1 感知机模型\n2.2 感知机学习策略\n2.3 感知机学习算法\n本章概要\n继续阅读\n习题\n参考文献\n第3章 众近邻法\n3.1 k近邻算法\n3.2 k近邻模型\n3.3 k近邻法的实现：kd树\n本章概要\n继续阅读\n习题\n参考文献\n第4章 朴素贝叶斯法\n4.1 朴素贝叶斯法的学习与分类\n4.2 朴素贝叶斯法的参数估计\n本章概要\n继续阅读\n习题\n参考文献\n第5章 决策树\n第6章 逻辑斯谛回归与最大熵模型\n第7章 支持向量机\n第8章 提升方法\n第9章 em算法及其推广\n第10章 隐马尔可夫模型\n第11章 条件随机场\n第12章 统计学习方法总结\n附录a 梯度下降法\n附录b 牛顿法和拟牛顿法\n附录c 拉格朗日对偶性\n索引",                    
                  目录，用`\n` 连接
  "author": [     作者列表    
    "李航"
  ],
  "pubdate": "2012-3",   出版日期
  "summary": "《统计学习方法》是计算机及其应用领域的一门重要的学科。《统计学习方法》全面系统地介绍了统计学习的主要方法，特别是监督学习方法，包括感知机、k近邻法、朴素贝叶斯法、决策树、逻辑斯谛回归与最大熵模型、支持向量机、提升方法、EM算法、隐马尔可夫模型和条件随机场等。除第1章概论和最后一章总结外，每章介绍一种方法。叙述从具体问题或实例入手，由浅入深，阐明思路，给出必要的数学推导，便于读者掌握统计学习方法的实质，学会运用。为满足读者进一步学习的需要，书中还介绍了一些相关研究，给出了少量习题，列出了主要参考文献。"
                  内容概括
}
```


