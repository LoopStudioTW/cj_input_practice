# v2_202508170605
# 新增功能
# 1. 圖片下方新增一行文字，作為答對與答錯的顯示
#   - 文字位置：垂直位置，在圖片下方半行字高；水平位置，對齊畫面中央
# 2. 當使用者按下鍵盤按鍵，如果按鍵的英文字母(例如：a)，和圖片第一個英文字母相同(例如：a_1.png)，
#   - 圖片下方文字：顯示答對(綠字)，以及英文字母和其對應的倉頡字根(例：答對，A(日))，
#   - 圖片：在答對的狀態下，鍵盤按任意鍵，就換下一張圖
# 3. 圖片大小保持一致，圖片顯示的區域有一個固定的尺寸
# 4. (AI自動加入)答錯
#   - 圖片下方文字：顯示「答錯！(紅字)」，並停留在同一圖片，等待使用者新的輸入
# 5. (AI自動加入)按鍵非英文字母
#   - 圖片下方文字：顯示「請按英文字母鍵」

# init_v1
# 寫一個python程式
# 1. 顯示一個視窗
# 2. 載入img資料夾中所有.png圖檔
# 3. 視窗中間有一個600x110大小的圖匡
# 4. 不重複隨機顯示載入的圖檔
# 5. 當使用者按下鍵盤的空白鍵，就換下一張圖
# 如果全部圖片都顯示過，就重頭來過，並且產生新的隨機順序

import tkinter as tk
from PIL import Image, ImageTk
import os
import random

# 定義英文字母與倉頡字根的對應字典
CJ_ROOTS = {
    'a': '日', 'b': '月', 'c': '金', 'd': '木', 'e': '水',
    'f': '火', 'g': '土', 'h': '竹', 'i': '戈', 'j': '十',
    'k': '大', 'l': '中', 'm': '一', 'n': '弓', 'o': '人',
    'p': '心', 'q': '手', 'r': '口', 's': '尸', 't': '廿',
    'u': '山', 'v': '女', 'w': '田', 'x': '難', 'y': '卜',
    'z': '重'
}

class ImageApp:
    def __init__(self, master):
        self.master = master
        self.master.title("倉頡字根練習")
        
        # 載入所有圖片並隨機排序
        self.image_files = self.load_images_from_folder("img")
        if not self.image_files:
            print("錯誤: 'img' 資料夾中沒有找到任何 .png 檔案。")
            self.master.destroy()
            return
        
        self.is_correct = False
        self.shuffle_images()

        # 設定視窗大小與位置
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 800
        window_height = 600
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.master.configure(bg="black")

        # 建立一個 Frame 作為圖片和文字的容器
        container = tk.Frame(self.master, bg="black")
        container.pack(expand=True)
        
        # 圖片顯示區塊
        # 解決方案：設定固定大小的寬度(width)和高度(height)
        self.image_label = tk.Label(container, bg="black", width=600, height=110)
        self.image_label.pack(pady=(0, 20))
        
        # 文字顯示區塊
        self.text_label = tk.Label(container, text="", font=("Helvetica", 24, "bold"), fg="white", bg="black")
        self.text_label.pack()

        # 綁定所有鍵盤按鍵事件
        self.master.bind("<Key>", self.handle_keypress)

        # 顯示第一張圖片
        self.show_next_image()

    def load_images_from_folder(self, folder):
        if not os.path.isdir(folder):
            print(f"錯誤: 找不到資料夾 '{folder}'。")
            return []
        
        file_paths = []
        for filename in os.listdir(folder):
            if filename.lower().endswith(".png"):
                file_paths.append(os.path.join(folder, filename))
        return file_paths

    def shuffle_images(self):
        random.shuffle(self.image_files)
        self.current_image_index = 0

    def show_next_image(self):
        if self.current_image_index >= len(self.image_files):
            print("所有圖片都已顯示過，將重新產生新的隨機順序。")
            self.shuffle_images()

        image_path = self.image_files[self.current_image_index]
        image = Image.open(image_path)
        
        original_width, original_height = image.size
        target_width, target_height = 600, 110
        
        ratio_w = target_width / original_width
        ratio_h = target_height / original_height
        ratio = min(ratio_w, ratio_h)
        
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        
        tk_image = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image

        self.text_label.config(text="")
        self.is_correct = False
        
        self.current_image_index += 1

    def handle_keypress(self, event):
        if self.is_correct:
            self.show_next_image()
        else:
            current_image_path = self.image_files[self.current_image_index - 1]
            filename = os.path.basename(current_image_path)
            first_char = filename[0].lower()

            pressed_key = event.char.lower()
            
            if 'a' <= pressed_key <= 'z':
                if pressed_key == first_char:
                    cj_root = CJ_ROOTS.get(first_char, '')
                    self.text_label.config(text=f"答對！ {first_char.upper()}({cj_root})", fg="green")
                    self.is_correct = True
                else:
                    self.text_label.config(text="答錯！", fg="red")
            else:
                self.text_label.config(text="請按英文字母鍵。", fg="yellow")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()