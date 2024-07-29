import json
from src.build_library.prompt.self_instruct import system, get_content, get_content_pair, system_similar, get_content_similar
import random
from src.utils.llm.main import get_llm, add_llm_args
import argparse
from src.utils.get_k_sim import KSIM
from src.utils.logger import get_logger
from rouge_score import rouge_scorer

def filter_similar(new_inst, all_instructions):
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False)
    # scorer = rouge_scorer.RougeScorer(["rouge2"], use_stemmer=False)
    rouge_scores = []
    for exist_inst in all_instructions:
        score = scorer.score(new_inst, exist_inst)["rougeL"].fmeasure
        rouge_scores.append(score)
    print(max(rouge_scores))
    if max(rouge_scores) > 0.60:
        # print(new_inst)
        max_index = rouge_scores.index(max(rouge_scores))
        # print(all_instructions[max_index])
        # print("!!!")
        # exit()
        return False
    return True
def load_previous_pair_library():
    with open(f'result/library/1_concept_pair_remove_2024-07-24_18-23-54.json', 'r') as f:
        data = json.load(f)
    data = data['concept_pair_list']
    return data

def load_previous_library():
    with open('result/library/3_format_remove_2024-07-24_18-24-03.json', 'r') as f:
        data = json.load(f)
    return data

def seperate_result(content, start, end):
    result = []
    for i in range(start + 1, end):
        start_index = content.find(f'Concept {i}:')
        end_index = content.find(f'Concept {i+1}:')
        # print(start_index, end_index)
        result.append(content[start_index + len(f'Concept {i}:') : end_index].strip())
    result.append(content[end_index + len(f'Concept {end}:'):].strip())
    final_reuslt = []
    for res in result:
        res = res.replace('Object:', '').replace('Transformation:', '').strip()
        final_reuslt.append(res)
    return final_reuslt

def seperate_result_pair(content, start, end):
    result = []
    for i in range(start + 1, end):
        start_index = content.find(f"Concept {i}:\n")
        end_index = content.find(f"Concept {i+1}:\n")
        result.append(content[start_index + len(f"Concept {i}:\n") : end_index].strip())
    result.append(content[end_index + len(f"Concept {end}:\n"):].strip())
    return result

def self_instruct(llm, example_k, example_new, generate_k, logger):
    random.seed(42)
    original_data = load_previous_library()
    original_data = original_data['transformation_library']
    cur_data = []
    ksim = KSIM(original_data)
    while(len(cur_data) < 400):
        if len(cur_data) < 100:
            # print("?")
            data = random.sample(original_data, 1)
            sim_data = ksim.get_k_sim(data[0], example_k - 1)
            sim_data = ksim.get_object_from_index(sim_data)
            data += sim_data
        else:
            data = random.sample(original_data, example_k - example_new)
            data += random.sample(cur_data, example_new)
        # print(get_content(data, generate_k))
        prompt = [
            {"role": "system", "content": system_similar},
            {"role": "user", "content": get_content_similar(data, generate_k)}
        ]

        response = llm(prompt).choices[0].message.content
        logger.info(f"Example:\n{get_content_similar(data, generate_k)}")
        logger.info(f"Response:\n{response}")
        # print(response)
        cur_result = seperate_result(response, example_k, example_k + generate_k)
        for cur_inst in cur_result:
            # if filter_similar(cur_inst, cur_data + original_data):
            cur_data.append(cur_inst)
    return cur_data

def self_instruct_pair(llm, example_k, example_new, generate_k, logger):
    random.seed(42)
    original_data = load_previous_pair_library()
    cur_data = []
    while(len(cur_data) < 40):
        data = random.sample(original_data, example_k)
        prompt = [
            {"role": "system", "content": system},
            {"role": "user", "content": get_content_pair(data, generate_k)}
        ]
        print(get_content_pair(data, generate_k))
        response = llm(prompt).choices[0].message.content
        print(response)
        # cur_data.append(response)
        cur_result = seperate_result(response, example_k, example_k + generate_k)
        for cur_inst in cur_result:
            cur_data.append(cur_inst)
    return cur_data


def main():
    parser = argparse.ArgumentParser()
    add_llm_args(parser)
    args = parser.parse_args()
    logger = get_logger('self_instruct', args)
    llm = get_llm(args)
    new_generate = self_instruct(llm, 4, 0, 4, logger)
    with open('result/enlarged_library/self_instruct_4t_similar.json', 'w') as f:
        new_generate = {'transformation_library': new_generate, 'object_library': [], 'grid_library': []}
        json.dump(new_generate, f, indent=4)
    with open('result/enlarged_library/merge.json', 'w') as f:
        new_generate = {'transformation_library': new_generate['transformation_library'] + load_previous_library()['transformation_library'], 'object_library': [], 'grid_library': []}
        json.dump(new_generate, f, indent=4)
main()