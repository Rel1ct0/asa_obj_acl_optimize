from ipaddress import IPv4Address, IPv4Network, collapse_addresses


def og_parse(line: str):
    if line.startswith(' group-object'):
        return list(IPv4Network(line.split()[-1]))
    if line.startswith(' network-object'):
        answer = list()
        answer.append(IPv4Network(line.split()[1] + '/' + line.split()[2]))
        return answer
    if line.startswith(' range'):
        candidate_addresses = list()
        for address in range(int(IPv4Address(line.split()[1])), int(IPv4Address(line.split()[2])) + 1):
            candidate_addresses.append(IPv4Network(address))
        return list(collapse_addresses(candidate_addresses))
    return None


def find_duplicate_ogroups(objects: dict):
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