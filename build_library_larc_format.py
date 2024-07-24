import os
import json
from src.utils.llm.main import get_llm, add_llm_args
from src.utils.logger import get_logger
import argparse
from src.build_library.prompt.concept_library_prompt import get_library_example_prompt
from datetime import datetime
import re
def seperate_batch(files, batch_size):
    batchs = []
    for i in range(0, len(files), batch_size):
        batchs.append(files[i:i+batch_size])
    return batchs

def split_sentences(text):
    sentences = re.split(r'\d+\.\s*', text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    sentences = [sentence for sentence in sentences if sentence != '**']
    return sentences


def load_confident_larc(llm, logger, batch_size=1):
    path = 'data/LARC/larc_confident/'
    files = os.listdir(path)
    files = sorted(files)
    batchs = seperate_batch(files, batch_size)
    object_library = []
    grid_library = []
    transformation_library = []
    concept_pair_list = []
    for files in batchs:
        print(files)
        str_task_description = "The following descriptions below each task describe the same task's transformation by different people.\n\n"
        for cnt, file in enumerate(files):
            cur_path = path + file
            with open(cur_path, 'r') as f:
                task = json.load(f)
            if len(files) > 1:
                str_task_description += 'Task ' + str(cnt + 1) + '\n' + '```\n'
            task_description = task['descriptions']
            example1, answer1 = get_library_example_prompt(batch_size)
            for i, description in enumerate(task_description):
                str_task_description += 'Description ' + str(i + 1) + '\n'
                str_task_description += description['see_description'] + '\n' + description['grid_description'] + '\n' + description['do_description'] + '\n\n'
                str_task_description = str_task_description.replace('...', ': ').replace('  ',' ')
            str_task_description += '```\n\n'
        system = """You are an expert player in visual puzzle games. You are asked to extract crucial concept from given hypothese.
Please extract the crucial concept from the above descriptions in the following format:\n\n
Definition about the objects:\n
1. [definition 1]\n
...
Grid size:\n
1. [grid size 1]\n
Crucial concepts about the transformation:\n
1. [concept 1]\n
...
Make concepts as refined as possible, no more than one sentence. Each concept should be unique to each other.
"""             
        concept_pair = {}
        
        # logger.info(str_task_description)
        prompt = [
                {"role": "system", "content": system},
                {"role": "user", "content": example1},
                {"role": "assistant", "content": answer1},
                {"role": "user", "content": str_task_description}
        ]
        # logger.info(system)
        # logger.info(example1)
        # logger.info(answer1)
        # logger.info(str_task_description)
        # exit()
        for i in range(3):
            response = llm(prompt).choices[0].message.content
            # print(response)
            # print("!!!")
            object_idx = response.find('Definition about the objects:')
            grid_idx = response.find('Grid size:')
            concept_idx = response.find('Crucial concepts about the transformation:')
            if object_idx == -1 or grid_idx == -1 or concept_idx == -1:
                logger.info('Failed to extract concept')
            else:
                object_definitions = response[object_idx + len('Definition about the objects:'):grid_idx]
                object_definitions = object_definitions.strip()
                grid_sizes = response[grid_idx + len('Grid size:'): concept_idx]
                grid_sizes = grid_sizes.strip()
                concepts = response[concept_idx + len('Crucial concepts about the transformation:'):]
                concepts = concepts.strip()

                object_definitions = split_sentences(object_definitions)
                grid_sizes = split_sentences(grid_sizes)
                concepts = split_sentences(concepts)

                object_library += object_definitions
                grid_library += grid_sizes
                transformation_library += concepts

                concept_pair['object'] = object_definitions
                concept_pair['grid'] = grid_sizes
                concept_pair['transformation'] = concepts

                concept_pair_list.append(concept_pair)
                logger.info(response)
                break
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f'result/library/{batch_size}_format_{current_time}.json','w') as f:
        json.dump({'object_library':object_library, 'grid_library':grid_library, 'transformation_library':transformation_library}, f, indent=4)
    with open(f'result/library/{batch_size}_concept_pair_{current_time}.json','w') as f:
        json.dump({'concept_pair_list':concept_pair_list}, f, indent=4)
    
def main():
    parser = argparse.ArgumentParser()
    add_llm_args(parser)
    parser.add_argument('--batch_size', type=int, default=1)
    args = parser.parse_args()
    llm = get_llm(args)
    logger = get_logger(f'extract_concept_{args.batch_size}', args)
    load_confident_larc(llm, logger, args.batch_size)

main()