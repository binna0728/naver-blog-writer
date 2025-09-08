import time
import pyperclip
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import threading

class NaverBlogWriter:
    def __init__(self):
        self.naver_id = "cocodinglab"
        self.naver_password = "zhzheld201*"
        self.driver = None
        self.keep_running = True
        self.setup_driver()
    
    def setup_driver(self):
        """Chrome 드라이버 설정"""
        try:
            print("Chrome 드라이버 설정 중...")
            
            current_dir = os.getcwd()
            possible_drivers = [
                os.path.join(current_dir, "chromedriver.exe"),
                os.path.join(current_dir, "driver", "chromedriver.exe"),
                "chromedriver.exe",
            ]
            
            driver_path = None
            for path in possible_drivers:
                if os.path.exists(path):
                    driver_path = path
                    print(f"드라이버 발견: {driver_path}")
                    break
            
            if not driver_path:
                print("Chrome 드라이버를 찾을 수 없습니다!")
                raise Exception("Chrome 드라이버를 찾을 수 없습니다.")
            
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36")
            
            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # WebDriver 속성 숨기기
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("Chrome 드라이버 설정 완료!")
            
        except Exception as e:
            print(f"드라이버 설정 중 오류: {e}")
            raise
    
    def login_to_naver(self):
        """네이버 로그인"""
        try:
            print("네이버 로그인 페이지로 이동 중...")
            self.driver.get("https://nid.naver.com/nidlogin.login")
            time.sleep(3)
            
            print("아이디 입력 중...")
            id_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "id"))
            )
            
            pyperclip.copy(self.naver_id)
            id_input.click()
            time.sleep(0.5)
            id_input.clear()
            time.sleep(0.3)
            
            actions = ActionChains(self.driver)
            actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            time.sleep(1)
            
            print(f"아이디 입력 완료: {self.naver_id}")
            
            print("비밀번호 입력 중...")
            pw_input = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "pw"))
            )
            
            pyperclip.copy(self.naver_password)
            pw_input.click()
            time.sleep(0.5)
            pw_input.clear()
            time.sleep(0.3)
            actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            time.sleep(1)
            
            print("비밀번호 입력 완료")
            
            print("로그인 버튼 클릭 중...")
            login_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "log.login"))
            )
            login_btn.click()
            
            print("로그인 처리 중...")
            time.sleep(2)
            time.sleep(3)
            
            current_url = self.driver.current_url
            print(f"현재 URL: {current_url}")
            
            if ("naver.com" in current_url and "login" not in current_url) or "mail.naver.com" in current_url:
                print("로그인 성공!")
                return True
            elif "captcha" in current_url.lower() or "turing" in current_url.lower():
                print("캡차 인증이 필요합니다.")
                return True
            else:
                print("로그인 실패 또는 추가 인증 필요")
                return False
                
        except Exception as e:
            print(f"로그인 중 오류 발생: {str(e)}")
            return False
    
    def go_to_blog_write(self):
        """블로그 글쓰기 페이지로 이동"""
        try:
            print("블로그 글쓰기 페이지로 이동 중...")
            self.driver.get("https://blog.naver.com/GoBlogWrite.naver")
            time.sleep(3)
            print("블로그 글쓰기 페이지 도착!")
            return True
            
        except Exception as e:
            print(f"블로그 글쓰기 페이지 이동 중 오류: {str(e)}")
            return False
    
    def write_test_post(self):
        """테스트 포스트 작성"""
        try:
            print("자동 글 작성을 시작합니다...")
            
            # #mainFrame 셀렉터로 iframe 진입
            print("메인 프레임으로 전환 중...")
            main_frame = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#mainFrame"))
            )
            self.driver.switch_to.frame(main_frame)
            time.sleep(2)
            
            # se-popup-button-cancel 셀렉터가 존재하면 클릭
            try:
                cancel_btn = self.driver.find_element(By.CSS_SELECTOR, ".se-popup-button-cancel")
                if cancel_btn.is_displayed():
                    cancel_btn.click()
                    print("팝업 취소 버튼 클릭됨")
                    time.sleep(1)
            except:
                print("팝업 취소 버튼 없음 - 넘어감")
            
            # se-help-panel-close-button 셀렉터가 존재하면 클릭
            try:
                help_close_btn = self.driver.find_element(By.CSS_SELECTOR, ".se-help-panel-close-button")
                if help_close_btn.is_displayed():
                    help_close_btn.click()
                    print("도움말 패널 닫기 버튼 클릭됨")
                    time.sleep(1)
            except:
                print("도움말 패널 닫기 버튼 없음 - 넘어감")
            
            # se-section-documentTitle 셀렉터를 클릭 후 "제목 테스트" 입력
            print("제목 입력 중...")
            title_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".se-section-documentTitle"))
            )
            title_element.click()
            time.sleep(1)
            
            # 클립보드 사용해서 제목 입력
            pyperclip.copy("제목 테스트")
            actions = ActionChains(self.driver)
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            time.sleep(0.3)
            actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            time.sleep(1)
            print("제목 입력 완료: '제목 테스트'")
            
            # se-section-text 셀렉터를 클릭한 후 내용 5줄 입력
            print("본문 내용 입력 중...")
            text_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".se-section-text"))
            )
            text_element.click()
            time.sleep(1)
            
            # 5줄의 내용 작성
            content_lines = []
            for i in range(1, 6):
                content_lines.append(f"{i}. 안녕하세요 내용을 입력하고 있습니다.")
            
            content = "\n".join(content_lines)
            pyperclip.copy(content)
            
            actions = ActionChains(self.driver)
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            time.sleep(0.3)
            actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            time.sleep(2)
            print("본문 내용 5줄 입력 완료")
            
            # save_btn_bzc58 셀렉터를 클릭
            print("저장 버튼 클릭 중...")
            save_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#save_btn_bzc58"))
            )
            save_btn.click()
            time.sleep(3)
            print("저장 버튼 클릭 완료!")
            
            # 메인 프레임에서 나가기
            self.driver.switch_to.default_content()
            
            print("✅ 테스트 포스트 작성이 완료되었습니다!")
            return True
            
        except Exception as e:
            print(f"글 작성 중 오류 발생: {str(e)}")
            # 오류 발생 시 메인 프레임에서 나가기
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            return False
    
    def keep_alive(self):
        """브라우저 상태 유지"""
        try:
            while self.keep_running:
                # 브라우저가 닫혔는지 확인
                try:
                    self.driver.current_url  # 브라우저 상태 체크
                    time.sleep(10)  # 10초마다 체크
                except:
                    print("브라우저가 사용자에 의해 종료되었습니다.")
                    self.keep_running = False
                    break
        except Exception as e:
            print(f"상태 유지 중 오류: {str(e)}")
    
    def run(self):
        """전체 프로세스 실행"""
        try:
            if self.login_to_naver():
                if self.go_to_blog_write():
                    print("\n" + "="*70)
                    print("성공! 네이버 블로그 글쓰기 페이지에 접속했습니다!")
                    print("="*70)
                    print("")
                    print("브라우저가 열린 상태로 계속 유지됩니다.")
                    print("자유롭게 글을 작성하세요!")
                    print("")
                    print("프로그램을 종료하려면:")
                    print("- 브라우저를 직접 닫거나")
                    print("- Ctrl+C를 눌러주세요")
                    print("")
                    print("브라우저 상태를 모니터링 중입니다...")
                    
                    # 백그라운드에서 브라우저 상태 유지
                    monitor_thread = threading.Thread(target=self.keep_alive)
                    monitor_thread.daemon = True
                    monitor_thread.start()
                    
                    # 무한 대기 (브라우저가 닫힐 때까지)
                    try:
                        while self.keep_running:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print("\n프로그램이 사용자에 의해 종료되었습니다.")
                        self.keep_running = False
                    
                    print("프로그램이 종료됩니다.")
                    return True
                else:
                    print("블로그 글쓰기 페이지 이동 실패")
                    return False
            else:
                print("로그인 실패")
                return False
                
        except Exception as e:
            print(f"실행 중 오류: {str(e)}")
            return False
    
    def close(self):
        """브라우저 종료"""
        self.keep_running = False
        if self.driver:
            try:
                self.driver.quit()
                print("브라우저가 종료되었습니다.")
            except:
                pass

if __name__ == "__main__":
    print("="*70)
    print("네이버 블로그 자동 로그인 프로그램 (브라우저 계속 유지)")
    print("="*70)
    
    try:
        import pyperclip
    except ImportError:
        print("pyperclip 모듈이 필요합니다.")
        print("다음 명령어로 설치하세요: pip install pyperclip")
        exit()
    
    blog_writer = NaverBlogWriter()
    
    try:
        blog_writer.run()
        
    except KeyboardInterrupt:
        print("\n프로그램이 중단되었습니다.")
    
    except Exception as e:
        print(f"\n오류가 발생했습니다: {str(e)}")
    
    finally:
        blog_writer.close()
        print("감사합니다!")