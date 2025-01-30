import openai

def initialize_openai():
    """
    OpenAI API 초기화
    """
   
    with open(r"C:\Users\User\Documents\GitHub\NLP\SceneScriptor\open_api_key.txt", "r", encoding="utf-8") as file:
        openai.api_key = file.read().strip()
    
# 외모 생김새 추출 모델
def call_gpt_to_extract_features(text, final_output):
    """
    GPT-3.5 Turbo를 사용하여 전체 텍스트에서 외모적 특징과 시대적 배경을 추출.
    """
    # 외모 생김새 추출을 위한 고정 input_person 생성
    input_person = set()
    for item in final_output:
        for dialogue in item.get("dialogues", []):
            speaker = dialogue.get("speaker")
            if speaker:  # speaker가 None이 아닌 경우에만 추가
                input_person.add(speaker)
    
        # 문자열 변환
    input_person_list = ", ".join(sorted(input_person)) 
    print(input_person_list)

    prompt = f"""
    반드시 지정한 인물({input_person_list}) 들만 외모적 생김새를 아래 형식에 맞게 추출하세요.
    **모든 인물에 대한 정보를 반드시 포함하세요.**
    **각각의 인물이 빠짐없이 출력되어야 합니다.**
    **명확한 정보가 없는 경우 최대한 추론하여 기재하세요.**

    1. **출력 형식**:
       ```
       [시대적 배경] 시대적 배경 설명
       [이름] 성별, 머리 길이, 나이대, 체격 / 없다면 작성 하지 말 것
       ```
       - 각 인물은 한 줄로 작성합니다.
       - 반드시 위의 출력 형식을 따르세요.

    2. **시대적 배경**:
       - 시대적 배경을 간결하게 서술합니다.

    3. **인물 정보**:
       - 각 인물의 정보를 아래 형식에 맞게 작성하세요:
         `[이름] 성별, 머리 길이, 나이대, 체격`
       - 이름이 없는 인물은 맥락에 따라 논리적으로 추론하여 작성하세요.
       - 포함되지 않은 요소는 생략하세요.

    4. **주의 사항**:
       - 명시적 정보가 없는 경우 논리적으로 추론하여 작성하세요.
       - 모호한 표현은 절대 사용하지 마세요.
       - 인물에 대한 외모 생김새만 추출하세요.

    5. **예시 출력**:
       ```
       [시대적 배경] 21세기 현대, 일반적인 도시 생활의 풍경

       [수지] 여성, 짧은 머리, 30대 초반,검은 눈동자, 날씬한 체격
       [정국] 남성, 긴 머리, 30대 초반,검은 눈동자, 건강한 체격
       [랩몬스터] 남성, 20대 초반
       [이수만] 남성, 60대
       ```
    {text}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=.3
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error during GPT call: {e}")
        return None
