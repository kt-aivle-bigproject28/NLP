import re

def parse_gpt_result_to_json(result):
    """
    GPT 모델 결과를 JSON 형태로 변환
    """
    try:
        # 텍스트를 라인별로 분리
        lines = result.strip().split("\n")

        # 시대적 배경 추출
        background = None
        characters = []

        for line in lines:
            if line.startswith("[시대적 배경]"):
                background = line.replace("[시대적 배경] ", "").strip()
            elif line.startswith("[") and "]" in line:
                name, appearance = line.split("]", 1)
                characters.append({
                    "name": name.replace("[", "").strip(),
                    "appearance": appearance.strip()
                })

        # 모든 캐릭터 포함한 JSON 반환
        data = {
            "background": background,
            "characters": characters
        }
        return data

    except Exception as e:
        return {"error": f"Failed to parse result: {e}"}