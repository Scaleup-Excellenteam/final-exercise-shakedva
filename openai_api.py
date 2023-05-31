import openai
import os
import time

openai.api_key = os.getenv('OPENAI_API_KEY')


class OpenaiApi:
    """
    Connects tto the OpenAi API, sends a prompt to summarize a slide.
    """
    PROMPT = "Please summarize the key points from slide number {slide_index} titled '{file_title}' simply: {" \
             "slide_text} "
    REQUEST_WAIT_TIME = 60
    DEFAULT_MODEL = "gpt-3.5-turbo"

    @classmethod
    async def get_model_response(cls, gpt_outputs, prompt_content, model=DEFAULT_MODEL):
        """
        Connect to OpenAi API, sends a prompt to summarize a slide and saves the results in a list of outputs.
        :param gpt_outputs: list of the explanation from the api.
        :param prompt_content: str the prompt to send to the api.
        :param model: the AI model
        """
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