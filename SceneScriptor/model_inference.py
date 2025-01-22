from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

def load_model_and_tokenizer(model_path, tokenizer_path):
    """
    모델과 토크나이저를 로드합니다.
    """
    tokenizer = PreTrainedTokenizerFast.from_pretrained(tokenizer_path)
    model = BartForConditionalGeneration.from_pretrained(model_path)
    return tokenizer, model

def generate_output(tokenizer, model, text, max_length=512):
    """
    모델을 통해 텍스트를 처리하고 출력합니다.
    """
    inputs = tokenizer(text, return_tensors="pt", padding="max_length", truncation=True, max_length=max_length)
    output_ids = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=max_length,
        num_beams=4,
        length_penalty=1.0,
        early_stopping=True,
    )
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)
