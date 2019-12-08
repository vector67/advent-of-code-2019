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
def find_most_recent_common_ancestor(node, obj1, obj2):
    found_obj1 = False
    found_obj2 = False
    dist_to_obj1 = 0
    dist_to_obj2 = 0
    for i in node:
        if i == obj1:
            found_obj1 = True
            print('found obj1', i)
        elif i == obj2:
            found_obj2 = True
            print('found obj2', i)
        else:
            print('searching deeper', i)
            dist_to_obj1_add, dist_to_obj2_add = find_most_recent_common_ancestor(node[i], obj1, obj2)
            dist_to_obj1 += dist_to_obj1_add
            dist_to_obj2 += dist_to_obj2_add
    if found_obj1:
        dist_to_obj1 = 1
    if found_obj2:
        dist_to_obj2 = 1
    if dist_to_obj1 > 0 and dist_to_obj2 > 0:
        return dist_to_obj1, dist_to_obj2
    elif dist_to_obj1 > 0:
        if found_obj1:
            dist_to_obj1 = 0
        return dist_to_obj1 + 1, dist_to_obj2
    elif dist_to_obj2 > 0:
        if found_obj2:
            dist_to_obj2 = 0
        return dist_to_obj1, dist_to_obj2 + 1
    return 0, 0

for i in top_level_names:
    dist_to_obj1, dist_to_obj2 = find_most_recent_common_ancestor(tree[i], 'YOU', 'SAN')
    if not(dist_to_obj1 == 0):
        print(dist_to_obj1, dist_to_obj2)
        print(dist_to_obj1 + dist_to_obj2)

# find_most_recent_common_ancestor(tree, top_level_names, 'YOU', 'SAN')
# print(sum_orbits)
# print(leaves)