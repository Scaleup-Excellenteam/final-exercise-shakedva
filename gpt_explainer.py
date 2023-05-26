from pptx import Presentation
import asyncio
FILE_PATH = r'C:\Users\shake\Desktop\College\4th Year\Semester B\Excellenteam\python\Ex\Tests demo.pptx'


async def parse_slide(slide):
    slide_text = []
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for paragraph in shape.text_frame.paragraphs:
            for run in paragraph.runs:
                run_text = run.text.strip()
                if run_text:
                    slide_text.append(run_text)

    print(slide_text)
    return slide_text


async def main():
    tasks = []
    prs = Presentation(FILE_PATH)
    for index, slide in enumerate(prs.slides):
        tasks.append(parse_slide(slide))
    await asyncio.gather(*tasks)
    print("finish")


if __name__ == "__main__":
    asyncio.run(main())
