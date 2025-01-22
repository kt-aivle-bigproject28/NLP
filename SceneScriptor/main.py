import json
from gpt_api import initialize_openai, call_gpt_to_extract_features
from characteristic_parser import parse_gpt_result_to_json
from file_reader import read_text_from_file
from text_processing import slice_text
from model_inference import load_model_and_tokenizer, generate_output
from json_parser import parse_output_to_json  # JSON 파싱 함수

def slice_and_process_text(input_file_path, slice_num=20000, chunk_size=500):
    """
    텍스트를 자르고 모델을 통해 처리하여 JSON으로 변환합니다.
    """
    # 모델과 토크나이저 기본값을 사용
    model_path = "kobart-summarization-finetuned"
    tokenizer_path = "kobart-summarization-finetuned"

    # 텍스트 파일 읽기
    with open(input_file_path, 'r', encoding='utf-8') as f:
        input_txt = f.read()

    # 텍스트 청크로 나누기
    chunks = slice_text(input_txt, slice_num, chunk_size)

    # 모델과 토크나이저 로드
    tokenizer, model = load_model_and_tokenizer(model_path, tokenizer_path)

    # 청크별로 처리
    for idx, chunk in enumerate(chunks):
        generated_output = generate_output(tokenizer, model, chunk)
        parsed_output = parse_output_to_json(generated_output)
        # JSON 출력
        print(json.dumps(parsed_output, indent=4, ensure_ascii=False))

        # 사용자 확인 후 다음 청크 진행
        user_input = input(f"청크 {idx + 1} 처리를 완료하려면 '완료'를 입력하세요: ")
        if user_input.strip().lower() != "완료":
            print("작업을 중단합니다.")
            break

def main(input_path):
    """
    전체 흐름을 관리하는 메인 함수
    1. 텍스트 파일을 읽고 GPT로 특징 및 배경 추출
    2. 추출된 정보를 기반으로 텍스트를 청크로 나누어 모델 처리
    """
    
    initialize_openai()
    
    # 1. 텍스트 파일을 읽고 GPT 호출하여 배경과 인물 특징 추출
    text = read_text_from_file(input_path)
    if text:
        # GPT 호출하여 텍스트 처리
        result = call_gpt_to_extract_features(text)

        if result:
            # JSON 변환
            parsed_data = parse_gpt_result_to_json(result)

            # 변환된 JSON 확인
            print(json.dumps(parsed_data, ensure_ascii=False, indent=4))
        else:
            print("GPT로부터 결과를 얻는 데 실패했습니다.")
    else:
        print("파일을 읽는 데 실패했습니다.")

    # 2. 텍스트를 청크로 나누고 모델을 통해 처리
    slice_and_process_text(input_path)

if __name__ == "__main__":
    input_path = input("텍스트 파일 경로를 입력하세요: ").strip('""')
    main(input_path)
