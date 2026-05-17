#!/usr/bin/env python3
"""
API接口测试工具 - 发送HTTP请求测试API
"""
import sys, json, tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import urllib.request
import urllib.error

class App:
    def __init__(self, root):
        self.root = root
        root.title("API测试工具 v1.0")
        root.geometry("900x700")
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#1565c0", height=50)
        f.pack(fill="x")
        tk.Label(f, text="🔌 API测试工具", font=("Arial",14,"bold"),
                 fg="white", bg="#1565c0").pack(pady=12)
        
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        
        # 请求配置
        cf = tk.Frame(main)
        cf.pack(fill="x", pady=5)
        
        tk.Label(cf, text="方法：").pack(side="left")
        self.method = ttk.Combobox(cf, values=["GET","POST","PUT","DELETE","PATCH"],
                                    state="readonly", width=8)
        self.method.set("GET")
        self.method.pack(side="left", padx=5)
        
        tk.Label(cf, text="URL：").pack(side="left", padx=(10,5))
        self.url_entry = tk.Entry(cf, font=("Arial",11), width=50)
        self.url_entry.pack(side="left", padx=5)
        self.url_entry.insert(0, "https://api.github.com")
        
        tk.Button(cf, text="发送请求", command=self.send_request,
                  bg="#4caf50", fg="white", font=("Arial",10,"bold"),
                  padx=15).pack(side="left", padx=15)
        
        # Headers
        hf = tk.LabelFrame(main, text="Headers（每行一个，格式：key: value）", padx=5, pady=5)
        hf.pack(fill="x", pady=5)
        self.headers_txt = tk.Text(hf, height=3, font=("Consolas",9))
        self.headers_txt.pack(fill="x")
        self.headers_txt.insert(1.0, "User-Agent: API-Test-Tool/1.0\nAccept: application/json")
        
        # Body
        bf = tk.LabelFrame(main, text="请求Body（JSON格式）", padx=5, pady=5)
        bf.pack(fill="x", pady=5)
        self.body_txt = tk.Text(bf, height=5, font=("Consolas",10), bg="#e3f2fd")
        self.body_txt.pack(fill="x")
        
        # 响应
        tk.Label(main, text="响应结果：", font=("Arial",10,"bold")).pack(anchor="w", pady=(10,5))
        self.response_txt = scrolledtext.ScrolledText(main, font=("Consolas",10),
                                                       height=15, wrap="word")
        self.response_txt.pack(fill="both", expand=True)
        
        # 状态栏
        self.status = tk.Label(main, text="输入URL后点击「发送请求」",
                               font=("Arial",10), fg="gray")
        self.status.pack(anchor="w")
    
    def send_request(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("提示", "请输入URL")
            return
        
        method = self.method.get()
        headers = {}
        for line in self.headers_txt.get(1.0, "end").strip().split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip()] = v.strip()
        
        body = self.body_txt.get(1.0, "end").strip() if method in ["POST","PUT","PATCH"] else None
        
        try:
            self.status.config(text="请求中...")
            self.root.update()
            
            req = urllib.request.Request(url, method=method, headers=headers)
            if body:
                req.data = body.encode("utf-8")
                if "Content-Type" not in headers:
                    req.add_header("Content-Type", "application/json")
            
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = resp.read().decode("utf-8")
                status = resp.status
                resp_headers = dict(resp.headers)
            
            # 格式化JSON响应
            try:
                data = json.loads(result)
                result = json.dumps(data, indent=2, ensure_ascii=False)
            except:
                pass
            
            self.response_txt.delete(1.0, "end")
            self.response_txt.insert(1.0, f"状态码：{status}\n\n{result}")
            self.status.config(text=f"✅ 响应成功（{status}）")
            
        except urllib.error.HTTPError as e:
            self.response_txt.delete(1.0, "end")
            self.response_txt.insert(1.0, f"HTTP错误：{e.code}\n{e.read().decode()}")
            self.status.config(text=f"❌ HTTP {e.code}")
        except Exception as e:
            self.response_txt.delete(1.0, "end")
            self.response_txt.insert(1.0, f"请求失败：{str(e)}")
            self.status.config(text="❌ 请求失败")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
