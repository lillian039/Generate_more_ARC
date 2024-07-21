from src.load_dataset.load_arc_subset import load_arc_subset, transform_input_list, extract_python_code, generate_output_by_code, task_filter
import argparse
from src.utils.llm.main import get_llm, add_llm_args
from src.utils.logger import get_logger
from src.build_library.prompt.concept_library_prompt import system_prompt_abc, get_prompt_for_hypotheses2
from src.build_library.prompt.transform_concept_library import get_transformation_library
from src.utils.format.color_format import transform_color_into_number, transform_number_into_color
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
    random.seed(2)
    data = load_arc_subset()
    transformation_library = get_transformation_library()
    json_record = []
    for task in data:
        logger.info(task['name'])
        train_example = task['data']['train']
        test_example = task['data']['test']
        input_images = []
        for example in train_example:
            input_images.append(transform_number_into_color(example['input']))
        input_images.append(transform_number_into_color(test_example[0]['input']))
        transformed_list = transform_input_list(input_images)
        transformation_hint  = random.sample(transformation_library, 2)
        print(transformed_list)
        
        # original_hypo = task['human_description']
        # prompt_for_hypotheses = get_prompt_for_hypotheses1(transformed_list, original_hypo)
        prompt_for_hypotheses = get_prompt_for_hypotheses2("", transformation_hint)
        prompt = [
            {"role": "system", "content": system_prompt_abc},
            {"role": "user", "content": prompt_for_hypotheses}
        ]

        response = llm(prompt).choices[0].message.content

        codes = extract_python_code(response)
        for i, code in enumerate(codes):
            outputs = generate_output_by_code(input_images, code)
            for i in range(len(outputs)):
                outputs[i]['input'] = transform_color_into_number(outputs[i]['input'])
                outputs[i]['output'] = transform_color_into_number(outputs[i]['output'])
            # print(outputs)
            if not task_filter(outputs):
                continue
            try:
                visualize_data(outputs, task['name'], i)
            except Exception as e:
                print(e)
                continue
            json_record.append({'task': task['name'], 'num': i, 'hypothesis': code, 'results': outputs})
        logger.info(response)

    with open('result/hypotheses1.json','w') as f:
        json.dump(json_record, f, indent=4)
        # exit()

    
main()