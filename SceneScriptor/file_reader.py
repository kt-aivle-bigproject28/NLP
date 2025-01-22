def read_text_from_file(file_path):
    """
    주어진 파일 경로에서 텍스트를 읽고 반환합니다.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as e:
        print(f"파일을 찾을 수 없습니다: {e}")
        return None