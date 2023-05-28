import openai
import os
import time

openai.api_key = os.getenv('OPENAI_API_KEY')


class OpenaiApi:
    PROMPT = "Please summarize the key points from slide number {slide_index} titled '{file_title}' simply: {" \
             "slide_text} "
    REQUEST_WAIT_TIME = 60

    DEFAULT_MODEL = "gpt-3.5-turbo"

    @classmethod
    async def get_model_response(cls, gpt_outputs, prompt_content, model=DEFAULT_MODEL):
        while True:
            try:
                completion = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": OpenaiApi.PROMPT.format(**prompt_content)
                        }
                    ]
                )
                gpt_outputs.append(completion.choices[0].message.content)
                break
            except openai.error.RateLimitError:
                time.sleep(OpenaiApi.REQUEST_WAIT_TIME)
