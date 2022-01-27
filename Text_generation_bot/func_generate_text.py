def generate_text(prompt):
    
    import torch
    from transformers import GPT2Tokenizer 

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    model = torch.load('model_M_P.pt', map_location=device) # загружаем (предтренерованную на произведении) модель
    

    tokenizer = GPT2Tokenizer.from_pretrained('sberbank-ai/rugpt3small_based_on_gpt2') # загружаем токенайзер
    prompt = tokenizer.encode(prompt, return_tensors='pt').to(device)

    out = model.generate(
        input_ids=prompt, # строка для начала генерации
        max_length=90, # длину последовательности, которую хотим получит
        num_beams=5, # колв-во веток
        do_sample=True, # семплируем/нет
        temperature=40., # температура
        top_k=30, # кол-во слов, которые расмативаем
        top_p=0.9, # суммараня вероятность
        no_repeat_ngram_size=3, # которые НЕ повторять
        num_return_sequences=1, # сколько текстов будет сгенерировано
        ).cpu().numpy()
        
    my_out = tokenizer.decode(out[0])
    return my_out