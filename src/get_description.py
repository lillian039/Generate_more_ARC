import os
import json

def get_description_by_step(llm, logger):
    path = 'data/code_and_requirement_complete/'
    file_list = sorted(os.listdir(path))
    tasks = []
    for file in file_list:
        with open(os.path.join(path, file), 'r') as f:
            task = json.load(f)
        tasks.append(task)

    step_description = []
    task_names = []
    print(len(tasks))
    for i in range(len(tasks)):
        task = tasks[i]
        # print(task['name'])

        task_names.append(task['name'])
        description = task['description']['object'] + task['description']['size'] + task['description']['description']
        system = "You are an expert player in visual puzzle games. You are asked to generate clear transformation hypothese based on the given information."
        user = f"Given the following information, generate a clear transformation hypothese:\n\n{description}\n\nThe rule should be in the following format:\n\nRule: \nstep 1: [Your rule for step 1]\nstep 2: [Your rule for step 2]\n...\n\nTry to make your description as clear and concise as possible, no more than three steps."
        prompt = [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
        response = llm(prompt)
        response_content = response.choices[0].message.content
        response_content = response_content.replace('Rule:','').strip()
        task['description_step'] = response_content
        # logger.info(response_content)
        step_description.append(response_content)
    return step_description, tasks

def get_description_directly():
    path = 'data/code_and_requirement_complete/'
    file_list = sorted(os.listdir(path))
    tasks = []
    description_list = []
    tasks = []
    for file in file_list:
        with open(os.path.join(path, file), 'r') as f:
            task = json.load(f)
        tasks.append(task)
    for i in range(len(tasks)):
        task = tasks[i]
        # print(task['name'])
        description = task['description']['object'] +'\n'+ task['description']['size'] +'\n'+ task['description']['description']
        description = description.replace('...',' ')
        # print(description)
        # exit(0)
        task['description_direct'] = description
        description_list.append(description)
        
    return description_list, tasks
