import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import heapq

class CampusMap:
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.load_users_from_file()
        self.vertices = {}
        self.edges = {}
        self.load_map_from_file()
        self.root = tk.Tk()
        self.selected_nodes = []
        self.nodes = {}

    # 从文件加载用户信息
    def load_users_from_file(self):
        try:
            with open("users.json", "r") as file:
                self.users = json.load(file)
        except FileNotFoundError:
            pass

    # 将用户信息保存到文件
    def save_users_to_file(self):
        with open("users.json", "w") as file:
            json.dump(self.users, file)

    # 将地图信息保存到文件
    def save_map_to_file(self):
        with open("campus_map.json", "w", encoding="utf-8") as file:
            map_data = {"vertices": self.vertices, "edges": self.edges}
            json.dump(map_data, file)

    # 从文件加载地图信息
    def load_map_from_file(self):
        try:
            with open("campus_map.json", "r", encoding="utf-8") as file:
                map_data = json.load(file)
                self.vertices = map_data.get("vertices", {})
                self.edges = map_data.get("edges", {})
        except FileNotFoundError:
            pass

    # 用户登录
    def login(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            print(f"用户 {username} 登录成功！")
        else:
            print("错误：用户名或密码不正确。")

    # 用户登出
    def logout(self):
        self.current_user = None
        print("用户已登出。")

    # 用户注册
    def register(self, username, password, user_type):
        if username not in self.users:
            self.users[username] = {"password": password, "type": user_type}
            self.save_users_to_file()
            print(f"用户 {username} 注册成功！")
        else:
            print("错误：用户名已存在。")

    # 注册界面
    def register_ui(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("注册")
        self.create_labeled_entry(register_window, "用户名:", 0)
        self.create_labeled_entry(register_window, "密码:", 1, show="*")
        self.create_labeled_entry(register_window, "用户类型（管理员/用户）:", 2)
        tk.Button(register_window, text="注册", command=lambda: self.handle_register(register_window)).grid(row=3, column=0, columnspan=2, pady=10)

    # 创建带标签的输入框
    def create_labeled_entry(self, window, label_text, row, show=None):
        tk.Label(window, text=label_text).grid(row=row, column=0, padx=10, pady=10)
        entry_var = tk.StringVar()
        tk.Entry(window, textvariable=entry_var, show=show).grid(row=row, column=1, padx=10, pady=10)
        return entry_var

    # 处理注册逻辑
    def handle_register(self, window):
        username = window.children['!entry'].get()
        password = window.children['!entry2'].get()
        user_type = window.children['!entry3'].get()
        if username and password and user_type:
            self.register(username, password, user_type)
            window.destroy()
        else:
            messagebox.showerror("错误", "所有字段都必须填写")

    # 登录界面
    def login_ui(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("登录")
        self.create_labeled_entry(login_window, "用户名:", 0)
        self.create_labeled_entry(login_window, "密码:", 1, show="*")
        error_label = tk.Label(login_window, text="", fg="red")
        error_label.grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(login_window, text="登录", command=lambda: self.handle_login(login_window, error_label)).grid(row=3, column=0, columnspan=2, pady=10)

    # 处理登录逻辑
    def handle_login(self, window, error_label):
        username = window.children['!entry'].get()
        password = window.children['!entry2'].get()
        if username and password:
            self.login(username, password)
            if self.current_user == username:
                window.destroy()
                self.user_menu_ui()
            else:
                error_label.config(text="账号或密码错误")
        else:
            error_label.config(text="所有字段都必须填写")

    # 计算最短路径
    def shortest_path(self, start, end):
        distances = {vertex: float('infinity') for vertex in self.vertices}
        distances[start] = 0
        priority_queue = [(0, start)]
        predecessors = {vertex: None for vertex in self.vertices}

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)
            if current_vertex == end:
                path = []
                while current_vertex is not None:
                    path.insert(0, current_vertex)
                    current_vertex = predecessors[current_vertex]
                return path, current_distance
            if current_distance > distances[current_vertex]:
                continue
            for neighbor, weight in self.edges.get(current_vertex, []):
                weight = int(weight) if weight is not None else 0
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))
        return None, float('infinity')

    # 查询路径
    def query_route(self, start, end):
        shortest_path, distance = self.shortest_path(start, end)
        if shortest_path:
            print(f"最短路径: {shortest_path}")
        else:
            print("未找到最短路径")
        return shortest_path, distance

    # 计算路径权重
    def calculate_path_weight(self, path):
        weight = 0
        for i in range(len(path) - 1):
            start, end = path[i], path[i + 1]
            edges = self.edges.get(start, [])
            for edge_end, edge_weight in edges:
                if edge_end == end:
                    weight += int(edge_weight) if edge_weight is not None else 0
                    break
        return weight

    # 登出并销毁窗口
    def logout_and_destroy(self, window):
        def logout():
            self.logout()
            window.destroy()
        return logout

    # 显示地图界面
    def view_map_ui(self, path=None):
        self.view_map_window = tk.Toplevel()
        self.view_map_window.title("校园导航系统")
        canvas_width = 800
        canvas_height = 600
        canvas = tk.Canvas(self.view_map_window, width=canvas_width, height=canvas_height)
        self.load_map_image(canvas, canvas_width, canvas_height)
        canvas.pack()
        self.create_control_buttons()
        self.create_toggle_buttons()
        self.layers = {
            "axis": path is None,
            "lines": path is None,
            "distances": path is None,
            "nodes": True,
            "node_names": True
        }
        self.refresh_map(canvas, path)

    # 加载地图图像
    def load_map_image(self, canvas, width, height):
        try:
            img = Image.open("map.png")
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            canvas.background = photo
            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        except Exception as e:
            print(f"无法加载背景图像: {e}")

    # 创建控制按钮
    def create_control_buttons(self):
        control_frame = tk.Frame(self.view_map_window)
        control_frame.pack(pady=10)
        buttons = [
            ("计算最短路径", self.calculate_shortest_path),
            ("查询节点信息", self.query_selected_node_info),
            ("删除节点", self.delete_selected_node),
            ("删除路径", self.delete_selected_route),
            ("添加节点", lambda: self.view_map_window.bind("<Button-1>", self.add_node)),
            ("添加路径", self.add_route_ui)
        ]
        for i, (text, command) in enumerate(buttons):
            tk.Button(control_frame, text=text, command=command).grid(row=i // 2, column=i % 2, padx=10, pady=5)

    # 创建切换按钮
    def create_toggle_buttons(self):
        toggle_frame = tk.Frame(self.view_map_window)
        toggle_frame.pack(pady=10)
        buttons = [
            ("坐标轴", "axis"),
            ("线路", "lines"),
            ("线路距离", "distances"),
            ("节点", "nodes"),
            ("节点名", "node_names"),
            ("刷新地图", self.refresh_map)
        ]
        for text, layer in buttons[:-1]:
            tk.Button(toggle_frame, text=text, command=lambda l=layer: self.toggle_layer(self.view_map_window.winfo_children()[0], l)).pack(side=tk.LEFT, padx=5)
        tk.Button(toggle_frame, text="刷新地图", command=self.refresh_map).pack(side=tk.LEFT, padx=5)

    # 切换图层
    def toggle_layer(self, canvas, layer):
        self.layers[layer] = not self.layers[layer]
        canvas.itemconfigure(layer, state="normal" if self.layers[layer] else "hidden")
        if layer == "lines" and not self.layers["lines"]:
            canvas.itemconfigure("distances", state="hidden")
            self.layers["distances"] = False
        elif layer == "nodes" and not self.layers["nodes"]:
            canvas.itemconfigure("node_names", state="hidden")
            self.layers["node_names"] = False
        self.refresh_map(canvas)

    # 刷新地图
    def refresh_map(self, canvas, path=None):
        self.load_map_from_file()
        self.load_map_image(canvas, 800, 600)
        self.draw_map_elements(canvas, path)

    # 绘制地图元素
    def draw_map_elements(self, canvas, path=None):
        if self.layers["axis"]:
            self.draw_axis(canvas)
        for vertex, data in self.vertices.items():
            x, y = data.get("position", (0, 0))
            self.draw_edges(canvas, vertex, x, y)
            self.draw_nodes(canvas, vertex, x, y)
        if path:
            self.highlight_path(canvas, path)

    # 绘制坐标轴
    def draw_axis(self, canvas):
        axis_length = 50
        canvas.create_line(0, 600 - axis_length, 800, 600 - axis_length, fill="black", tags="axis")
        canvas.create_line(axis_length, 600, axis_length, 0, fill="black", tags="axis")
        for i in range(0, 800, 100):
            canvas.create_line(i, 600 - axis_length - 5, i, 600 - axis_length + 5, fill="black", tags="axis")
            canvas.create_text(i, 600 - axis_length + 20, text=str(i), font=("Helvetica", 8), tags="axis")
        for i in range(0, 601, 100):
            y = 600 - i
            canvas.create_line(axis_length - 5, y, axis_length + 5, y, fill="black", tags="axis")
            canvas.create_text(axis_length - 20, y, text=str(600 - i), font=("Helvetica", 8), tags="axis")

    # 绘制边
    def draw_edges(self, canvas, vertex, x, y):
        for end, weight in self.edges.get(vertex, []):
            end_x, end_y = self.vertices[end]["position"]
            if self.layers["lines"]:
                canvas.create_line(x, y, end_x, end_y, tags="lines", fill="red")
            if self.layers["distances"]:
                canvas.create_text((x + end_x) / 2, (y + end_y) / 2, text=str(weight), font=("Helvetica", 8), tags="distances")

    # 绘制节点
    def draw_nodes(self, canvas, vertex, x, y):
        if self.layers["nodes"]:
            node_id = canvas.create_oval(x - 5, y - 5, x + 5, y + 5, tags="nodes", fill="yellow")
            self.nodes[vertex] = node_id
            canvas.tag_bind(node_id, '<Button-1>', lambda event, node_name=vertex: self.toggle_node(canvas, node_name))
        if self.layers["node_names"]:
            canvas.create_text(x, y + 10, text=vertex, font=("Helvetica", 8), tags="node_names", fill="blue")

    # 高亮路径
    def highlight_path(self, canvas, path):
        for i in range(len(path) - 1):
            start, end = path[i], path[i + 1]
            start_x, start_y = self.vertices[start]["position"]
            end_x, end_y = self.vertices[end]["position"]
            canvas.create_line(start_x, start_y, end_x, end_y, tags="lines", width=5, fill="blue")

    # 切换节点
    def toggle_node(self, canvas, node_name):
        node_id = self.nodes[node_name]
        if node_name in self.selected_nodes:
            canvas.itemconfig(node_id, fill="yellow")
            self.selected_nodes.remove(node_name)
        else:
            if len(self.selected_nodes) < 2:
                canvas.itemconfig(node_id, fill="red")
                self.selected_nodes.append(node_name)
            else:
                messagebox.showerror("错误", "最多只能选择两个节点")

    # 查询选中的节点信息
    def query_selected_node_info(self):
        if len(self.selected_nodes) == 1:
            node_name = self.selected_nodes[0]
            info = self.query_vertex(node_name)
            if info:
                position = info["position"]
                connections = info["connections"]
                connection_text = "\n".join([f"到 {neighbor}: {weight} 米" for neighbor, weight in connections])
                result = f"地点: {node_name}\n坐标: {position}\n连接的地点:\n{connection_text}"
                messagebox.showinfo("节点信息", result)
                self.selected_nodes = []
                self.refresh_map(self.view_map_window.winfo_children()[0])
            else:
                messagebox.showerror("错误", f"未找到节点 {node_name} 的信息")
        else:
            messagebox.showerror("错误", "请选择一个节点进行查询")

    # 删除选中的节点
    def delete_selected_node(self):
        if len(self.selected_nodes) == 1:
            node_name = self.selected_nodes[0]
            self.remove_location(node_name)
            self.save_map_to_file()
            self.selected_nodes = []
            self.refresh_map(self.view_map_window.winfo_children()[0])
        else:
            messagebox.showerror("错误", "请选择一个节点进行删除")

    # 删除选中的路径
    def delete_selected_route(self):
        if len(self.selected_nodes) == 2:
            start_node = self.selected_nodes[0]
            end_node = self.selected_nodes[1]
            self.remove_route(start_node, end_node)
            self.remove_route(end_node, start_node)
            self.save_map_to_file()
            self.selected_nodes = []
            self.refresh_map(self.view_map_window.winfo_children()[0])
        else:
            messagebox.showerror("错误", "请选择两个节点进行删除路径")

    # 添加节点
    def add_node(self, event):
        x, y = event.x, event.y
        add_node_window = tk.Toplevel(self.view_map_window)
        add_node_window.title("添加新节点")
        tk.Label(add_node_window, text="请输入新节点的名字:").pack(pady=10)
        node_name_var = tk.StringVar()
        tk.Entry(add_node_window, textvariable=node_name_var).pack(pady=10)

        def add_node_callback():
            node_name = node_name_var.get()
            if node_name:
                self.add_vertex(node_name, x, y, {"position": (x, y)})
                add_node_window.destroy()
                self.view_map_window.destroy()
                self.view_map_ui()
            else:
                messagebox.showerror("错误", "节点名称不能为空")

        tk.Button(add_node_window, text="添加", command=add_node_callback).pack(pady=10)

    # 计算最短路径
    def calculate_shortest_path(self):
        if len(self.selected_nodes) == 2:
            start_node = self.selected_nodes[0]
            end_node = self.selected_nodes[1]
            path, distance = self.shortest_path(start_node, end_node)
            if path:
                self.selected_nodes = []
                self.view_map_window.destroy()
                messagebox.showinfo("最短路径", f"从 {start_node} 到 {end_node} 的最短路径为: {path}, 距离为: {distance}")
                self.view_map_ui(path)
            else:
                messagebox.showerror("错误", "未找到从这两个节点的路径")
        else:
            messagebox.showerror("错误", "请选择两个节点进行计算")

    # 移除地点
    def remove_location(self, vertex_name):
        if vertex_name in self.vertices:
            del self.vertices[vertex_name]
            for start in self.edges:
                self.edges[start] = [(v, w) for v, w in self.edges[start] if v != vertex_name]
            print(f"地点撤销成功: {vertex_name}")
            self.save_map_to_file()
        else:
            print(f"错误：地点 {vertex_name} 不存在。")

    # 添加节点
    def add_vertex(self, vertex_name, x, y, data):
        data["position"] = (x, y)
        self.vertices[vertex_name] = data
        self.save_map_to_file()

    # 移除路径
    def remove_route(self, start, end):
        if start in self.edges:
            if end in [v for v, _ in self.edges[start]]:
                self.edges[start] = [(v, w) for v, w in self.edges[start] if v != end]
                print(f"路线撤销成功: {start} 到 {end}")
            else:
                print(f"错误：路径 {start} 到 {end} 不存在。")
        else:
            print(f"错误：起始地点 {start} 不存在。")

    # 添加路径界面
    def add_route_ui(self):
        if len(self.selected_nodes) == 2:
            add_route_window = tk.Toplevel(self.view_map_window)
            add_route_window.title("增加路径")
            tk.Label(add_route_window, text="请输入路径权重:").pack(pady=10)
            weight_var = tk.StringVar()
            tk.Entry(add_route_window, textvariable=weight_var).pack(pady=10)

            def add_route_callback():
                weight = weight_var.get()
                start, end = self.selected_nodes
                if weight:
                    self.add_route(start, end, weight)
                    self.add_route(end, start, weight)
                    add_route_window.destroy()
                    self.selected_nodes = []
                    self.view_map_window.destroy()
                    self.view_map_ui()
                else:
                    messagebox.showerror("错误", "路径权重不能为空")

            tk.Button(add_route_window, text="添加", command=add_route_callback).pack(pady=10)
        else:
            messagebox.showerror("错误", "请选择两个节点进行添加路径")

    # 添加路径
    def add_route(self, start, end, weight=None):
        if start in self.vertices and end in self.vertices:
            if end in [v for v, _ in self.edges.get(start, [])]:
                print(f"错误：路径 {start} 到 {end} 已存在。")
            else:
                self.add_edge(start, end, weight)
                print(f"路线添加成功: {start} 到 {end}")
        else:
            print(f"错误：起始地点 {start} 或目标地点 {end} 不存在。")

    # 添加边
    def add_edge(self, start, end, weight=None):
        if start not in self.edges:
            self.edges[start] = []
        self.edges[start].append((end, weight))
        self.save_map_to_file()

    # 查询节点信息
    def query_vertex(self, vertex_name):
        vertex_info = self.vertices.get(vertex_name)
        if not vertex_info:
            return None
        position = vertex_info.get("position", (0, 0))
        connections = self.edges.get(vertex_name, [])
        connected_vertices = [(neighbor, weight) for neighbor, weight in connections]
        return {"position": position, "connections": connected_vertices}

    # 用户菜单界面
    def user_menu_ui(self):
        self.view_map_ui()

    # 运行程序
    def run(self):
        self.root.withdraw()
        while True:
            if self.current_user is None:
                login_register_window = tk.Tk()
                login_register_window.title("登录")
                tk.Label(login_register_window, text="欢迎登录校园导航").pack(pady=20)
                tk.Button(login_register_window, text="登录", command=lambda: self.show_login_window(login_register_window)).pack(pady=10)
                tk.Button(login_register_window, text="注册", command=lambda: self.show_register_window(login_register_window)).pack(pady=10)
                tk.Button(login_register_window, text="退出系统", command=lambda: self.exit_system(login_register_window)).pack(pady=10)
                login_register_window.mainloop()

    # 显示登录窗口
    def show_login_window(self, window):
        self.login_ui()
        window.destroy()

    # 显示注册窗口
    def show_register_window(self, window):
        self.register_ui()
        window.destroy()

    # 退出系统
    def exit_system(self, window):
        print("感谢使用，再见！")
        window.destroy()

if __name__ == "__main__":
    campus_map = CampusMap()
    campus_map.run()
