from ipaddress import IPv4Address, IPv4Network, collapse_addresses


def og_parse(line, objects_list, ogroups_list) -> list:
    if line.startswith(' group-object'):
        return ogroups_list[line.split()[-1]]
    if line.startswith(' network-object'):
        if line.split()[1] == 'host':
            answer = list()
            answer.append(IPv4Network(line.split()[-1]))
            return answer
        if line.split()[1] == 'object':
            return objects_list[line.split()[-1]]
        answer = list()
        answer.append(IPv4Network(line.split()[1] + '/' + line.split()[2]))
        return answer
    return None


def find_duplicate_ogroups(ogroups_list: dict):
    print('*'*10, 'looking for duplicate object groups', '*'*10)
    mentioned_objects = set()
    duplicate_objects = dict()
    keys = list(ogroups_list.keys())
    for i in range(0, len(keys)-1):
        for j in range(i+1, len(keys)):
            if keys[j] in mentioned_objects:
                continue
            if ogroups_list[keys[i]] == ogroups_list[keys[j]]:
                if not duplicate_objects.get(keys[i]):
                    duplicate_objects[keys[i]] = list()
                duplicate_objects[keys[i]].append(keys[j])
                mentioned_objects.add(keys[j])
    if duplicate_objects:
        for dupl in duplicate_objects.keys():
            print(f"object-group {dupl} has duplicates: {', '.join(duplicate_objects[dupl])}")
    print('*' * 10, 'done looking for duplicate object groups', '*' * 10)
