import json
import os
from file_reader import read_file
from text_processing import preprocess_and_split  
from model_inference import load_model_and_tokenizer, generate_output
from json_parser import parse_output_to_json, parse_gpt_result_to_json
from gpt_api import call_gpt_to_extract_features, initialize_openai  

# api key 불러오기
initialize_openai() 

def slice_and_process_text(input_file_path):
    """
    텍스트를 자르고 모델을 통해 처리하여 JSON으로 변환합니다.
    """
    input_txt = read_file(input_file_path, slice_num=10000)  # ✅ slice_num 추가
    if input_txt is None:
        return None

    chunks, processed_text  = preprocess_and_split(input_txt, slice_num=10000, chunk_size=250)
    tokenizer, model = load_model_and_tokenizer()
    if tokenizer is None or model is None:
        print("❌ 모델 로딩 실패! 프로그램을 종료합니다.")
        return None

    final_output = []
    
    for idx, chunk in enumerate(chunks):
        generated_output = generate_output(tokenizer, model, chunk)
        parsed_output = parse_output_to_json(generated_output)
        final_output.append(parsed_output)

    return final_output, processed_text  

if __name__ == "__main__":
    input_path = input("텍스트 또는 PDF 파일 경로를 입력하세요: ").strip('""')
    final_output, input_txt  = slice_and_process_text(input_path)

    if final_output:
        text = read_file(input_path)

        gpt_result = call_gpt_to_extract_features(input_txt, final_output)
        if gpt_result:
            parsed_data = parse_gpt_result_to_json(gpt_result)
            print(json.dumps(parsed_data, ensure_ascii=False, indent=4))
        else:
            print("GPT로부터 결과를 얻는 데 실패했습니다.")

        # 사용자가 완료를 입력하면 시나리오 출력 시작
        user_input = input("\n 인물 특징 및 시대적 배경 출력을 완료하려면 '완료'를 입력하세요: ")
        if user_input.strip().lower() == "완료":
            # 청크별 출력
            for idx, chunk in enumerate(final_output, start=1):
                print(json.dumps(chunk, ensure_ascii=False, indent=4))
                user_input = input(f"\n 청크 {idx} 처리를 완료하려면 '완료'를 입력하세요: ")
                if user_input.strip().lower() != "완료":
                    print("작업을 중단합니다.")
                    break
