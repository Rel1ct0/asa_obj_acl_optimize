from ipaddress import IPv4Address, IPv4Network, collapse_addresses


def obj_parse(line: str):
    if line.startswith(' nat'):
        return None
    if line.startswith(' host'):
        return list(IPv4Network(line.split()[-1]))
    if line.startswith(' subnet'):
        answer = list()
        answer.append(IPv4Network(line.split()[1] + '/' + line.split()[2]))
        return answer
    if line.startswith(' range'):
        candidate_addresses = list()
        for address in range(int(IPv4Address(line.split()[1])), int(IPv4Address(line.split()[2])) + 1):
            candidate_addresses.append(IPv4Network(address))
        return list(collapse_addresses(candidate_addresses))
    return None
