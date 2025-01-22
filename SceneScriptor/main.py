import json
from text_processing import slice_text
from model_inference import load_model_and_tokenizer, generate_output
from json_parser import parse_output_to_json  

def slice_and_process_text(input_file_path, model_path, tokenizer_path, slice_num=20000, chunk_size=500):
    """
    텍스트를 자르고 모델을 통해 처리하여 JSON으로 변환합니다.
    """
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
        print(f"청크 {idx + 1} 결과:")
        print(json.dumps(parsed_output, indent=4, ensure_ascii=False))

        # 사용자 확인 후 다음 청크 진행
        user_input = input(f"청크 {idx + 1} 처리를 완료하려면 '완료'를 입력하세요: ")
        if user_input.strip().lower() != "완료":
            print("작업을 중단합니다.")
            break

# 실행 예시
if __name__ == "__main__":
    input_path = input("텍스트 파일 경로를 입력하세요: ").strip('""')
    model_path = "kobart-summarization-finetuned"
    tokenizer_path = "kobart-summarization-finetuned"
    slice_and_process_text(input_path, model_path, tokenizer_path)