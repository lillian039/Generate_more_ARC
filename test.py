from src.utils.get_k_sim import KSIM
import json

with open(f'result/library/1_concept_pair_2024-07-24_00-13-19.json', 'r') as f:
    data = json.load(f)

# print(data)
data = data['concept_pair_list']

object_concept = []
transformation_concept = []
for item in data:
    object_concept.append(item['object'][0])
    transformation_concept.append(item['transformation'])

ksim = KSIM(object_concept)

cur_index = 1
# index = ksim.get_k_sim(object_concept[cur_index], 5)
index = ksim.get_lager_sim(object_concept[cur_index], 0.25)
print(object_concept[cur_index])
print(index)
transformation = ksim.get_content_from_index(index, transformation_concept)
objects = ksim.get_object_from_index(index)
print(objects)
print(transformation)