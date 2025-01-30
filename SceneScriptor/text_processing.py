import re

def preprocess_and_split(input_txt, slice_num=10000, chunk_size=250):
    """
    텍스트 전처리 및 청크 분리 함수
    """
    # 텍스트 전처리
    input_txt = input_txt.replace('*', '').replace('◆', '').replace('◇', '')
    input_txt = re.sub(r'\s+', ' ', input_txt)  # 연속된 공백 제거
    input_txt = input_txt.replace('\n', ' ').replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    input_txt = re.sub(r'\([^가-힣]*[\u4E00-\u9FFF\u3040-\u30FF]+[^가-힣]*\)', '', input_txt)  # 괄호 안 한자/일본어 제거
    input_txt = re.sub(r'[\u4E00-\u9FFF\u3040-\u30FF]+', '', input_txt)  # 한자/일본어 제거
    input_txt = input_txt[:slice_num]  # 지정된 크기만큼 자르기
    
    chunks = []
    buffer = ""
    is_open_double_quote = False
    is_open_single_quote = False
    
    for char in input_txt:
        buffer += char

        if char == '"':
            is_open_double_quote = not is_open_double_quote
        elif char == "'":
            is_open_single_quote = not is_open_single_quote
        
        if len(buffer) >= chunk_size:
            if char in ['.', '!', '?'] and not is_open_double_quote and not is_open_single_quote:
                chunks.append(buffer.strip())
                buffer = ""
            elif char in ['"'] and len(buffer) > 3 and buffer[-3] in ['"']:
                chunks.append(buffer[:-1].strip())
                buffer = '"'
            elif char in ["'"] and len(buffer) > 3 and buffer[-3] in ["'"]:
                chunks.append(buffer[:-1].strip())
                buffer = "'"
            elif re.search(r'\.\.\.|!!|\?\?', buffer):
                match = re.search(r'(\.\.\.|!!|\?\?)', buffer)
                split_index = match.end()
                chunks.append(buffer[:split_index].strip())
                buffer = buffer[split_index:].strip()
    
    if buffer:
        chunks.append(buffer.strip())
    
    # 마지막 청크 삭제
    if chunks:
        chunks.pop()
    
    return chunks, input_txt
