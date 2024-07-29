import json
import re
import hashlib
import sys
import os
import signal
timeout = 10

def handler(signum, frame):
    raise TimeoutError("Execution time exceeded")

signal.signal(signal.SIGALRM, handler)

def load_arc_subset():
    with open('data/arc_subset.json') as f:
        data = json.load(f)
    return data


def transform_input_list(input_list):
    represent_str = ""
    for input_example in input_list:
        for i, row in enumerate(input_example):
            if i == 0:
                represent_str += '[' + str(row) + ',\n'
            elif i != len(input_example) - 1:
                represent_str += str(row) + ',\n'
            else:
                represent_str += str(row) + ']\n'
        represent_str += '\n'
    return represent_str
    # print(represent_str)

def extract_python_code(content_response):
    pattern = r"```python\n(.*?)\n```"
    code_list = re.findall(pattern, content_response, re.S)
    # print(code_list)
    return code_list

def transform_format_to_list(matrix):
    transform_success = True
    list_matrix = []
    try:
        # numpy format
        list_matrix = matrix.replace('\n','')
        list_matrix = list_matrix.replace(' ',',')
        list_matrix = eval(list_matrix)
    except Exception as e:
        try:
            # list format
            list_matrix = eval(matrix)
        except Exception as e:
            # other wrong format
            transform_success = False
    return list_matrix, transform_success

def generate_output_by_code(input_list, code):
    original_code = code
    if original_code.strip() == "":
        exit(0)
    outputs = []
    for input_example in input_list:
        # print(input_example)
        code = original_code + f"\nprint(transform_grid(np.array({input_example})))\n"
        # print(code)
        code_id = hashlib.md5(str(code).encode('utf-8')).hexdigest()
        try:
            with open(f'result/{code_id}_output.txt', 'w') as file:
                sys.stdout = file
                global timeout
                signal.alarm(timeout)
                exec(code, globals())
                sys.stdout = sys.__stdout__
                signal.alarm(0)
            with open(f'result/{code_id}_output.txt', 'r') as file:
                output = file.read()[:-1]
            os.remove(f'result/{code_id}_output.txt')
            output_list_format, succeed = transform_format_to_list(output)
            outputs.append({'input': input_example, 'output': output_list_format})
        except Exception as e:
            sys.stdout = sys.__stdout__
            os.remove(f'result/{code_id}_output.txt')
            output = f"Runtime Error: {e}"
            # print(code)
            # print(output)
    return outputs

def generate_input_num(input_number, code):
    original_code = code
    intputs = []
    for i in range(input_number):
        code = original_code
        if "from random import" in code:
            code = "import random\n" + code
        if "import random" in code:
            code += f"\nrandom.seed({i})\n"
        if "import numpy as np" in code:
            code += f"\nnp.random.seed({i})\n"
        if "rng = default_rng()" in code:
            code = code.replace("rng = default_rng()", f"rng = default_rng({i})")
        # print(code)
        code_id = hashlib.md5(str(code).encode('utf-8')).hexdigest()
        code += "print(generate_input())\n"
        try:
            with open(f'result/{code_id}_output.txt', 'w') as file:
                sys.stdout = file
                global timeout
                signal.alarm(timeout)
                exec(code, globals())
                sys.stdout = sys.__stdout__
                signal.alarm(0)
            with open(f'result/{code_id}_output.txt', 'r') as file:
                output = file.read()[:-1]
            os.remove(f'result/{code_id}_output.txt')
            output_list_format, succeed = transform_format_to_list(output)
            intputs.append(output_list_format)
        except Exception as e:
            sys.stdout = sys.__stdout__
            os.remove(f'result/{code_id}_output.txt')
            output = f"Runtime Error: {e}"
            print(output)
    return intputs
        
        
def task_filter(data):
    flag = False
    input_all_black = True
    output_all_black = True
    for i, output in enumerate(data):
        if output['output'] == output['input'] or len(output['output']) == 0 or len(output['input']) == 0:
            print("Same / Empty")
            return False
        for list in output['output']:
            for number in list:
                if (not isinstance(number, int)) or number < 0 or number > 9:
                    return False
        if i != 0 and output['output'] != data[i-1]['output']:
            flag = True
        for column in output['input']:
            for number in column:
                if number != 0:
                    input_all_black = False
                    break
        for column in output['output']:
            for number in column:
                if number != 0:
                    output_all_black = False
                    break
    if input_all_black or output_all_black:
        return False
    return flag

def load_library(batch_size):
    with open(f'result/cur_library/{batch_size}.json') as f:
        data = json.load(f)
    return data
    
def remove_print(code_str):
    code_str = code_str.replace('print(', '# print(')
    code_str = code_str.replace('np.random.seed()', '# np.random.seed()')
    code_str = code_str.replace('np.random.seed(', '# np.random.seed(')
    last_return_index = code_str.rfind("return")
    next_newline_index = code_str.find("\n", last_return_index + len("return"))
    if next_newline_index == -1:
        return code_str
    code_str = code_str[: next_newline_index + 1] + '\n'
    return code_str
    
def get_transformation_rule(content):
    rule_index = content.find('Transformation rule:')
    rule_length = content[rule_index + len('Transformation rule:'):].find('\n') + 1
    transformation_rule = content[rule_index + len('Transformation rule:'): rule_index + len('Transformation rule:') + rule_length]
    object_index = content.find('Object description:')
    object_length = content[object_index + len('Object description:'):].find('\n') + 1
    object_description = content[object_index + len('Object description:'): object_index + len('Object description:') + object_length]
    transformation_rule = transformation_rule.strip()
    object_description = object_description.strip()

    return transformation_rule, object_description
    