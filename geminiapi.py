import google.generativeai as genai
import os


class GeminiAPI:
    def __init__(self, api_key="AIzaSyDj0ejAhXNSydhVHdcLDUFuirq4Xhy2B0I"):
        """
        Gemini API 클래스 초기화
        
        Args:
            api_key (str): Gemini API 키
        """
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def generate_text(self, prompt, temperature=0.7, max_output_tokens=1024):
        """
        텍스트 생성
        
        Args:
            prompt (str): 입력 프롬프트
            temperature (float): 창의성 수준 (0.0-1.0)
            max_output_tokens (int): 최대 출력 토큰 수
            
        Returns:
            str: 생성된 텍스트
        """
        try:
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            return response.text
        except Exception as e:
            print(f"텍스트 생성 중 오류 발생: {str(e)}")
            return None
    
    def chat_conversation(self, messages):
        """
        대화형 채팅
        
        Args:
            messages (list): 메시지 리스트
            
        Returns:
            str: 응답 텍스트
        """
        try:
            chat = self.model.start_chat(history=[])
            response = chat.send_message(messages[-1] if isinstance(messages, list) else messages)
            return response.text
        except Exception as e:
            print(f"채팅 중 오류 발생: {str(e)}")
            return None
    
    def analyze_image(self, image_path, prompt="이미지를 분석해주세요."):
        """
        이미지 분석
        
        Args:
            image_path (str): 이미지 파일 경로
            prompt (str): 분석 요청 프롬프트
            
        Returns:
            str: 이미지 분석 결과
        """
        try:
            import PIL.Image
            image = PIL.Image.open(image_path)
            
            response = self.model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            print(f"이미지 분석 중 오류 발생: {str(e)}")
            return None
    
    def summarize_text(self, text):
        """
        텍스트 요약
        
        Args:
            text (str): 요약할 텍스트
            
        Returns:
            str: 요약된 텍스트
        """
        prompt = f"다음 텍스트를 간결하게 요약해주세요:\n\n{text}"
        return self.generate_text(prompt)
    
    def translate_text(self, text, target_language="영어"):
        """
        텍스트 번역
        
        Args:
            text (str): 번역할 텍스트
            target_language (str): 목표 언어
            
        Returns:
            str: 번역된 텍스트
        """
        prompt = f"다음 텍스트를 {target_language}로 번역해주세요:\n\n{text}"
        return self.generate_text(prompt)


def main():
    """예제 사용법"""
    gemini = GeminiAPI()
    
    print("=== Gemini API 테스트 ===\n")
    
    # 1. 기본 텍스트 생성
    print("1. 텍스트 생성 테스트:")
    response = gemini.generate_text("안녕하세요! 파이썬으로 할 수 있는 재미있는 프로젝트 3가지를 추천해주세요.")
    if response:
        print(response)
    print("\n" + "="*50 + "\n")
    
    # 2. 채팅 대화
    print("2. 채팅 대화 테스트:")
    chat_response = gemini.chat_conversation("오늘 날씨가 어때요?")
    if chat_response:
        print(chat_response)
    print("\n" + "="*50 + "\n")
    
    # 3. 텍스트 요약
    print("3. 텍스트 요약 테스트:")
    long_text = """
    인공지능(AI)은 컴퓨터 시스템이 일반적으로 인간의 지능이 필요한 작업을 수행할 수 있도록 하는 기술입니다. 
    여기에는 학습, 추론, 문제 해결, 인식 및 언어 이해가 포함됩니다. 
    AI는 머신러닝, 딥러닝, 자연어 처리 등 다양한 기술을 활용하여 구현됩니다. 
    현재 AI는 의료, 교육, 금융, 교통 등 다양한 분야에서 활용되고 있으며, 
    앞으로도 더욱 발전하여 인간의 삶을 개선하는 데 기여할 것으로 예상됩니다.
    """
    summary = gemini.summarize_text(long_text)
    if summary:
        print(summary)
    print("\n" + "="*50 + "\n")
    
    # 4. 번역
    print("4. 번역 테스트:")
    translation = gemini.translate_text("안녕하세요, 오늘은 좋은 날씨네요.", "영어")
    if translation:
        print(translation)


if __name__ == "__main__":
    main()