import re
import json

def clean_text(text):
    """
    텍스트에서 불필요한 문자나 특수 문자를 제거합니다.
    """
    if not isinstance(text, str):
        return text
    # 앞뒤 공백 제거
    text = text.strip()
    # 이스케이프 문자 제거
    text = text.replace("\\", "")
    # 불필요한 따옴표 제거
    text = re.sub(r'^["\']|["\']$', '', text)
    # 불필요한 ']', '[', 개행 문자 제거
    text = text.replace("]", "").replace("[", "").replace("\n", " ").strip()
    return text

def parse_output_to_json(generated_output):
    """
    모델의 출력 결과를 JSON 형식으로 변환하며, 텍스트를 전처리합니다.
    """
    parsed_data = {}
    try:
        # [location] 매칭
        location_match = re.search(r"\[location\]\s*(.+)", generated_output)
        parsed_data["location"] = clean_text(location_match.group(1)) if location_match else None

        # [caption] 매칭
        caption_match = re.search(r"\[caption\]\s*(.+)", generated_output)
        parsed_data["caption"] = clean_text(caption_match.group(1)) if caption_match else None

        # [dialogues] 매칭 및 처리
        dialogues_match = re.search(r"\[dialogues\]\s*(\[.+)", generated_output, re.DOTALL)
        if dialogues_match:
            dialogues_raw = dialogues_match.group(1).strip()
            # 다중 speaker와 dialogue 추출
            dialogue_list = re.findall(r"\[speaker\]\s*(.+?)\s*\[dialogue\]\s*(.+?)(?=\[speaker\]|\Z)", dialogues_raw, re.DOTALL)
            parsed_data["dialogues"] = [
                {
                    "speaker": clean_text(speaker.strip()),
                    "dialogue": clean_text(dialogue.strip())
                } for speaker, dialogue in dialogue_list
            ]
        else:
            parsed_data["dialogues"] = []  # dialogues가 없는 경우 빈 리스트 반환

        return parsed_data
    except Exception as e:
        # 예외 발생 시 에러 메시지 포함
        print(f"JSON 디코딩 실패! 출력: {generated_output}")
        print(f"에러 메시지: {e}")
        return {}