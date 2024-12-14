import tkinter.messagebox as ctk_messagebox
import customtkinter as ctk
import os
import subprocess
import shutil
import threading


class PyinstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pyinstaller GUI工具")
        
        # 文件夹路径
        self.folder_label = ctk.CTkLabel(root, text="文件夹路径:")
        self.folder_label.configure(font=('HarmonyOS Sans SC Black', 15, 'bold'))  # 增加文本大小
        self.folder_label.grid(row=0, column=0, padx=5, pady=10)
        self.folder_path = ctk.StringVar()
        self.folder_entry = ctk.CTkEntry(root, textvariable=self.folder_path, width=260)  # 增加路径区宽度
        self.folder_entry.grid(row=0, column=1, padx=5, pady=10)
        self.browse_folder_button = ctk.CTkButton(root, text="浏览", command=self.browse_folder, width=32)  # 按钮宽度
        self.browse_folder_button.configure(font=('HarmonyOS Sans SC Black', 15, 'bold'))  # 增加文本大小
        self.browse_folder_button.grid(row=0, column=2, padx=10, pady=5)
        
        # Python文件名
        self.py_file_label = ctk.CTkLabel(root, text="PY文件:")
        self.py_file_label.configure(font=('HarmonyOS Sans SC Black', 15, 'bold'))  # 增加文本大小
        self.py_file_label.grid(row=1, column=0, padx=5, pady=10)
        self.py_file = ctk.StringVar()
        self.py_file_entry = ctk.CTkEntry(root, textvariable=self.py_file, width=260)  # 增加路径区宽度
        self.py_file_entry.grid(row=1, column=1, padx=5, pady=10)
        self.browse_py_button = ctk.CTkButton(root, text="浏览", command=self.browse_py, width=32)  # 按钮宽度
        self.browse_py_button.configure(font=('HarmonyOS Sans SC Black', 15, 'bold'))  # 增加文本大小
        self.browse_py_button.grid(row=1, column=2, padx=5, pady=10)
        
        # 图标文件名
        self.ico_file_label = ctk.CTkLabel(root, text="图标文件:")
        self.ico_file_label.configure(font=('HarmonyOS Sans SC Black', 15, 'bold'))  # 增加文本大小
        self.ico_file_label.grid(row=2, column=0, padx=5, pady=10)
        self.ico_file = ctk.StringVar()
        self.ico_file_entry = ctk.CTkEntry(root, textvariable=self.ico_file, width=260)  # 增加路径区宽度
        self.ico_file_entry.grid(row=2, column=1, padx=5, pady=10)
        self.browse_ico_button = ctk.CTkButton(root, text="浏览", command=self.browse_ico, width=32)  # 按钮宽度
        self.browse_ico_button.configure(font=('HarmonyOS Sans SC Black', 15, 'bold'))  # 增加文本大小
        self.browse_ico_button.grid(row=2, column=2, padx=5, pady=10)
        
        # 进度条
        self.progress = ctk.CTkProgressBar(root, width=300, height=14, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=3, pady=10, padx=5, sticky='ew')
        self.progress['value'] = 0  # 初始时隐藏进度条
        self.progress.grid_remove()  # 初始时不显示进度条
        
        # 生成按钮
        self.generate_exe_button = ctk.CTkButton(root, text="           生成EXE              ", command=self.generate_exe_thread, width=30)  # 增加生成按钮宽度
        self.generate_exe_button.configure(font=('HarmonyOS Sans SC Black', 24, 'bold'))  # 增加生成按钮文本大小
        self.generate_exe_button.grid(row=4, column=1, pady=13)  # 使按钮居中

    def browse_folder(self):
        folder_selected = ctk.filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def browse_py(self):
        file_selected = ctk.filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_selected:
            self.py_file.set(os.path.basename(file_selected))
            self.folder_path.set(os.path.dirname(file_selected))

    def browse_ico(self):
        file_selected = ctk.filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")])
        if file_selected:
            self.ico_file.set(os.path.basename(file_selected))

    def generate_exe_thread(self):
        self.generate_exe_button.grid_remove()  # 隐藏生成按钮
        thread = threading.Thread(target=self.generate_exe)
        thread.start()

    def generate_exe(self):
        folder = self.folder_path.get()
        py_file = self.py_file.get()
        ico_file = self.ico_file.get()
        
        if not all([folder, py_file, ico_file]):
            ctk_messagebox.showwarning("错误", "请填写所有必要信息！")
            self.generate_exe_button.grid()  # 显示生成按钮
            return
            
        try:
            self.progress.grid()  # 显示进度条
            self.progress.start()
            os.chdir(folder)
            
            python_path = os.path.dirname(os.path.dirname(subprocess.__file__))
            scripts_path = os.path.join(python_path, 'Scripts')
            pyinstaller_path = os.path.join(scripts_path, 'pyinstaller.exe')
            
            if not os.path.exists(pyinstaller_path):
                self.progress.stop()
                self.progress.grid_remove()  # 隐藏进度条
                self.generate_exe_button.grid()  # 显示生成按钮
                ctk_messagebox.showerror("错误", "找不到pyinstaller，请确保已正确安装！\n可以尝试运行: pip install pyinstaller")
                return
                
            full_command = f'"{pyinstaller_path}" --onefile --windowed --icon="{ico_file}" "{py_file}"'
            
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            process = subprocess.Popen(
                full_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=startupinfo,
                universal_newlines=True
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                for item in os.listdir(folder):
                    if item != 'dist' and item != py_file and item != ico_file and (os.path.isfile(os.path.join(folder, item)) or item == 'build'):
                        try:
                            if os.path.isfile(os.path.join(folder, item)):
                                os.remove(os.path.join(folder, item))
                            else:
                                shutil.rmtree(os.path.join(folder, item))
                        except Exception as e:
                            print(f"无法删除 {item}: {str(e)}")
                
                self.progress.stop()
                self.progress.grid_remove()  # 隐藏进度条
                self.generate_exe_button.grid()  # 显示生成按钮
                ctk_messagebox.showinfo("成功", "EXE文件生成成功！已清理临时文件。")
            else:
                self.progress.stop()
                self.progress.grid_remove()  # 隐藏进度条
                self.generate_exe_button.grid()  # 显示生成按钮
                error_msg = stderr if stderr else stdout
                if not error_msg:
                    error_msg = "未知错误，请检查:\n1. pyinstaller是否正确安装\n2. 文件路径是否包含特殊字符\n3. 是否有足够的权限"
                ctk_messagebox.showerror("错误", f"生成失败！\n命令: {full_command}\n\n错误信息：\n{error_msg}")
                
        except Exception as e:
            self.progress.stop()
            self.progress.grid_remove()  # 隐藏进度条
            self.generate_exe_button.grid()  # 显示生成按钮
            ctk_messagebox.showerror("错误", f"发生错误：\n{str(e)}\n\n请确保:\n1. 已安装pyinstaller\n2. 有管理员权限\n3. 文件路径正确")

if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # 设置外观模式
    ctk.set_default_color_theme("blue")  # 设置默认颜色主题
    root = ctk.CTk()
    app = PyinstallerGUI(root)
    root.mainloop()
