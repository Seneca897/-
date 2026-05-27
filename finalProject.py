import tkinter as tk
from tkinter import filedialog, messagebox
import random

class GameOfLife:
    def __init__(self, root):
        """
        初始化生命游戏引擎与 GUI 界面
        【考点提示：面向对象(OOP)的类构建与初始化】
        """
        self.root = root
        self.root.title("康威生命游戏 (Conway's Game of Life) - 期末大作业")
        self.root.geometry("950x650")
        self.root.configure(bg="#2d2d2d")

        # 系统核心参数
        self.ROWS = 40        # 网格行数
        self.COLS = 60        # 网格列数
        self.CELL_SIZE = 15   # 细胞大小(像素)
        self.is_running = False
        self.speed = 100      # 迭代速度(毫秒)

        # 核心数据结构：二维列表(Matrix)记录细胞状态，0为死，1为生
        # 【考点提示：二维列表/矩阵的生成与控制】
        self.grid = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]

        self._build_ui()
        self.draw_grid()

    def _build_ui(self):
        """构建图形用户界面"""
        # 左侧控制面板
        control_frame = tk.Frame(self.root, bg="#2d2d2d", width=200)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        title_label = tk.Label(control_frame, text="控制面板", fg="white", bg="#2d2d2d", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # 按钮组 【考点提示：GUI事件绑定】
        tk.Button(control_frame, text="开始演化 (Start)", width=15, command=self.start).pack(pady=5)
        tk.Button(control_frame, text="暂停演化 (Pause)", width=15, command=self.pause).pack(pady=5)
        tk.Button(control_frame, text="随机生成 (Random)", width=15, command=self.randomize).pack(pady=5)
        tk.Button(control_frame, text="清空宇宙 (Clear)", width=15, command=self.clear).pack(pady=5)
        
        tk.Label(control_frame, text="--- 文件操作 ---", fg="gray", bg="#2d2d2d").pack(pady=15)
        tk.Button(control_frame, text="保存图纸 (Save)", width=15, command=self.save_to_file).pack(pady=5)
        tk.Button(control_frame, text="读取图纸 (Load)", width=15, command=self.load_from_file).pack(pady=5)

        # 右侧画布
        self.canvas = tk.Canvas(self.root, width=self.COLS * self.CELL_SIZE, height=self.ROWS * self.CELL_SIZE, bg="black", highlightthickness=1, highlightbackground="#3d3d3d")
        self.canvas.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # 绑定鼠标点击事件，允许用户用鼠标画出初始细胞
        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.canvas.bind("<B1-Motion>", self.toggle_cell) # 支持按住鼠标拖拽绘制

    def draw_grid(self):
        """将二维列表的逻辑状态渲染到画布上"""
        self.canvas.delete("all")
        for r in range(self.ROWS):
            for c in range(self.COLS):
                if self.grid[r][c] == 1:
                    x1 = c * self.CELL_SIZE
                    y1 = r * self.CELL_SIZE
                    x2 = x1 + self.CELL_SIZE
                    y2 = y1 + self.CELL_SIZE
                    # 极客配色：黑底亮绿
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#00FF00", outline="#003300")

    def toggle_cell(self, event):
        """处理鼠标点击事件，反转细胞状态"""
        c = event.x // self.CELL_SIZE
        r = event.y // self.CELL_SIZE
        if 0 <= r < self.ROWS and 0 <= c < self.COLS:
            self.grid[r][c] = 1 # 鼠标画过的地方变成活细胞
            self.draw_grid()

    def get_neighbors_count(self, r, c):
        """
        计算周围8个邻居的活细胞总数 (带边界环绕处理/拓扑环面)
        【考点提示：双层 for 循环，复杂的逻辑边界处理】
        """
        count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                # 拓扑环面：越界后从屏幕另一边穿出来 (类似吃豆人)
                nr = (r + i) % self.ROWS
                nc = (c + j) % self.COLS
                count += self.grid[nr][nc]
        return count

    def compute_next_generation(self):
        """
        算法核心引擎：计算下一代细胞状态
        【考点提示：深拷贝概念，核心业务逻辑的抽象】
        """
        # 创建一个全新的空白矩阵存放下一代
        next_grid = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        
        for r in range(self.ROWS):
            for c in range(self.COLS):
                alive_neighbors = self.get_neighbors_count(r, c)
                
                # 康威生命游戏三法则
                if self.grid[r][c] == 1: # 当前是活细胞
                    if alive_neighbors in [2, 3]:
                        next_grid[r][c] = 1 # 存活
                    else:
                        next_grid[r][c] = 0 # 孤独死或拥挤死
                else: # 当前是死细胞
                    if alive_neighbors == 3:
                        next_grid[r][c] = 1 # 繁衍
        
        self.grid = next_grid

    def run(self):
        """主循环定时器"""
        if self.is_running:
            self.compute_next_generation()
            self.draw_grid()
            # 利用 tkinter 的 after 方法实现非阻塞定时循环
            self.root.after(self.speed, self.run)

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.run()

    def pause(self):
        self.is_running = False

    def clear(self):
        self.is_running = False
        self.grid = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.draw_grid()

    def randomize(self):
        self.is_running = False
        # 【考点提示：随机数模块的使用】
        self.grid = [[random.choice([0, 0, 0, 1]) for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.draw_grid()

    def save_to_file(self):
        """
        将当前宇宙状态保存为 TXT 文本
        【考点提示：文件写入 (File Output) 与 异常处理 (try-except)】
        """
        self.pause()
        try:
            filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if filepath:
                with open(filepath, 'w', encoding='utf-8') as f:
                    for row in self.grid:
                        # 将列表 [1, 0, 1] 转换为字符串 "101" 存入文件
                        f.write("".join(map(str, row)) + "\n")
                messagebox.showinfo("成功", "图纸保存成功！")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {e}")

    def load_from_file(self):
        """
        从 TXT 文本读取宇宙状态
        【考点提示：文件读取 (File Input)】
        """
        self.pause()
        try:
            filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
            if filepath:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for r, line in enumerate(lines):
                        if r >= self.ROWS: break
                        line = line.strip()
                        for c, char in enumerate(line):
                            if c >= self.COLS: break
                            self.grid[r][c] = int(char)
                self.draw_grid()
        except Exception as e:
            messagebox.showerror("错误", f"读取图纸损坏或格式错误: {e}")

if __name__ == "__main__":
    # 启动 GUI 引擎
    root = tk.Tk()
    app = GameOfLife(root)
    root.mainloop()