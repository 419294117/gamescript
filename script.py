import tkinter as tk
from threading import Thread
import pyautogui
import time
import random
import pygetwindow as gw
from pynput.mouse import Listener
from pynput.keyboard import Key, Controller
import tkinter.messagebox as messagebox
from queue import Queue

# 主函数，执行点击操作
def main(points_a_str, points_b_str, min_sleep, max_sleep, window_title, running):
    # 解析多个坐标点
    def parse_points(points_str):
        points = []
        for point_str in points_str.split(';'):
            x, y = map(int, point_str.split(','))
            points.append((x, y))
        return points

    points_a = parse_points(points_a_str.get())
    points_b = parse_points(points_b_str.get())
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        if window:
            window.activate()
    except IndexError:
        print(f"没有找到标题为 '{window_title}' 的窗口。")
        return

    def click_point(point):
        pyautogui.click(point)

    def random_sleep():
        time.sleep(random.uniform(min_sleep, max_sleep))

    while running[0]:
        point_a = random.choice(points_a)
        point_b = random.choice(points_b)

        click_point(point_a)
        random_sleep()
        click_point(point_b)
        random_sleep()

# GUI界面
def gui():
    root = tk.Tk()
    root.title("自动点击器")
    # 设置窗口的宽度和高度
    root.geometry("600x800")  # 例如，500像素宽和400像素高

    # 输入字段
    points_a = tk.StringVar()
    points_b = tk.StringVar()
    min_sleep = tk.StringVar()
    max_sleep = tk.StringVar()
    window_title = tk.StringVar()
    strings_var = tk.StringVar()  # 新增：用于输入的字符串变量

    # 创建一行输入框和按钮 target.png
    def create_point_row(label_text, points_var):
        frame = tk.Frame(root)
        tk.Label(frame, text=label_text).pack(side=tk.LEFT)
        entry = tk.Entry(frame, textvariable=points_var)
        entry.pack(side=tk.LEFT)
        button = tk.Button(frame, text="获取位置", command=lambda: get_position(points_var, root, window_title.get()))
        button.pack(side=tk.LEFT)
        frame.pack()

    msg_queue = Queue()

    def show_message():
        while True:
            msg = msg_queue.get()
            if msg == "stop":
                break
            messagebox.showerror("错误", msg, parent=root)

    # 获取鼠标位置的函数
    def get_position(points_var, root, window_title):
        def on_click(x, y, button, pressed):
            if pressed:
                try:
                    current_window = gw.getWindowsAt(x, y)[0]
                    print(f"当前的窗口是：{current_window.title}")
                    if current_window.title == window_title:
                        current_points = points_var.get()
                        new_point = f"{x},{y}"
                        # 如果已经有坐标，则添加新坐标，否则直接设置新坐标
                        if current_points:
                            points_var.set(current_points + ';' + new_point)
                        else:
                            points_var.set(new_point)
                    else:
                        msg_queue.put("点击位置不在指定窗口内！")
                except IndexError:
                    msg_queue.put("未检测到窗口！")
                return False  # 停止监听

        def start_listener():
            with Listener(on_click=on_click) as listener:
                listener.join()

        # 在新线程中启动鼠标监听
        listener_thread = Thread(target=start_listener)
        listener_thread.start()

    Thread(target=show_message).start()

    create_point_row("Point A (x1,y1;x2,y2;...):", points_a)
    create_point_row("Point B (x1,y1;x2,y2;...):", points_b)

    tk.Label(root, text="最小随机数:").pack()
    tk.Entry(root, textvariable=min_sleep).pack()
    tk.Label(root, text="最大随机数:").pack()
    tk.Entry(root, textvariable=max_sleep).pack()
    tk.Label(root, text="程序名字:").pack()
    tk.Entry(root, textvariable=window_title).pack()
    tk.Label(root, text="向聊天框发送随机消息:").pack()
    tk.Entry(root, textvariable=strings_var).pack()

    # 控制变量
    running = [False]
    thread = [None]
    task_thread = [None]  # 新增：随机任务的线程

    # 开始和结束函数
    def start():
        if not running[0]:
            running[0] = True
            min_s = float(min_sleep.get())
            max_s = float(max_sleep.get())
            title = window_title.get()

            # 启动主线程
            thread[0] = Thread(target=main, args=(points_a, points_b, min_s, max_s, title, running))
            thread[0].start()

            # 如果需要，启动任务线程
            # if task_thread[0] is None:
            #     task_thread[0] = Thread(target=随机任务函数, args=(其他参数))
            #     task_thread[0].start()

    def stop():
        running[0] = False
        # if thread[0]:
        #     thread[0].join()
        # if task_thread[0]:  # 新增：停止随机任务线程
        #     task_thread[0].join()

    # 按钮
    tk.Button(root, text="开始", command=start).pack()
    tk.Button(root, text="结束", command=stop).pack()

    root.mainloop()

if __name__ == "__main__":
    gui()
