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

class ImageApp:
    def __init__(self, master):
        self.master = master
        self.master.title("隨機圖片顯示器")
        
        # 取得所有 .png 檔案路徑
        self.image_files = self.load_images_from_folder("img")
        if not self.image_files:
            print("錯誤: 'img' 資料夾中沒有找到任何 .png 檔案。")
            self.master.destroy()
            return

        # 隨機打亂圖片順序
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

        # 建立一個標籤來顯示圖片
        self.image_label = tk.Label(self.master, bg="black")
        self.image_label.pack(expand=True)

        # 綁定空白鍵事件
        self.master.bind("<space>", self.show_next_image)

        # 顯示第一張圖片
        self.show_next_image()

    def load_images_from_folder(self, folder):
        """
        載入指定資料夾中所有 .png 圖檔的路徑。
        """
        if not os.path.isdir(folder):
            print(f"錯誤: 找不到資料夾 '{folder}'。")
            return []
        
        file_paths = []
        for filename in os.listdir(folder):
            if filename.lower().endswith(".png"):
                file_paths.append(os.path.join(folder, filename))
        return file_paths

    def shuffle_images(self):
        """
        重新打亂圖片順序並重置索引。
        """
        random.shuffle(self.image_files)
        self.current_image_index = 0

    def show_next_image(self, event=None):
        """
        顯示下一張隨機圖片。
        """
        # 如果所有圖片都已顯示過，則重新打亂順序並從頭開始
        if self.current_image_index >= len(self.image_files):
            print("所有圖片都已顯示過，將重新產生新的隨機順序。")
            self.shuffle_images()

        # 載入並調整圖片大小
        image_path = self.image_files[self.current_image_index]
        image = Image.open(image_path)
        
        # 保持長寬比調整圖片大小，以適應 600x110 的圖框
        original_width, original_height = image.size
        target_width, target_height = 600, 110
        
        ratio_w = target_width / original_width
        ratio_h = target_height / original_height
        
        ratio = min(ratio_w, ratio_h)
        
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # 建立 Tkinter 圖片物件並顯示
        tk_image = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image  # 保持引用，防止垃圾回收

        # 更新索引，準備顯示下一張
        self.current_image_index += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()