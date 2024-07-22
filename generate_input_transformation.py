from src.load_dataset.load_arc_subset import load_library, extract_python_code, remove_print, task_filter, generate_input_num, generate_output_by_code
import argparse
from src.utils.llm.main import get_llm, add_llm_args
from src.utils.logger import get_logger
from src.build_library.prompt.generate_tasks_prompt import generate_system, content_prompt
from src.build_library.prompt.transform_concept_library import get_transformation_library
from src.load_dataset.vis_data_per_task import visualize_data
import random
import json
def main():
    parser = argparse.ArgumentParser()
    add_llm_args(parser)
    args = parser.parse_args()
    llm = get_llm(args)
    logger = get_logger('input_hypo', args)
    # 123 42
    
    rng = random.Random(42)
    # random.seed(42)
    concept_library = load_library(3)
    transform_library = concept_library['transformation_library']
    object_library = concept_library['object_library']
    grid_library = concept_library['grid_library']
    cnt = 0
    while(cnt < 40):
        transformation_hint  = rng.sample(transform_library, 1)
        object_hint = rng.sample(object_library, 1)
        grid_hint = rng.sample(grid_library, 1)
        hint = f"""
Transformation rule: {transformation_hint[0]}
"""     
        prompt = [
            {"role": "system", "content": generate_system},
            {"role": "user", "content": content_prompt(hint)}
        ]
        
        logger.info(hint)
        # logger.info(content_prompt(hint))
        response = llm(prompt).choices[0].message.content
        
        code = extract_python_code(response)[0]
        code = remove_print(code)
        if code.strip() == "":
            print(response)
            print("*"*10)
            print(extract_python_code(response)[0])
            exit()
        inputs = generate_input_num(4, code)
        logger.info(code)
        # print(inputs)
        # exit(0)
        outputs = generate_output_by_code(inputs, code)
        # print(outputs)
        if not task_filter(outputs):
            continue
        try:
            visualize_data(outputs, cnt, 1)
        except Exception as e:
            print(e)
        
        logger.info(response)
        # print(response)
        cnt += 1
main()