## import necessary libraries 
import requests
import json

## define necessary parameters as global variables 
ORG_ID = input("Enter your organization id: ")
API_KEY = input("Enter your API key: ")
BASE_URL = "https://api.meraki.com/api/v0/organizations/" + ORG_ID + "/networkObjects"
headers={"content-type":"application/json", "X-Cisco-Meraki-API-Key": API_KEY}

## define function for creating object group from parsed text file
def add_network_object_group(name):
	BASE = "https://api.meraki.com/api/v0"
	URL = BASE + "/organizations/" + ORG_ID + "/networkObjectGroups"
	payload = {"name":name,"networkObjectIds":[]}
	r=requests.post(URL, params=payload,headers=headers)
	dic = json.loads(r.text)
	if("id" in dic):
		return int(dic["id"])
	return None

## define function for creating objects to go inside group 
def add_network_object(name,ip,groupid):
	payload = {"name":name,"type":"ipv4Cidr","value":ip,"networkObjectGroupIds":[groupid]}
	r=requests.post(BASE_URL, json=payload,headers=headers)
	return r.text

## create network object groups
def create_network_groups(object_groups):
	for group in object_groups:
		name = group[0]
		print("====CREATED GROUP " + name + " ======")
		groupid = add_network_object_group(name)
		print("- group created with id " + str(groupid))
		count = 0
		for network_object in group[1]:
			print("----creating network object----")
			obj_name = name +"_"+str(count)
			print(obj_name)
			print(str(network_object))
			result = add_network_object(obj_name,str(network_object),groupid)
			count+=1
			print(result)

#### functions needed to clear objects previously created (for testing environment only) ####
## acquire network objects from organization using BASE_URL
def get_all_network_objects():
    	r=requests.get(BASE_URL,headers=headers)
	return r.text

## acquire network object groups from organization using BASE_URL and "/networkObjectGroups"
def get_all_network_groups():
	BASE = "https://api.meraki.com/api/v0"
	URL = BASE + "/organizations/" + ORG_ID + "/networkObjectGroups"
	r=requests.get(URL,headers=headers)
	return r.text

## define how to delete an object
def delete_object(obj_id):
	BASE = "https://api.meraki.com/api/v0"
	URL = BASE + "/organizations/" + ORG_ID + "/networkObjects/" + str(obj_id)
	print(URL)
	r=requests.delete(URL, headers=headers)
	print(r)
	return r.text

## iterate through network objects, delete one at a time 
def delete_all_network_objects():
	network_objects = json.loads(get_all_network_objects())
	for netobj in network_objects:
		print("Deleting object " + str(netobj["id"]))
		print(delete_object(netobj["id"]))

## define how to delete a group
def delete_group(group_id):
	BASE = "https://api.meraki.com/api/v0"
	URL = BASE + "/organizations/" + ORG_ID + "/networkObjectGroups/" + str(group_id)
	print(URL)
	r=requests.delete(URL,headers=headers)
	print(r)
	return r.text

## iteratate through object groups, delete one at a time 
def delete_all_network_groups():
	network_objects = json.loads(get_all_network_groups())
	for group in network_objects:
		print("Deleting group " + str(group["id"]))
		print(delete_group(group["id"]))