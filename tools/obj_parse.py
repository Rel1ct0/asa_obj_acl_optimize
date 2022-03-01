from ipaddress import IPv4Address, IPv4Network, collapse_addresses


def obj_parse(line: str):
    answer = list()
    if line.startswith(' nat'):
        return None
    if line.startswith(' host'):
        answer.append(IPv4Network(line.split()[-1]))
        return answer
    if line.startswith(' subnet'):
        answer.append(IPv4Network(line.split()[1] + '/' + line.split()[2]))
        return answer
    if line.startswith(' range'):
        answer = list()
        for address in range(int(IPv4Address(line.split()[1])), int(IPv4Address(line.split()[2])) + 1):
            answer.append(IPv4Network(address))
        return list(collapse_addresses(answer))
    return None


def find_duplicate_objects(objects: dict):
    print('*' * 10, 'looking for duplicate objects', '*' * 10)
    mentioned_objects = set()
    duplicate_objects = dict()
    keys = list(objects.keys())
    for i in range(0, len(keys)-1):
        for j in range(i+1, len(keys)):
            if keys[j] in mentioned_objects:
                continue
            if objects[keys[i]] == objects[keys[j]]:
                if not duplicate_objects.get(keys[i]):
                    duplicate_objects[keys[i]] = list()
                duplicate_objects[keys[i]].append(keys[j])
                mentioned_objects.add(keys[j])
    if duplicate_objects:
        for dupl in duplicate_objects.keys():
            print(f"object {dupl} has duplicates: {', '.join(duplicate_objects[dupl])}")
    print('*' * 10, 'done looking for duplicate objects', '*' * 10)


def print_empty_objects(obj_list: dict):
    empty_objects = str()
    for next_object in obj_list.keys():
        if len(obj_list[next_object]) == 0:
            empty_objects = empty_objects + f"\t\t {next_object}\n"
    if empty_objects:
        empty_objects = 'Empty objects found:\n' + empty_objects
        print(empty_objects)
