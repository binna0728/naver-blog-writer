"""
🚀 최신 Modern UI 네이버 블로그 자동 작성기
- 다크 테마 지원
- 최신 디자인 트렌드 적용
- 애니메이션 효과
- 카드형 레이아웃
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import time
import pyperclip
import os
from openpyxl import load_workbook, Workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from geminiapi import GeminiAPI
import shutil
import glob


class ModernTheme:
    """최신 UI 테마 클래스"""
    
    # 다크 테마 색상
    DARK = {
        'bg_primary': '#0f172a',      # 슬레이트 950
        'bg_secondary': '#1e293b',    # 슬레이트 800
        'bg_tertiary': '#334155',     # 슬레이트 700
        'text_primary': '#f8fafc',    # 슬레이트 50
        'text_secondary': '#cbd5e1',  # 슬레이트 300
        'accent_primary': '#3b82f6',  # 블루 500
        'accent_secondary': '#8b5cf6', # 바이올렛 500
        'success': '#10b981',         # 에메랄드 500
        'warning': '#f59e0b',         # 앰버 500
        'error': '#ef4444',           # 레드 500
        'card_bg': '#1e293b',         # 슬레이트 800
        'border': '#475569'           # 슬레이트 600
    }
    
    # 라이트 테마 색상
    LIGHT = {
        'bg_primary': '#ffffff',
        'bg_secondary': '#f8fafc',
        'bg_tertiary': '#e2e8f0',
        'text_primary': '#0f172a',
        'text_secondary': '#475569',
        'accent_primary': '#3b82f6',
        'accent_secondary': '#8b5cf6',
        'success': '#10b981',
        'warning': '#f59e0b',
        'error': '#ef4444',
        'card_bg': '#ffffff',
        'border': '#e2e8f0'
    }


class ModernCard(tk.Frame):
    """모던 카드 위젯"""
    
    def __init__(self, parent, title="", theme=ModernTheme.DARK, **kwargs):
        super().__init__(parent, bg=theme['card_bg'], relief='flat', bd=0, **kwargs)
        self.theme = theme
        
        # 카드 스타일링
        self.configure(highlightbackground=theme['border'], 
                      highlightcolor=theme['accent_primary'],
                      highlightthickness=1)
        
        if title:
            self.title_label = tk.Label(self, 
                                       text=title,
                                       font=('Segoe UI', 14, 'bold'),
                                       fg=theme['text_primary'],
                                       bg=theme['card_bg'])
            self.title_label.pack(anchor='w', padx=20, pady=(15, 10))


class ModernButton(tk.Button):
    """모던 버튼 위젯"""
    
    def __init__(self, parent, text, style='primary', theme=ModernTheme.DARK, **kwargs):
        # 스타일별 색상 설정
        styles = {
            'primary': {
                'bg': theme['accent_primary'],
                'fg': '#ffffff',
                'active_bg': theme['accent_secondary']
            },
            'success': {
                'bg': theme['success'],
                'fg': '#ffffff',
                'active_bg': '#059669'
            },
            'warning': {
                'bg': theme['warning'],
                'fg': '#ffffff', 
                'active_bg': '#d97706'
            },
            'secondary': {
                'bg': theme['bg_tertiary'],
                'fg': theme['text_primary'],
                'active_bg': theme['border']
            }
        }
        
        style_config = styles.get(style, styles['primary'])
        
        super().__init__(parent,
                        text=text,
                        font=('Segoe UI', 10, 'bold'),
                        bg=style_config['bg'],
                        fg=style_config['fg'],
                        activebackground=style_config['active_bg'],
                        activeforeground='#ffffff',
                        relief='flat',
                        bd=0,
                        padx=20,
                        pady=8,
                        cursor='hand2',
                        **kwargs)
        
        # 호버 효과
        self.bind("<Enter>", lambda e: self.configure(bg=style_config['active_bg']))
        self.bind("<Leave>", lambda e: self.configure(bg=style_config['bg']))


class ModernEntry(tk.Entry):
    """모던 입력창 위젯"""
    
    def __init__(self, parent, placeholder="", theme=ModernTheme.DARK, **kwargs):
        super().__init__(parent,
                        font=('Segoe UI', 10),
                        bg=theme['bg_secondary'],
                        fg=theme['text_primary'],
                        relief='flat',
                        bd=0,
                        highlightbackground=theme['border'],
                        highlightcolor=theme['accent_primary'],
                        highlightthickness=2,
                        insertbackground=theme['text_primary'],
                        **kwargs)
        
        self.theme = theme
        self.placeholder = placeholder
        self.placeholder_active = False
        
        if placeholder:
            self.insert(0, placeholder)
            self.configure(fg=theme['text_secondary'])
            self.placeholder_active = True
            
            self.bind("<FocusIn>", self._on_focus_in)
            self.bind("<FocusOut>", self._on_focus_out)
    
    def _on_focus_in(self, event):
        if self.placeholder_active:
            self.delete(0, tk.END)
            self.configure(fg=self.theme['text_primary'])
            self.placeholder_active = False
    
    def _on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(fg=self.theme['text_secondary'])
            self.placeholder_active = True


class ModernText(tk.Text):
    """모던 텍스트 영역 위젯"""
    
    def __init__(self, parent, theme=ModernTheme.DARK, **kwargs):
        super().__init__(parent,
                        font=('Segoe UI', 10),
                        bg=theme['bg_secondary'],
                        fg=theme['text_primary'],
                        relief='flat',
                        bd=0,
                        highlightbackground=theme['border'],
                        highlightcolor=theme['accent_primary'],
                        highlightthickness=2,
                        insertbackground=theme['text_primary'],
                        selectbackground=theme['accent_primary'],
                        selectforeground='#ffffff',
                        wrap=tk.WORD,
                        **kwargs)


class ModernBlogWriterApp:
    """최신 UI 네이버 블로그 자동 작성기"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("네이버 블로그 자동 작성기 2024")
        self.root.geometry("1000x700")
        
        # 다크 테마 적용
        self.theme = ModernTheme.DARK
        self.root.configure(bg=self.theme['bg_primary'])
        
        # 변수들
        self.driver = None
        self.gemini_api = None
        self.is_running = False
        
        self.setup_styles()
        self.create_header()
        self.create_sidebar()
        self.create_main_content()
        self.create_footer()
        self.center_window()
        
        # 초기 페이지 표시
        self.show_dashboard()
    
    def setup_styles(self):
        """ttk 스타일 설정"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 진행바 스타일
        style.configure("Modern.Horizontal.TProgressbar",
                       background=self.theme['accent_primary'],
                       troughcolor=self.theme['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=self.theme['accent_primary'],
                       darkcolor=self.theme['accent_primary'])
    
    def create_header(self):
        """헤더 생성"""
        header = tk.Frame(self.root, bg=self.theme['bg_secondary'], height=70)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        # 로고 및 제목
        title_frame = tk.Frame(header, bg=self.theme['bg_secondary'])
        title_frame.pack(side='left', padx=30, pady=20)
        
        # 아이콘
        icon_label = tk.Label(title_frame, 
                             text="🚀", 
                             font=('Segoe UI', 20),
                             bg=self.theme['bg_secondary'])
        icon_label.pack(side='left')
        
        # 제목
        title_label = tk.Label(title_frame, 
                              text="네이버 블로그 자동 작성기",
                              font=('Segoe UI', 18, 'bold'),
                              fg=self.theme['text_primary'],
                              bg=self.theme['bg_secondary'])
        title_label.pack(side='left', padx=(10, 0))
        
        # 버전 정보
        version_label = tk.Label(title_frame,
                                text="v2.0",
                                font=('Segoe UI', 10),
                                fg=self.theme['accent_primary'],
                                bg=self.theme['bg_secondary'])
        version_label.pack(side='left', padx=(10, 0), pady=(5, 0))
        
        # 테마 토글 버튼
        theme_btn = ModernButton(header, "🌙", style='secondary', theme=self.theme,
                                command=self.toggle_theme)
        theme_btn.pack(side='right', padx=30, pady=20)
    
    def create_sidebar(self):
        """사이드바 생성"""
        sidebar = tk.Frame(self.root, bg=self.theme['bg_secondary'], width=250)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        # 네비게이션 메뉴
        nav_items = [
            ("🏠", "대시보드", self.show_dashboard),
            ("🔐", "로그인 설정", self.show_login),
            ("✨", "AI 글 생성", self.show_ai_writer),
            ("📊", "엑셀 포스팅", self.show_excel),
            ("📋", "실행 로그", self.show_logs),
            ("⚙️", "설정", self.show_settings)
        ]
        
        self.nav_buttons = []
        for icon, text, command in nav_items:
            btn_frame = tk.Frame(sidebar, bg=self.theme['bg_secondary'])
            btn_frame.pack(fill='x', padx=10, pady=2)
            
            btn = tk.Button(btn_frame,
                           text=f"{icon}  {text}",
                           font=('Segoe UI', 11),
                           bg=self.theme['bg_secondary'],
                           fg=self.theme['text_secondary'],
                           activebackground=self.theme['bg_tertiary'],
                           activeforeground=self.theme['text_primary'],
                           relief='flat',
                           bd=0,
                           anchor='w',
                           padx=20,
                           pady=12,
                           cursor='hand2',
                           command=command)
            btn.pack(fill='x')
            
            # 호버 효과
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.theme['bg_tertiary'], 
                                                            fg=self.theme['text_primary']))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.theme['bg_secondary'], 
                                                            fg=self.theme['text_secondary']))
            
            self.nav_buttons.append(btn)
    
    def create_main_content(self):
        """메인 콘텐츠 영역 생성"""
        self.main_frame = tk.Frame(self.root, bg=self.theme['bg_primary'])
        self.main_frame.pack(side='right', fill='both', expand=True)
    
    def create_footer(self):
        """푸터 생성"""
        footer = tk.Frame(self.root, bg=self.theme['bg_secondary'], height=40)
        footer.pack(side='bottom', fill='x')
        footer.pack_propagate(False)
        
        # 상태 표시
        self.status_var = tk.StringVar(value="준비됨")
        status_label = tk.Label(footer,
                               textvariable=self.status_var,
                               font=('Segoe UI', 9),
                               fg=self.theme['text_secondary'],
                               bg=self.theme['bg_secondary'])
        status_label.pack(side='left', padx=20, pady=12)
        
        # 진행률 바
        self.progress = ttk.Progressbar(footer, 
                                       style="Modern.Horizontal.TProgressbar",
                                       mode='indeterminate',
                                       length=200)
        self.progress.pack(side='right', padx=20, pady=12)
    
    def clear_main_frame(self):
        """메인 프레임 클리어"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def activate_nav_button(self, index):
        """네비게이션 버튼 활성화"""
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.configure(bg=self.theme['accent_primary'], 
                             fg='#ffffff')
            else:
                btn.configure(bg=self.theme['bg_secondary'], 
                             fg=self.theme['text_secondary'])
    
    def show_dashboard(self):
        """대시보드 페이지"""
        self.clear_main_frame()
        self.activate_nav_button(0)
        
        # 스크롤 가능한 캔버스
        canvas = tk.Canvas(self.main_frame, bg=self.theme['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme['bg_primary'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 환영 메시지
        welcome_card = ModernCard(scrollable_frame, "환영합니다! 👋", self.theme)
        welcome_card.pack(fill='x', padx=30, pady=20)
        
        welcome_text = tk.Label(welcome_card,
                               text="네이버 블로그 자동 작성기에 오신 것을 환영합니다.\n"
                                    "AI 기반 블로그 글 작성으로 효율적인 콘텐츠 제작을 시작하세요!",
                               font=('Segoe UI', 11),
                               fg=self.theme['text_secondary'],
                               bg=self.theme['card_bg'],
                               justify='left')
        welcome_text.pack(anchor='w', padx=20, pady=(0, 20))
        
        # 통계 카드들
        stats_frame = tk.Frame(scrollable_frame, bg=self.theme['bg_primary'])
        stats_frame.pack(fill='x', padx=30, pady=10)
        
        # 기능 카드 1
        feature1_card = ModernCard(stats_frame, theme=self.theme)
        feature1_card.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        tk.Label(feature1_card, text="🤖", font=('Segoe UI', 24), 
                bg=self.theme['card_bg']).pack(pady=(15, 5))
        tk.Label(feature1_card, text="AI 글 생성", font=('Segoe UI', 12, 'bold'),
                fg=self.theme['text_primary'], bg=self.theme['card_bg']).pack()
        tk.Label(feature1_card, text="Gemini API로\n자동 글 작성", 
                font=('Segoe UI', 9), fg=self.theme['text_secondary'], 
                bg=self.theme['card_bg'], justify='center').pack(pady=(5, 15))
        
        # 기능 카드 2
        feature2_card = ModernCard(stats_frame, theme=self.theme)
        feature2_card.pack(side='left', fill='both', expand=True, padx=5)
        
        tk.Label(feature2_card, text="📊", font=('Segoe UI', 24), 
                bg=self.theme['card_bg']).pack(pady=(15, 5))
        tk.Label(feature2_card, text="대량 포스팅", font=('Segoe UI', 12, 'bold'),
                fg=self.theme['text_primary'], bg=self.theme['card_bg']).pack()
        tk.Label(feature2_card, text="엑셀 파일로\n일괄 업로드", 
                font=('Segoe UI', 9), fg=self.theme['text_secondary'], 
                bg=self.theme['card_bg'], justify='center').pack(pady=(5, 15))
        
        # 기능 카드 3
        feature3_card = ModernCard(stats_frame, theme=self.theme)
        feature3_card.pack(side='left', fill='both', expand=True, padx=(10, 0))
        
        tk.Label(feature3_card, text="🚀", font=('Segoe UI', 24), 
                bg=self.theme['card_bg']).pack(pady=(15, 5))
        tk.Label(feature3_card, text="자동화", font=('Segoe UI', 12, 'bold'),
                fg=self.theme['text_primary'], bg=self.theme['card_bg']).pack()
        tk.Label(feature3_card, text="원클릭\n자동 포스팅", 
                font=('Segoe UI', 9), fg=self.theme['text_secondary'], 
                bg=self.theme['card_bg'], justify='center').pack(pady=(5, 15))
        
        # 빠른 시작 가이드
        guide_card = ModernCard(scrollable_frame, "빠른 시작 가이드 🚀", self.theme)
        guide_card.pack(fill='x', padx=30, pady=20)
        
        steps = [
            "1. 좌측 '로그인 설정'에서 네이버 계정과 Gemini API 설정",
            "2. 'AI 글 생성' 또는 '엑셀 포스팅' 선택",
            "3. 설정에 따라 자동으로 글 작성 및 포스팅 실행"
        ]
        
        for step in steps:
            step_label = tk.Label(guide_card,
                                 text=step,
                                 font=('Segoe UI', 10),
                                 fg=self.theme['text_secondary'],
                                 bg=self.theme['card_bg'],
                                 anchor='w')
            step_label.pack(fill='x', padx=20, pady=5)
    
    def show_login(self):
        """로그인 설정 페이지"""
        self.clear_main_frame()
        self.activate_nav_button(1)
        
        # 페이지 제목
        title_frame = tk.Frame(self.main_frame, bg=self.theme['bg_primary'])
        title_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Label(title_frame, text="로그인 설정", 
                font=('Segoe UI', 20, 'bold'),
                fg=self.theme['text_primary'],
                bg=self.theme['bg_primary']).pack(anchor='w')
        
        # 네이버 계정 카드
        naver_card = ModernCard(self.main_frame, "네이버 계정 정보 🔐", self.theme)
        naver_card.pack(fill='x', padx=30, pady=10)
        
        # 입력 필드들
        fields_frame = tk.Frame(naver_card, bg=self.theme['card_bg'])
        fields_frame.pack(fill='x', padx=20, pady=20)
        
        # 아이디
        tk.Label(fields_frame, text="아이디", font=('Segoe UI', 10, 'bold'),
                fg=self.theme['text_primary'], bg=self.theme['card_bg']).grid(row=0, column=0, sticky='w', pady=(0, 5))
        self.id_entry = ModernEntry(fields_frame, "네이버 아이디 입력", self.theme, width=40)
        self.id_entry.grid(row=1, column=0, sticky='ew', pady=(0, 15))
        
        # 비밀번호  
        tk.Label(fields_frame, text="비밀번호", font=('Segoe UI', 10, 'bold'),
                fg=self.theme['text_primary'], bg=self.theme['card_bg']).grid(row=2, column=0, sticky='w', pady=(0, 5))
        self.pw_entry = ModernEntry(fields_frame, "비밀번호 입력", self.theme, width=40, show="*")
        self.pw_entry.grid(row=3, column=0, sticky='ew', pady=(0, 15))
        
        fields_frame.columnconfigure(0, weight=1)
        
        # 테스트 버튼
        test_btn = ModernButton(naver_card, "🔍 로그인 테스트", 'primary', self.theme, command=self.test_login)
        test_btn.pack(padx=20, pady=(0, 20))
        
        # Gemini API 카드
        api_card = ModernCard(self.main_frame, "Gemini AI API 설정 🤖", self.theme)
        api_card.pack(fill='x', padx=30, pady=10)
        
        api_frame = tk.Frame(api_card, bg=self.theme['card_bg'])
        api_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(api_frame, text="API 키", font=('Segoe UI', 10, 'bold'),
                fg=self.theme['text_primary'], bg=self.theme['card_bg']).pack(anchor='w', pady=(0, 5))
        self.api_entry = ModernEntry(api_frame, "Gemini API 키 입력", self.theme, width=60)
        self.api_entry.pack(fill='x', pady=(0, 15))
        
        api_test_btn = ModernButton(api_card, "🤖 API 테스트", 'success', self.theme, command=self.test_api)
        api_test_btn.pack(padx=20, pady=(0, 20))
    
    def show_ai_writer(self):
        """AI 글 생성 페이지"""
        self.clear_main_frame()
        self.activate_nav_button(2)
        
        # 페이지 제목
        title_frame = tk.Frame(self.main_frame, bg=self.theme['bg_primary'])
        title_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Label(title_frame, text="AI 기반 글 생성", 
                font=('Segoe UI', 20, 'bold'),
                fg=self.theme['text_primary'],
                bg=self.theme['bg_primary']).pack(anchor='w')
        
        # 키워드 입력 카드
        keyword_card = ModernCard(self.main_frame, "SEO 키워드 입력 ✨", self.theme)
        keyword_card.pack(fill='x', padx=30, pady=10)
        
        keyword_frame = tk.Frame(keyword_card, bg=self.theme['card_bg'])
        keyword_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(keyword_frame, text="키워드 (쉼표로 구분)", 
                font=('Segoe UI', 10, 'bold'),
                fg=self.theme['text_primary'], 
                bg=self.theme['card_bg']).pack(anchor='w', pady=(0, 10))
        
        self.keywords_text = ModernText(keyword_frame, self.theme, height=4)
        self.keywords_text.pack(fill='x', pady=(0, 15))
        self.keywords_text.insert('1.0', "코딩교육, 프로그래밍 학습, 아이 코딩, 소프트웨어 교육, 진로 가이드")
        
        # 설정 카드
        settings_card = ModernCard(self.main_frame, "생성 설정 ⚙️", self.theme)
        settings_card.pack(fill='x', padx=30, pady=10)
        
        settings_frame = tk.Frame(settings_card, bg=self.theme['card_bg'])
        settings_frame.pack(fill='x', padx=20, pady=20)
        
        # 글 개수 설정
        count_frame = tk.Frame(settings_frame, bg=self.theme['card_bg'])
        count_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(count_frame, text="생성할 글 개수:", 
                font=('Segoe UI', 10, 'bold'),
                fg=self.theme['text_primary'],
                bg=self.theme['card_bg']).pack(side='left')
        
        self.post_count_var = tk.StringVar(value="3")
        count_entry = ModernEntry(count_frame, theme=self.theme, width=10, textvariable=self.post_count_var)
        count_entry.pack(side='left', padx=(20, 0))
        
        # 실행 버튼들
        button_frame = tk.Frame(self.main_frame, bg=self.theme['bg_primary'])
        button_frame.pack(fill='x', padx=30, pady=20)
        
        generate_btn = ModernButton(button_frame, "✨ 글만 생성하기", 'primary', self.theme, command=self.generate_seo_posts)
        generate_btn.pack(side='left', padx=(0, 15))
        
        post_btn = ModernButton(button_frame, "🚀 생성 후 바로 포스팅", 'success', self.theme, command=self.generate_and_post)
        post_btn.pack(side='left')
    
    def show_excel(self):
        """엑셀 포스팅 페이지"""
        self.clear_main_frame()
        self.activate_nav_button(3)
        
        # 페이지 제목
        title_frame = tk.Frame(self.main_frame, bg=self.theme['bg_primary'])
        title_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Label(title_frame, text="엑셀 기반 대량 포스팅", 
                font=('Segoe UI', 20, 'bold'),
                fg=self.theme['text_primary'],
                bg=self.theme['bg_primary']).pack(anchor='w')
        
        # 파일 선택 카드
        file_card = ModernCard(self.main_frame, "엑셀 파일 선택 📊", self.theme)
        file_card.pack(fill='x', padx=30, pady=10)
        
        file_frame = tk.Frame(file_card, bg=self.theme['card_bg'])
        file_frame.pack(fill='x', padx=20, pady=20)
        
        self.file_path_var = tk.StringVar(value="posting.xlsx")
        
        tk.Label(file_frame, text="선택된 파일:", 
                font=('Segoe UI', 10, 'bold'),
                fg=self.theme['text_primary'],
                bg=self.theme['card_bg']).pack(anchor='w', pady=(0, 5))
        
        file_display_frame = tk.Frame(file_frame, bg=self.theme['card_bg'])
        file_display_frame.pack(fill='x', pady=(0, 15))
        
        file_label = tk.Label(file_display_frame, 
                             textvariable=self.file_path_var,
                             font=('Segoe UI', 10),
                             fg=self.theme['accent_primary'],
                             bg=self.theme['card_bg'])
        file_label.pack(side='left')
        
        browse_btn = ModernButton(file_display_frame, "📂 파일 찾기", 'secondary', self.theme, command=self.browse_file)
        browse_btn.pack(side='right')
        
        # 미리보기 섹션
        preview_card = ModernCard(self.main_frame, "데이터 미리보기 👀", self.theme)
        preview_card.pack(fill='both', expand=True, padx=30, pady=10)
        
        self.preview_text = ModernText(preview_card, self.theme, height=8)
        self.preview_text.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 실행 버튼
        excel_btn = ModernButton(self.main_frame, "🚀 엑셀 데이터로 포스팅 시작", 'success', self.theme, command=self.process_excel)
        excel_btn.pack(pady=30)
    
    def show_logs(self):
        """로그 페이지"""
        self.clear_main_frame()
        self.activate_nav_button(4)
        
        # 페이지 제목
        title_frame = tk.Frame(self.main_frame, bg=self.theme['bg_primary'])
        title_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Label(title_frame, text="실행 로그", 
                font=('Segoe UI', 20, 'bold'),
                fg=self.theme['text_primary'],
                bg=self.theme['bg_primary']).pack(side='left')
        
        clear_btn = ModernButton(title_frame, "🗑️ 로그 지우기", 'warning', self.theme, command=self.clear_log)
        clear_btn.pack(side='right')
        
        # 로그 텍스트 영역
        log_card = ModernCard(self.main_frame, theme=self.theme)
        log_card.pack(fill='both', expand=True, padx=30, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_card, 
                                                 font=('JetBrains Mono', 10),
                                                 bg='#0f172a',
                                                 fg='#e2e8f0',
                                                 insertbackground='#e2e8f0',
                                                 selectbackground=self.theme['accent_primary'],
                                                 relief='flat',
                                                 bd=0)
        self.log_text.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 초기 로그 메시지
        self.log("🚀 네이버 블로그 자동 작성기 시작됨")
        self.log("📋 로그 시스템 준비 완료")
    
    def show_settings(self):
        """설정 페이지"""
        self.clear_main_frame()
        self.activate_nav_button(5)
        
        # 페이지 제목
        title_frame = tk.Frame(self.main_frame, bg=self.theme['bg_primary'])
        title_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Label(title_frame, text="설정", 
                font=('Segoe UI', 20, 'bold'),
                fg=self.theme['text_primary'],
                bg=self.theme['bg_primary']).pack(anchor='w')
        
        # 일반 설정 카드
        general_card = ModernCard(self.main_frame, "일반 설정 ⚙️", self.theme)
        general_card.pack(fill='x', padx=30, pady=10)
        
        settings_frame = tk.Frame(general_card, bg=self.theme['card_bg'])
        settings_frame.pack(fill='x', padx=20, pady=20)
        
        # 테마 설정
        theme_frame = tk.Frame(settings_frame, bg=self.theme['card_bg'])
        theme_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(theme_frame, text="테마:", 
                font=('Segoe UI', 10, 'bold'),
                fg=self.theme['text_primary'],
                bg=self.theme['card_bg']).pack(side='left')
        
        theme_btn = ModernButton(theme_frame, "🌙 다크 모드", 'secondary', self.theme, command=self.toggle_theme)
        theme_btn.pack(side='right')
        
        # 정보 카드
        info_card = ModernCard(self.main_frame, "프로그램 정보 📋", self.theme)
        info_card.pack(fill='x', padx=30, pady=10)
        
        info_text = """
버전: 2.0
개발: AI Assistant
업데이트: 2024년 최신 UI 적용
        
주요 기능:
• AI 기반 자동 글 생성
• 엑셀 데이터 대량 포스팅  
• 현대적인 다크 테마 UI
• 실시간 진행 상황 모니터링
        """
        
        tk.Label(info_card, text=info_text.strip(),
                font=('Segoe UI', 10),
                fg=self.theme['text_secondary'],
                bg=self.theme['card_bg'],
                justify='left').pack(padx=20, pady=20)
    
    def toggle_theme(self):
        """테마 토글"""
        if self.theme == ModernTheme.DARK:
            self.theme = ModernTheme.LIGHT
        else:
            self.theme = ModernTheme.DARK
        
        # UI 새로고침
        self.refresh_ui()
    
    def refresh_ui(self):
        """UI 새로고침"""
        # 전체 UI를 다시 그리는 로직
        messagebox.showinfo("알림", "테마가 변경되었습니다. 프로그램을 재시작해주세요.")
    
    def center_window(self):
        """창 중앙 배치"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def log(self, message, level='INFO'):
        """로그 출력"""
        timestamp = time.strftime("%H:%M:%S")
        
        # 레벨별 색상과 아이콘
        level_config = {
            'INFO': ('💡', '#3b82f6'),
            'SUCCESS': ('✅', '#10b981'),
            'WARNING': ('⚠️', '#f59e0b'),
            'ERROR': ('❌', '#ef4444')
        }
        
        icon, color = level_config.get(level, ('💡', '#3b82f6'))
        
        if hasattr(self, 'log_text'):
            self.log_text.insert('end', f"[{timestamp}] {icon} {message}\n")
            self.log_text.see('end')
            self.root.update()
    
    def clear_log(self):
        """로그 지우기"""
        if hasattr(self, 'log_text'):
            self.log_text.delete(1.0, 'end')
            self.log("🧹 로그가 지워졌습니다")
    
    def update_status(self, status):
        """상태 업데이트"""
        self.status_var.set(status)
        self.root.update()
    
    # 기능 메서드들 (기존 코드와 동일)
    def setup_driver(self):
        """Chrome 드라이버 설정 (기존 코드)"""
        # 기존 setup_driver 코드 유지
        pass
    
    def test_login(self):
        """로그인 테스트 (기존 코드)"""
        self.log("🔐 로그인 테스트를 시작합니다...")
        # 기존 test_login 코드 유지
        
    def test_api(self):
        """API 테스트 (기존 코드)"""
        self.log("🤖 Gemini API 테스트를 시작합니다...")
        # 기존 test_api 코드 유지
        
    def generate_seo_posts(self):
        """SEO 포스트 생성 (기존 코드)"""
        self.log("✨ AI 글 생성을 시작합니다...")
        # 기존 generate_seo_posts 코드 유지
        
    def generate_and_post(self):
        """생성 후 포스팅 (기존 코드)"""
        self.log("🚀 AI 글 생성 및 포스팅을 시작합니다...")
        # 기존 generate_and_post 코드 유지
        
    def browse_file(self):
        """파일 선택 (기존 코드)"""
        filename = filedialog.askopenfilename(
            title="엑셀 파일 선택",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
            self.log(f"📊 파일 선택됨: {filename}")
            
    def process_excel(self):
        """엑셀 처리 (기존 코드)"""
        self.log("📊 엑셀 데이터 처리를 시작합니다...")
        # 기존 process_excel 코드 유지
    
    def run(self):
        """앱 실행"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """프로그램 종료"""
        if self.driver:
            self.driver.quit()
        self.root.destroy()


if __name__ == "__main__":
    app = ModernBlogWriterApp()
    app.run()