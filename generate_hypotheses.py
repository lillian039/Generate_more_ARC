from src.build_library.prompt.concept_library_prompt import system_prompt, content_prompt, get_content_prompt
from src.utils.llm.main import get_llm, add_llm_args
import argparse
from src.utils.logger import get_logger
from src.get_description import get_description_by_step, get_description_directly
import random
import re
import json

def split_tasks(input_text):
    # 使用正则表达式匹配任务分隔符
    pattern = r"(Task \d+:.*?)(?=Task \d+:|$)"
    tasks = re.findall(pattern, input_text, re.S)
    for i in range(len(tasks)):
        tasks[i] = tasks[i].replace(f'Task {i+1}:', '').strip()
    return tasks

def main(batch_size = 4, generate_number = 4):
    parser = argparse.ArgumentParser()
    add_llm_args(parser)
    args = parser.parse_args()
    llm = get_llm(args)
    logger = get_logger('concept_library', args)
    random.seed(123)
    # hypothese_library, tasks = get_description_by_step(llm, logger)
    hypothese_library, tasks = get_description_directly()

    new_hypotheses_list = []
    cnt = 0
    while(len(hypothese_library) < 1000):
        sub_list_example = random.sample(hypothese_library, batch_size)        
        prompt = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_content_prompt(sub_list_example, generate_number)}
        ]
        response = llm(prompt).choices[0].message.content
        # logger.info(response)
        new_hypotheses = split_tasks(response)

        for new_inst in new_hypotheses:
            if new_inst == "":
                continue
            # filter out too short or too long instructions
            if len(new_inst.split()) <= 3 or len(new_inst.split()) > 100:
                continue
            hypothese_library.append(new_inst)
            cnt += 1
            new_hypotheses_list.append({cnt: new_inst})
            logger.info(new_inst)
            # exit(0)
    with open('result/hypotheses_direct.json','w') as f:
        json.dump(new_hypotheses_list, f, indent=4)
    

main() 