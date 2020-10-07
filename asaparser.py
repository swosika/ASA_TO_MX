import ciscoconfparse as cp
import netaddr as nt

def create_conf_obj(filename,mode="ios"):
	parse = cp.CiscoConfParse(filename, syntax=mode)
	return parse
def get_object_groups(parser):
	groups_list = []
	for object_group in parser.find_objects('^object-group network'):
		grouptext = object_group.text.split(" ")
		object_name = grouptext[2]
		objects_list = []
		for network_obj in object_group.re_search_children(r'^ network-object'):
			obj_text = network_obj.text.strip().split(" ")
			if(obj_text[1] == "host"):
				objects_list.append(nt.IPNetwork(obj_text[2]))
			else:
				ipaddr = nt.IPNetwork(obj_text[1])
				ipaddr.netmask = obj_text[2]
				objects_list.append(ipaddr)
		groups_list.append((object_name, objects_list))
	return groups_list		
def gather_data(filename):
	obj = create_conf_obj(filename)
	groups_list = get_object_groups(obj)
	return groups_list
def read_lines(filename):
	lines = []
	f = open(filename, "r")
	for line in f.readlines():
		lines.append(line.strip())
	return lines

def read_network_objects(lines):
	in_object_group = False
	objects = []
	subnet_objects = []
	for line in lines:
		if("subnet" in line):
			subnet_objects.append(line)
		if("network-object" in line):
			objects.append(line)
	return objects, subnet_objects

def read_object_groups(lines):
	all_objects = []
	objects = []
	last_object = None
	in_object_group = False
	for line in lines:
		if("object-group" in line):
			if(in_object_group):
				all_objects.append({"object-group":last_object, "objects":objects})
			in_object_group = True
			objects = []
			last_object = line
			continue
		elif(("network-object" in line) or ("port-object" in line)):
			objects.append(line)
		else:
			in_object_group = False
	return all_objects