import asyncio
import json
import os

from openai_api import OpenaiApi
from pptx_parser import PptxParser


class GptPptxExplainer:

    @classmethod
    async def explain(cls, file_path):
        base_file_name = os.path.basename(file_path)
        tasks = []
        gpt_outputs = []
        for index, slide_text in PptxParser.parse(file_path):
            prompt_content = {
                'slide_index': index,
                'file_title': base_file_name,
                'slide_text': slide_text
            }
            tasks.append(
                OpenaiApi.get_model_response(gpt_outputs, prompt_content)
            )
        await asyncio.gather(*tasks)
        with open(f'{os.path.splitext(file_path)[0]}_explained.json', 'w') as f:
            f.write(json.dumps(gpt_outputs))


if __name__ == "__main__":
    file_path = input("Enter a pptx file path: ")
    asyncio.run(GptPptxExplainer.explain(file_path))
