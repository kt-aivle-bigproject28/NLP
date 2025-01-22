import openai

def initialize_openai():
    """
    OpenAI API 초기화
    """
   
    with open(r"C:\Users\User\Documents\GitHub\NLP\SceneScriptor\open_api_key.txt", "r") as file:
        openai.api_key = file.read().strip()
    
def call_gpt_to_extract_features(text):
    """
    GPT-4 Turbo를 사용하여 전체 텍스트에서 외모적 특징과 시대적 배경을 추출.
    """
    prompt = f"""
    아래 텍스트에서 등장하는 시대적 배경과 모든 인물의 외모적 생김새를 다음 조건에 맞게 추출하세요:
    - 시대적 배경은 텍스트의 시간적, 공간적 환경을 간결히 서술하세요.
    - 각 인물의 생김새를 [이름] 형식으로 간결히 표현하세요.
    - 인물의 외모적 생김새에는 다음 요소만 포함하세요:
      1. 성별 (남성/여성)
      2. 머리 길이 (짧은 머리, 긴 머리 등)
      3. 눈동자 색 (검은 눈동자, 푸른 눈동자 등)
      4. 나이대 (어린아이, 청소년, 성인, 노인)
      5. 체격 (마른 체격, 건장한 체격, 비만한 체격 등)
    - 텍스트에서 명시적 정보가 없더라도, 맥락과 논리적으로 추론 가능한 경우에는 정보를 작성하세요.
    - 단, 추론이 가능하지 않은 경우 해당 인물은 출력하지 마세요.
    - "정보 없음", "가능성이 보임"과 같은 모호한 표현은 절대 사용하지 마세요.
    - 모든 인물을 포함하되, 각 인물은 구체적인 정보를 바탕으로 출력하세요.
    - 1인칭 시점의 화자는 "나" 또는 "나레이터"로 출력하지 말고, 맥락에 따라 이름을 유추하세요.
    - 반드시 예시 출력 형식에 맞게 작성하세요.

    출력 형식:
    [시대적 배경] (시대적 배경 정보)
    [이름] 성별, 머리 길이, 눈동자 색, 나이대, 체격

    예시 출력:
    [시대적 배경] 1940년대~1960년대 미국, 메인 주의 쇼생크 주립교도소
    [앤디 듀프레인] 남성, 짧은 머리, 푸른 눈동자, 성인, 마른 체격
    [레드] 남성, 짧은 머리, 검은 눈동자, 성인, 보통 체격
    [보그 다이아몬드] 남성, 짧은 머리, 검은 눈동자, 성인, 건장한 체격

    텍스트:
    {text}
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=1
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error during GPT call: {e}")
        return None