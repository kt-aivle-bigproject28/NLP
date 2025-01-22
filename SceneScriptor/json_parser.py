import re

def parse_output_to_json(generated_output):
    parsed_data = {}
    try:
        # [location] 매칭
        location_match = re.search(r"\[location\]\s*(.+)", generated_output)
        if location_match:
            parsed_data["location"] = location_match.group(1).strip()

        # [caption] 매칭
        caption_match = re.search(r"\[caption\]\s*(.+)", generated_output)
        if caption_match:
            parsed_data["caption"] = caption_match.group(1).strip()

        # [dialogues] 매칭 및 처리
        dialogues_match = re.search(r"\[dialogues\]\s*(\[.+)", generated_output, re.DOTALL)
        if dialogues_match:
            dialogues_raw = dialogues_match.group(1).strip()
            # 단일 speaker와 dialogue만 추출
            dialogue_data = re.search(r"\[speaker\]\s*(.+?)\s*\[dialogue\]\s*(.+?)(?=\[speaker\]|\Z)", dialogues_raw, re.DOTALL)
            if dialogue_data:
                parsed_data["dialogues"] = {
                    "speaker": dialogue_data.group(1).strip(),
                    "dialogue": re.sub(r"\s*\n\s*\]$", "", dialogue_data.group(2).strip())  # 닫는 대괄호 제거
                }

    except Exception as e:
        # 예외 발생 시 에러 메시지 포함
        parsed_data["error"] = f"Parsing error: {str(e)}"
        parsed_data["content"] = generated_output
    
    return parsed_data
