# Campus-Navigation
以杭州电子科技大学地图为例制作的校园导航（以下是我的课程作业的项目报告的部分内容）  
# 一、搜索问题介绍  
背景：
缺德地图开课啦！大学生上课老迷路，多半是忘了，用校园导航找路径，路最短，防止学校迷路，大学生一定要记住哦！  
搜索对象： 
一个包含学校各个节点以路径的地图  
 ![image](https://github.com/user-attachments/assets/54d3f56e-d69b-4052-b280-717eda1a9d1f)


搜索目标：
一条能够通向起点和终点的最短路  
# 二、算法原理介绍
Dijkstra算法  
Dijkstra算法是一种用于在加权图中查找从一个起始节点到所有其他节点的最短路径的算法。该算法最初由荷兰计算机科学家Edsger W. Dijkstra于1956年提出。Dijkstra算法适用于带有非负权重的有向图或无向图。
特点和限制：
Dijkstra算法仅适用于非负权重的图，因为它依赖于贪婪策略来选择当前最短路径。
它可以找到从起始节点到所有其他节点的最短路径，因此适用于单源最短路径问题。
Dijkstra算法不会处理负权边，如果图中存在负权边，应该使用其他算法，如Bellman-Ford算法。
算法的时间复杂度取决于数据结构的选择，一般情况下是O(V^2)或O(Vlog(V))，其中V是节点数。如果使用优先队列来优化，时间复杂度可以减小到O(Elog(V))，其中E是边数。
Dijkstra算法在许多领域广泛应用，包括路线规划、网络路由、资源分配和许多其他需要找到最短路径的应用。  
Dijkstra算法的步骤  
1.	创建一个空的最短路径字典，其中每个节点的距离设置为无穷大，起始节点的距离设置为0。
2.	创建一个空的已访问节点集合。
3.	从未访问的节点中选择距离起始节点最近的节点，标记为已访问。
4.	对于已访问节点的所有邻居，计算通过已访问节点到达它们的距离，并更新最短路径字典。
5.	重复步骤3和4，直到所有节点都被访问。

# 三、程序编写与调试说明
参照航电地图手动绘制了一个地图（耗时5h）                                   
85个节点  
![image](https://github.com/user-attachments/assets/48c750a9-e1f4-4186-975a-b45656b4ed0c)  
不少于500条边  
![image](https://github.com/user-attachments/assets/120451e5-4ac8-45c9-89b1-5d50b754529a)  

 
四、程序介绍
使用tkinter制作了一个应用界面，包含
登录界面：
可选择登录，注册及退出系统，注册后的账号和密码将存储在本地文件中
 ![image](https://github.com/user-attachments/assets/6796b39b-9571-4c6a-984c-c034d7dab92c)![image](https://github.com/user-attachments/assets/52265795-af2d-410a-b5ba-44fff2843d70)  
应用界面：  
![image](https://github.com/user-attachments/assets/66fa253f-6ff3-4c83-8c90-53005cecd3ba)  

节点选择功能  
可通过点击黄色的节点来选中1-2个节点，选中后节点会变红，再次点击又会取消选中  
  ![image](https://github.com/user-attachments/assets/d140d05f-50d6-4491-b54a-49c4f601c112)![image](https://github.com/user-attachments/assets/5e26c54e-878e-4f8a-ad6c-8e47c2888dac)  
当一个节点被选中时可执行节点查询，和删除节点的操作，  
两个节点被选中时，可执行计算最短路，增删路径的功能  

节点查询  
可以查询某节点的位置和与其相连的地点和距离  
 ![image](https://github.com/user-attachments/assets/0ba89519-0913-4792-ab17-a7f02574fa9c)  
 
插入节点  

![image](https://github.com/user-attachments/assets/7441f86a-0eb6-40f3-ba07-a1b621989686)![image](https://github.com/user-attachments/assets/4be5e85c-3e23-4dd3-b0af-bb23dcc90840)  


插入路径  
![image](https://github.com/user-attachments/assets/5dd55c7b-16af-4a7c-b094-3eb30d4253f5)![image](https://github.com/user-attachments/assets/a24706d9-475a-4e92-93fa-c779e93e446b)  


删除节点  
![image](https://github.com/user-attachments/assets/5b1d6bcd-6169-448d-adf2-ababeb85236d)![image](https://github.com/user-attachments/assets/ee7fe26b-c1b8-43a4-88ed-9f4a3eaacc83)  

 
删除路径  
![image](https://github.com/user-attachments/assets/d390bc44-8ab6-455a-b725-7266e8a968e3)![image](https://github.com/user-attachments/assets/8339cbd6-342d-4dae-bffa-0e605ac41a7e)


地图显示  
地图下方的6个按键中，前五个表示可选择为显示或者隐藏  
刷新地图则是在地图文件中修改了地图后点击刷新地图即可显示修改后的地图  
![图片1](https://github.com/user-attachments/assets/ccb4ba37-750b-4590-b4fd-1d5a75a74f24)  


最短路查询  
选中起点和终点后，再点击计算最短路径，程序便会用Dijkstra算法计算出最短路径，并显示出路径，同时弹出地图并显示具体路径。  
 ![image](https://github.com/user-attachments/assets/0dba2a15-80ce-4303-aa95-0134e4cba547)  
![image](https://github.com/user-attachments/assets/69a107a2-fe1d-4f77-8fa6-0a0cee80bc77)  

 

