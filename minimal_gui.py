"""
최소한의 의존성으로 작성된 네이버 블로그 자동 작성기
EXE 생성을 위한 간소화된 버전
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import time
import os
import sys
import subprocess
import requests
import json

class MinimalBlogWriter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("네이버 블로그 자동 작성기 (간소 버전)")
        self.root.geometry("700x500")
        self.root.configure(bg='#f0f0f0')
        
        self.create_widgets()
        self.center_window()
    
    def create_widgets(self):
        # 제목
        title_label = tk.Label(self.root, 
                              text="🚀 네이버 블로그 자동 작성기",
                              font=('맑은 고딕', 16, 'bold'),
                              fg='#2E86AB',
                              bg='#f0f0f0')
        title_label.pack(pady=20)
        
        # 로그인 정보 프레임
        login_frame = tk.LabelFrame(self.root, 
                                   text="로그인 정보",
                                   font=('맑은 고딕', 12, 'bold'),
                                   bg='white')
        login_frame.pack(fill='x', padx=20, pady=10)
        
        # 아이디
        tk.Label(login_frame, text="네이버 아이디:", 
                font=('맑은 고딕', 10), bg='white').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.id_entry = tk.Entry(login_frame, font=('맑은 고딕', 10), width=30)
        self.id_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # 비밀번호
        tk.Label(login_frame, text="비밀번호:", 
                font=('맑은 고딕', 10), bg='white').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.pw_entry = tk.Entry(login_frame, font=('맑은 고딕', 10), width=30, show="*")
        self.pw_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # API 키
        tk.Label(login_frame, text="Gemini API 키:", 
                font=('맑은 고딕', 10), bg='white').grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.api_entry = tk.Entry(login_frame, font=('맑은 고딕', 10), width=30)
        self.api_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # SEO 키워드 프레임
        seo_frame = tk.LabelFrame(self.root, 
                                 text="SEO 키워드 작성",
                                 font=('맑은 고딕', 12, 'bold'),
                                 bg='white')
        seo_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(seo_frame, text="키워드 (쉼표로 구분):", 
                font=('맑은 고딕', 10), bg='white').pack(anchor='w', padx=10, pady=5)
        
        self.keywords_entry = tk.Text(seo_frame, height=2, font=('맑은 고딕', 10))
        self.keywords_entry.pack(fill='x', padx=10, pady=5)
        self.keywords_entry.insert('1.0', "코딩교육, 프로그래밍, 아이코딩")
        
        # 버튼 프레임
        btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        btn_frame.pack(fill='x', padx=20, pady=20)
        
        # 패키지 설치 버튼
        install_btn = tk.Button(btn_frame, 
                               text="📦 필수 패키지 설치",
                               font=('맑은 고딕', 10, 'bold'),
                               bg='#FF9800',
                               fg='white',
                               command=self.install_packages)
        install_btn.pack(side='left', padx=(0, 10))
        
        # 전체 프로그램 실행 버튼
        run_btn = tk.Button(btn_frame, 
                           text="🚀 전체 프로그램 실행",
                           font=('맑은 고딕', 10, 'bold'),
                           bg='#4CAF50',
                           fg='white',
                           command=self.run_full_program)
        run_btn.pack(side='left')
        
        # 로그 영역
        log_frame = tk.LabelFrame(self.root, 
                                 text="실행 로그",
                                 font=('맑은 고딕', 12, 'bold'))
        log_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, 
                                                 font=('Consolas', 9),
                                                 bg='#2d3748',
                                                 fg='#e2e8f0')
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 상태바
        self.status_var = tk.StringVar(value="준비됨")
        status_bar = tk.Label(self.root, 
                             textvariable=self.status_var,
                             bg='#343a40',
                             fg='white',
                             font=('맑은 고딕', 9))
        status_bar.pack(fill='x', side='bottom')
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert('end', f"[{timestamp}] {message}\n")
        self.log_text.see('end')
        self.root.update()
    
    def update_status(self, status):
        self.status_var.set(status)
        self.root.update()
    
    def install_packages(self):
        def install_thread():
            try:
                self.update_status("패키지 설치 중...")
                self.log("필수 패키지 설치를 시작합니다...")
                
                packages = [
                    'selenium',
                    'webdriver-manager', 
                    'google-generativeai',
                    'openpyxl',
                    'pyperclip'
                ]
                
                for package in packages:
                    self.log(f"설치 중: {package}")
                    result = subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                                          capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        self.log(f"✅ {package} 설치 완료")
                    else:
                        self.log(f"❌ {package} 설치 실패: {result.stderr}")
                
                self.log("패키지 설치가 완료되었습니다!")
                messagebox.showinfo("완료", "필수 패키지 설치가 완료되었습니다!")
                
            except Exception as e:
                self.log(f"패키지 설치 중 오류: {str(e)}")
                messagebox.showerror("오류", f"패키지 설치 중 오류가 발생했습니다: {str(e)}")
            finally:
                self.update_status("준비됨")
        
        threading.Thread(target=install_thread, daemon=True).start()
    
    def run_full_program(self):
        try:
            # 설정값 검증
            naver_id = self.id_entry.get().strip()
            naver_pw = self.pw_entry.get().strip()
            api_key = self.api_entry.get().strip()
            keywords = self.keywords_entry.get('1.0', 'end').strip()
            
            if not all([naver_id, naver_pw, api_key, keywords]):
                messagebox.showerror("오류", "모든 필드를 입력해주세요.")
                return
            
            self.log("전체 프로그램을 실행합니다...")
            
            # 전체 프로그램 파일이 있는지 확인
            full_program = "gui_블로그자동작성기.py"
            if os.path.exists(full_program):
                self.log("전체 프로그램을 실행합니다...")
                
                # 환경변수로 설정값 전달
                env = os.environ.copy()
                env['NAVER_ID'] = naver_id
                env['NAVER_PW'] = naver_pw
                env['GEMINI_API'] = api_key
                env['KEYWORDS'] = keywords
                
                subprocess.Popen([sys.executable, full_program], env=env)
                self.log("전체 프로그램이 실행되었습니다!")
                
            else:
                self.log("전체 프로그램 파일을 찾을 수 없습니다.")
                messagebox.showwarning("경고", f"{full_program} 파일을 찾을 수 없습니다.")
                
        except Exception as e:
            self.log(f"프로그램 실행 중 오류: {str(e)}")
            messagebox.showerror("오류", f"프로그램 실행 중 오류가 발생했습니다: {str(e)}")
    
    def run(self):
        # 시작 메시지
        self.log("네이버 블로그 자동 작성기에 오신 것을 환영합니다!")
        self.log("1. 먼저 '필수 패키지 설치' 버튼을 클릭하세요.")
        self.log("2. 로그인 정보와 API 키, 키워드를 입력하세요.")
        self.log("3. '전체 프로그램 실행' 버튼을 클릭하세요.")
        
        self.root.mainloop()


if __name__ == "__main__":
    app = MinimalBlogWriter()
    app.run()