from src.load_dataset.load_arc_subset import load_library, extract_python_code, remove_print, task_filter, generate_input_num, generate_output_by_code, get_transformation_rule
import argparse
from src.utils.llm.main import get_llm, add_llm_args
from src.utils.logger import get_logger
from src.build_library.prompt.generate_tasks_prompt import generate_system, content_prompt, generate_system2, content_prompt_strict
from src.build_library.prompt.transform_concept_library import get_transformation_library
from src.load_dataset.vis_data_per_task import visualize_data
from src.utils.sample_dpp import get_dpp
from src.utils.html_vis import get_html_vis, get_html_vis_double
import random
import json


def generate_input_output(logger, hint, llm, double_check, cnt, generator_number, json_record, html_description):
    prompt = [
        {"role": "system", "content": generate_system2},
        {"role": "user", "content": content_prompt_strict(hint)}
    ]
    
    logger.info(f"HINT: {hint}")
    for i in range(3):
        response = llm(prompt).choices[0].message.content
        logger.info(response)
        transformation_rule, object_description = get_transformation_rule(response) 

        logger.info(f"Transformation rule: {transformation_rule}")
        logger.info(f"Object description: {object_description}")   
        try:        
            code = extract_python_code(response)[0]
        except:
            continue
        code = remove_print(code)
        if code.strip() == "":
            print(response)
            print("*"*10)
            print(extract_python_code(response)[0])
            exit()
        inputs = generate_input_num(5, code)
        if inputs is None:
            continue
        if double_check:
            inputs2 = generate_input_num(5, code)
            if inputs2 != inputs:
                print("Input double check failed")
                continue
        logger.info(code)
        outputs = generate_output_by_code(inputs, code)
        if outputs is None:
            continue
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
            json_record[cnt] = {'task': cnt, 'transformation_rule': transformation_rule, 'hint': hint, "object_description": object_description,'generator': code, 'results': outputs, 'response': response}
            html_description[cnt] = f"Transformation rule:\n{transformation_rule}\n\nObject description:\n{object_description}\n\nhint:\n{hint}\n"
            cnt += 1
            return True
        except Exception as e:
            print(e)
    return False

def main(generator_number = 1):
    double_check = True
    parser = argparse.ArgumentParser()
    add_llm_args(parser)
    args = parser.parse_args()
    llm = get_llm(args)
    logger = get_logger('input_hypo', args)
    # 123 42
    json_record = []
    html_description = []
    for i in range(generator_number):
        json_record.append({})
        html_description.append({})

    rng = random.Random(42)
    # random.seed(42)
    concept_library = load_library("1")
    transform_library = concept_library['transformation_library']
    object_library = concept_library['object_library']
    grid_library = concept_library['grid_library']
    
    cnt = 0

    # cur_description = get_dpp(transform_library, 123, 120)
    # object_library = get_dpp(object_library, 123, 120)
    # cur_description2 = get_dpp(transform_library, 123, 150)
    round_num = 0
    while(cnt < 200):
        print('Cur round', cnt)
        transformation_hint  = rng.sample(transform_library, 2)
        object_hint = rng.sample(object_library, 1)
        # grid_hint = rng.sample(grid_library, 1)
        transformation_hint_str = ""
        for i, hints in enumerate(transformation_hint):
            transformation_hint_str += f"{i + 1}. " + hints + '\n'
        # transformation_hint = "1. " + cur_description[round_num] + '\n' + "2. " + cur_description2[round_num]
        # transformation_hint = cur_description[round_num]
        # transformation_hint = cur_description[round_num]
        round_num += 1
        hint = f"""
Transformation key concept: \n{transformation_hint_str}
Object key concept : {object_hint[0]}
"""     
        print(hint)
        # exit(0)
        flag = False
        for i in range(generator_number):
            cur_result = generate_input_output(logger=logger, hint=hint, llm=llm, double_check=double_check, cnt=cnt, generator_number=i+1, json_record=json_record[i], html_description=html_description[i])
            if not flag and cur_result:
                flag = True
        if flag:
            cnt += 1
    
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
        html_content = get_html_vis_double(html_description, json_record, cnt)
        f.write(html_content)
        # print(response)

main(2)