from src.load_dataset.load_arc_subset import load_library, extract_python_code, remove_print, task_filter, generate_input_num, generate_output_by_code, get_transformation_rule
import argparse
from src.utils.llm.main import get_llm, add_llm_args
from src.utils.logger import get_logger
from src.build_library.prompt.generate_tasks_prompt import generate_system, content_prompt, generate_system2
from src.build_library.prompt.transform_concept_library import get_transformation_library
from src.load_dataset.vis_data_per_task import visualize_data
from src.utils.sample_dpp import get_dpp
from src.utils.html_vis import get_html_vis
import random
import json
def main(generator_number = 1):
    double_check = True
    parser = argparse.ArgumentParser()
    add_llm_args(parser)
    args = parser.parse_args()
    llm = get_llm(args)
    logger = get_logger('input_hypo', args)
    # 123 42
    json_record = []
    
    rng = random.Random(42)
    # random.seed(42)
    concept_library = load_library("merge")
    transform_library = concept_library['transformation_library']
    object_library = concept_library['object_library']
    grid_library = concept_library['grid_library']
    html_description = []
    cnt = 0

    cur_description = get_dpp(transform_library, 42, 150)
    # cur_description2 = get_dpp(transform_library, 123, 150)
    round_num = 0
    while(cnt < 100):
        # transformation_hint  = rng.sample(transform_library, 1)
        # object_hint = rng.sample(object_library, 1)
        # grid_hint = rng.sample(grid_library, 1)
        # transformation_hint_str = ""
        # for hints in transformation_hint:
        #     transformation_hint_str += hints + '\n'
        # transformation_hint = "1. " + cur_description[round_num] + '\n' + "2. " + cur_description2[round_num]
        transformation_hint = cur_description[round_num]

        # print(transformation_hint)
        # exit(0)
        # Object description: {object_hint}
        round_num += 1
        hint = f"""
Transformation rule: {transformation_hint}
"""     
        prompt = [
            {"role": "system", "content": generate_system2},
            {"role": "user", "content": content_prompt(hint)}
        ]
        
        logger.info(f"HINT: {hint}")
        for i in range(3):
            # logger.info(content_prompt(hint))
            response = llm(prompt).choices[0].message.content
            logger.info(response)
            transformation_rule, object_description = get_transformation_rule(response) 
            # print(response)
            # print("**")
            # print(transformation_rule)
            # print(object_description)
            # exit()
            logger.info(f"Transformation rule: {transformation_rule}")
            logger.info(f"Object description: {object_description}")           
            code = extract_python_code(response)[0]
            code = remove_print(code)
            if code.strip() == "":
                print(response)
                print("*"*10)
                print(extract_python_code(response)[0])
                exit()
            inputs = generate_input_num(5, code)
            if double_check:
                inputs2 = generate_input_num(5, code)
                if inputs2 != inputs:
                    print("Input double check failed")
                    # print(inputs)
                    # print(inputs2)
                    print(code)
                    # exit()
                    continue
            logger.info(code)
            # print(inputs)
            # exit(0)
            outputs = generate_output_by_code(inputs, code)
            if double_check:
                outputs2 = generate_output_by_code(inputs, code)
                if outputs2 != outputs:
                    print("Output double check failed")
                    continue

            # print(outputs)
            if not task_filter(outputs):
                continue
            try:
                visualize_data(outputs, cnt, generator_number)
                cnt += 1
                json_record.append({'task': cnt, 'transformation_rule': transformation_rule, 'hint': hint, "object_description": object_description,'generator': code, 'results': outputs})
                html_description.append(f"Transformation rule:\n{transformation_rule}\n\nObject description:\n{object_description}\n\nhint:\n{hint}\n")
                break
            except Exception as e:
                print(e)
        
        
        logger.info(response)
    usage = llm.tracker.usage
    print(usage)
    print("Total requests ",usage['requests'], " Generate requests ", cnt, "Concept num", round_num)
    prompt_price = 0.01 * usage['prompt_tokens'] * 1e-3
    completion_price = 0.03 * usage['completion_tokens'] * 1e-3
    print(f"Prompt price: {prompt_price:.2f}Completion price: {completion_price:.2f} Total price: {(prompt_price + completion_price):.2f}")
    logger.info(f"Prompt price: {prompt_price:.2f}Completion price: {completion_price:.2f} Total price: {(prompt_price + completion_price):.2f}")
    with open(f'result/vis/cat_img/code_{generator_number}.json','w') as f:
        json.dump(json_record, f, indent=4)
    with open(f'result/vis/cat_img/vis_{generator_number}.html', 'w') as f:
        html_content = get_html_vis(html_description, cnt)
        f.write(html_content)
        # print(response)
        
main(1)
main(2)