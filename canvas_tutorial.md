# 北大Canvas 简明教程

2021/3/2 闫宏飞

北大Canvas网址，https://pku.instructure.com/

教师微信群：北大Canvas + Teams技术服务群（328）。加”guo-929“微信好友，邀请入群。



##  介绍

Canvas是北京大学为开课教师和选课学生提供的学习管理平台（Learning Management System, LMS）。Canvas已经与北大教务系统对接，开课教师登录进入后，可以看到自己的课程，可以自行添加、删除选课学生和助教。

Canvas中的课程内容是层级式展开，如图1所示，从选定一门课程开车，到课程内导航，到每周或者每次课程的单元导航。

```mermaid
graph LR
	subgraph 全局导航
        Course[课程] 
	end

    subgraph 课程导航
        Course--> Modules[...<br><br>作业<br><br>Studio<br><br>文件<br><br>单元<br><br>人员<br><br>公告<br><br>测验<br><br>...]
    end

    subgraph 单元导航
        Modules -->ModuleDetail[课前阅读<br><br>课堂直播地址<br><br>课件<br><br>课堂直播录像<br><br>作业]
    end
    classDef green fill:#9f6,stroke:#333,stroke-width:2px;
    class ModulesDetail green
```
​														图1. Canvas中的课程内容层级式展开



教师或者助教可以在Canvas中，安排每周课程（在Canvas中称为单元），布置及批改作业，发布公告，和录制微课件。

学生可以在Canvas中看到每周课程安排（如：课前预习资料、课件、课堂直播地址等），提交作业及查看教师反馈。

如图2所示，访问Canvas https://pku.instructure.com/ 。如图3所示，登录进入Canvas.

<img src="https://i.loli.net/2021/02/26/xUYblP7ro1eKh5g.png" alt="image-20210226202127789" style="zoom: 33%;" />

​														图2. 访问Canvas中



<img src="https://i.loli.net/2021/02/26/yOkC8u6PK3mDT9Q.png" alt="image-20210226202250481"  />

​															图3. 登录进入Canvas

## 课程设置

可参考：如何使用 Canvas 设置课程，https://zh.guides.instructure.com/m/11077/l/1099124-canvas

### 2.1 打开一门课程

请点击全局导航 (Global Navigation) 中的**课程 (Courses)** 链接 。然后点击您想查看的课程的名称。

<img src="https://i.loli.net/2021/02/26/y9XUzgHL6FGEu3V.png" alt="查看课程首页" style="zoom:50%;" />

​																图4. 打开一门课程



<img src="https://i.loli.net/2021/02/26/CROKbMhc4QSHToI.png" alt="查看教程" style="zoom:80%;" />

​											图5. 进入单元设置



### 2.2 安排每周或者每次课程（单元）

![image-20210226231135493](https://i.loli.net/2021/02/26/eMbTVNrfgEpm3Wn.png)

​				图6. a) 随着课程推进，单元内容呈现								b) 设置课程主页为课程单元



###  2.3 针对一个具体单元的设置

单元可以增加、删除、移动。单元中包含的网页、作业，也可以增删改。

<img src="https://i.loli.net/2021/02/27/WPU2lGn3ehZoB7i.png" alt="image-20210227001952482" style="zoom:50%;" />

​															图7. 具体一个课程单元的设置



## 布置及批改作业



<img src="https://i.loli.net/2021/02/27/Ibxf4gK1kTuwJcR.png" alt="image-20210227141700737" style="zoom:67%;" />

​														图8. 布置作业



<img src="https://i.loli.net/2021/02/27/Xsrg6RveWMUBxyI.png" alt="image-20210227141813309" style="zoom:67%;" />

​												图9. 点开一次作业



<img src="https://i.loli.net/2021/02/27/j13lHw7YLChrzWe.png" alt="image-20210227141956621" style="zoom:67%;" />

​											图10. 批改一份作业



## 利用Studio制作微课件

大家可以先观看Canvas一小时入门培训录像（主讲：沈倩宜 Dorin Shen，2020年2月8日），在“Growing with Canvas”课程中。

其中最重要的，最主要的是5分钟视频，利用Studio制作微课件。

Screen Capture Demo, https://pku.instructuremedia.com/embed/9cf7145a-abd9-4418-a5ff-5dcfed2e2f8f



<img src="https://i.loli.net/2021/02/27/BgaTYeVmARuEy9U.png" alt="image-20210227141355317" style="zoom:67%;" />

​								图11. 利用Studio制作微课件



## 参考

[1]. Canvas中文指南，https://zh.guides.instructure.com/

[2]. Draw Diagrams With Markdown, https://support.typora.io/Draw-Diagrams-With-Markdown/



## 附录1. 课堂直播（会议系统）

课堂直播可以使用Teams，或者腾讯会议。上课时候，在教室中开启一个直播会议系统就可以，会议网址可以放在放在课程网站中。

<img src="https://i.loli.net/2021/02/27/4mCEKrwQTsfWdZj.png" alt="image-20210227144421128" style="zoom: 50%;" />

​										图12. 课堂直播 