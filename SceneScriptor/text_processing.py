import re

def slice_text(input_txt, slice_num=20000, chunk_size=500):
    """
    텍스트를 지정된 길이로 자르고, 청크로 나눕니다.
    """
    input_txt = input_txt.replace('\n', ' ')
    input_txt = input_txt[:slice_num]  # 지정된 크기만큼 자르기

    # 문장 끝 패턴 정의 및 분리
    sentence_end_pattern = re.compile(r'([.!?]["”]?\s)')
    sentences = sentence_end_pattern.split(input_txt)

    # 문장을 청크로 나누기
    chunks = []
    current_chunk = ""

    for i in range(0, len(sentences) - 1, 2):
        sentence = sentences[i] + sentences[i + 1]
        if len(current_chunk) + len(sentence) > chunk_size:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks