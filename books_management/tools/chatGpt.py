import openai

openai.api_key = "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"

while True:
    prompt = input("请输入：")
    model_engine = "text-davinci-003"
    response = openai.Completion.create(
        engine = model_engine,
        prompt = prompt,
        max_tokens = 3000,
        n = 1,
        stop = None,
        temperature = 0

    )
    print(f"chatGpt：{response.choices[0].text.strip()}")