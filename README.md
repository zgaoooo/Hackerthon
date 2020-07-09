# Prototype Climate Impact Rating Server & API
- WebApp: 一个简单的web程序
- Analysis：气候影响分析程序
- CIRAPI：API服务器

WebAPP:  
在目录下使用 
> python -m http.server  

创建一个简单的http服务器，浏览器输入  
>http://localhost:8000/   

访问WebApp

CIRAPI  
API服务器，
在目录下使用 
> python pipenv run server.py  
  
启动api服务器 ，从云端数据库读取数据，调用Analysis模块进行分析
## Authors

* 任静静 北京大学物理学院大气与海洋科学系直博三年级学生，从事气溶胶遥感算法研究，擅长python matlab编程语言。
* 姜中景 北京大学物理学院大气与海洋科学系直博三年级学生，研究方向为大气化学，擅长matlab、ncl编程语言以及大气化学传输模式。
* 谭海月 北京大学物理学院大气与海洋科学系直博三年级学生，研究方向为大气化学，擅长数值模拟
* 房思勤 西安电子科技大学硕士，研究方向为区块链，擅长C++编程。
* 高镇 西安电子科技大学硕士，研究方向为计算机视觉，擅长C++编程。


