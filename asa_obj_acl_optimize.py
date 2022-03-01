from sys import argv
from ipaddress import IPv4Address, IPv4Network, collapse_addresses
from tools import obj_parse


def print_empty_objects(obj_list: dict):
    empty_objects = str()
    for next_object in obj_list.keys():
        if len(obj_list[next_object]) == 0:
            empty_objects = empty_objects + f"\t\t {next_object}\n"
    if empty_objects:
       empty_objects = 'Empty objects found:\n' + empty_objects
       print(empty_objects)


if len(argv) != 2:
    print('Usage: asa_acl_optimizer <config.txt>')
    exit(1)

with open(argv[1]) as infile:
    config = infile.readlines()

print(f"Configuration file loaded, has {len(config)} lines")

objects = dict()    # Every value is a list of IPv4Networks (one element for host/subnet, more for range)
obj_groups = dict()
acls = dict()
used_objects = set()
used_obj_groups = set()

now_processing = ''
current_object = ''

for line in config:
    if line.startswith(' description'):
        continue
    if now_processing == 'object':
        if not objects.get(current_object):
            objects[current_object] = list()
        if object_parsed := obj_parse.obj_parse(line):
            objects[current_object].extend(object_parsed)
            now_processing = ''
            current_object = ''
        continue
    if now_processing == 'obj_group':
        pass
    if line.startswith('object network'):
        now_processing = 'object'
        current_object = line.split()[-1]
        continue
    if line.startswith('object-group network'):
        now_processing = 'obj_group'
        current_object = line.split()[-1]
        continue
    if line.startswith('access-list'):
        now_processing == 'acl'
        current_object = line.split()[1]
        continue

print_empty_objects(objects)

for z in objects.keys():
    print(f'{z}: {objects[z]}')
