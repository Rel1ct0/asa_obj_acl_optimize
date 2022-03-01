from sys import argv
from ipaddress import IPv4Address, IPv4Network, collapse_addresses
from tools import obj_parse, og_parse


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
        if not objects.get(current_object):   # New object to add
            objects[current_object] = list()
        if object_parsed := obj_parse.obj_parse(line):       # Object content successfully parsed
            objects[current_object].extend(object_parsed)    # Add content to objects dict
        now_processing = ''                              # And reset processing
        current_object = ''
        continue
    if now_processing == 'obj_group':
        if not obj_groups.get(current_object):  # New object group to add
            obj_groups[current_object] = list()
        if og_parsed := og_parse.og_parse(line, objects, obj_groups):  # Object group content successfully parsed
            obj_groups[current_object].extend(og_parsed)  # Add content to object groups dict
            continue
        else:
            now_processing = ''  # Not an object group config line, continue processing
            current_object = ''
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


for ogroup in obj_groups.keys():
    obj_groups[ogroup] = sorted(obj_groups[ogroup])

#obj_parse.print_empty_objects(objects)
#obj_parse.find_duplicate_objects(objects)
#og_parse.print_empty_ogroups(obj_groups)
#og_parse.find_duplicate_ogroups(obj_groups)
og_parse.find_redundant_lines_in_ogroup(obj_groups)
