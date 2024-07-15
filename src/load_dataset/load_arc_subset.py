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
        for row in input_example:
            represent_str += str(row) + '\n'
        represent_str += '\n'
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
    outputs = []
    for input_example in input_list:
        code = original_code + f"\nprint(transform_grid(np.array({input_example})))\n"
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
            print(output)
    return outputs
        
        
def task_filter(data):
    flag = False
    for i, output in enumerate(data):
        if output['output'] == output['input'] or len(output['output']) == 0 or len(output['input']) == 0:
            return False
        for list in output['output']:
            for number in list:
                if (not isinstance(number, int)) or number < 0 or number > 9:
                    return False
        if i != 0 and output['output'] != data[i-1]['output']:
            flag = True
    return flag
    
    
    
    