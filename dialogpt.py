# INSTANTIATE HUGGING FACE MODEL
# from transformers import AutoTokenizer, AutoModelForCausalLM

# hf_token = os.getenv('HUGGING_FACE_TOKEN')
# tokenizer = AutoTokenizer.from_pretrained("Youshiko/DialoGPT-medium-Thanos")
# model = AutoModelForCausalLM.from_pretrained("Youshiko/DialoGPT-medium-Thanos")
# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token     

# inputs = tokenizer(message.content + tokenizer.eos_token, return_tensors='pt', padding=True, truncation=True)

# chat_history_ids = model.generate(
#     inputs['input_ids'],
#     attention_mask=inputs['attention_mask'],
#     max_length=250,
#     pad_token_id=tokenizer.eos_token_id,
#     temperature=0.7,
#     do_sample=True,
#     top_k=50,
#     top_p=0.9,
#     repetition_penalty=1.2
# )

# response = tokenizer.decode(chat_history_ids[:, inputs['input_ids'].shape[-1]:][0], skip_special_tokens=True)