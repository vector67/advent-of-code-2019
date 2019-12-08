tree = {}
top_level_names = []
token_dict = {}
for line in open('Day 6/data.txt'):
    tokens = line.split(')')
    if tokens[0] not in token_dict:
        token_dict[tokens[0]] = {}
        tree[tokens[0]] = token_dict[tokens[0]]
        top_level_names.append(tokens[0])
    tokens[1] = tokens[1].strip()
    if tokens[1] not in token_dict:
        token_dict[tokens[1]] = {}
    if tokens[1] in top_level_names:
        top_level_names.remove(tokens[1])
    parent_object = token_dict[tokens[0]]
    parent_object[tokens[1]] = token_dict[tokens[1]]
def recursive_amount_orbits(node):
    num_orbits = 0
    num_sub_nodes = 1
    for i in node:
        num_orbits_sub, num_sub_nodes_sub = recursive_amount_orbits(node[i])
        num_orbits += num_orbits_sub + num_sub_nodes_sub
        num_sub_nodes += num_sub_nodes_sub
    return num_orbits, num_sub_nodes
sum_orbits = 0
for i in top_level_names:
    sum_orbits += recursive_amount_orbits(tree[i])[0]
print(sum_orbits)
# print(leaves)