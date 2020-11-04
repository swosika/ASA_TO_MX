## import necessary libraries 
import requests
import json
import firewalldemo as fd


session = requests.Session()
## define necessary parameters as global variables 
"""
ORG_ID = ""
API_KEY = ""

def me(API_KEY1,ORG_ID1):
	global ORG_ID
	global API_KEY
	ORG_ID = ORG_ID1
	API_KEY = API_KEY1
	print (ORG_ID,API_KEY)
	return ORG_ID, API_KEY

print (ORG_ID,API_KEY, "ALEX")
"""
#BASE_URL = "https://api.meraki.com/api/v0/organizations/" + ORG_ID + "/networkObjects"
#headers={"content-type":"application/json", "X-Cisco-Meraki-API-Key": API_KEY}
"""
print (BASE_URL)
"""## define function for creating object group from parsed text file
def add_network_object_group(name,ORG_ID,API_KEY):
	BASE = "https://api.meraki.com/api/v0"
	URL = BASE + "/organizations/" + ORG_ID + "/networkObjectGroups"
	payload = {"name":name,"networkObjectIds":[]}
	headers={"content-type":"application/json", "X-Cisco-Meraki-API-Key": API_KEY}
	r=session.post(URL, params=payload,headers=headers)
	dic = json.loads(r.text)
	if("id" in dic):
		return int(dic["id"])
	return None

## define function for creating objects to go inside group 
def add_network_object(name,ip,groupid,ORG_ID,API_KEY):
	BASE_URL = "https://api.meraki.com/api/v0/organizations/" + ORG_ID + "/networkObjects"
	headers={"content-type":"application/json", "X-Cisco-Meraki-API-Key": API_KEY}
	payload = {"name":name,"type":"ipv4Cidr","value":ip,"networkObjectGroupIds":[groupid]}
	r=session.post(BASE_URL, json=payload,headers=headers)
	return r.text

## create network object groups
def create_network_groups(object_groups,ORG_ID,API_KEY):
	for group in object_groups:
		name = group[0]
		print("====CREATED GROUP " + name + " ======")
		groupid = add_network_object_group(name,ORG_ID,API_KEY)
		print("- group created with id " + str(groupid))
		count = 0
		for network_object in group[1]:
			print("----creating network object----")
			obj_name = name +"_"+str(count)
			print(obj_name)
			print(str(network_object))
			result = add_network_object(obj_name,str(network_object),groupid,ORG_ID,API_KEY)
			count+=1
			print(result)

#### functions needed to clear objects previously created (for testing environment only) ####
## acquire network objects from organization using BASE_URL
def get_all_network_objects(API_KEY,ORG_ID):
	BASE_URL = "https://api.meraki.com/api/v0/organizations/" + ORG_ID + "/networkObjects"
	headers={"content-type":"application/json", "X-Cisco-Meraki-API-Key": API_KEY}
	r=session.get(BASE_URL,headers=headers)
	return r.text

## acquire network object groups from organization using BASE_URL and "/networkObjectGroups"
def get_all_network_groups(ORG_ID, API_KEY):
	BASE = "https://api.meraki.com/api/v0"
	URL = BASE + "/organizations/" + ORG_ID + "/networkObjectGroups"
	headers={"content-type":"application/json", "X-Cisco-Meraki-API-Key": API_KEY}
	r=session.get(URL,headers=headers)
	return r.text

## define how to delete an object
def delete_object(obj_id, ORG_ID,API_KEY):
	BASE = "https://api.meraki.com/api/v0"
	URL = BASE + "/organizations/" + ORG_ID + "/networkObjects/" + str(obj_id)
	headers={"content-type":"application/json", "X-Cisco-Meraki-API-Key": API_KEY}
	print(URL)
	r=session.delete(URL, headers=headers)
	print(r)
	return r.text

## iterate through network objects, delete one at a time 
def delete_all_network_objects(API_KEY,ORG_ID):
	try:
		network_objects = json.loads(get_all_network_objects(API_KEY,ORG_ID))
		for netobj in network_objects:
			print("Deleting object " + str(netobj["id"]))
			print(delete_object(netobj["id"],ORG_ID,API_KEY))
	except:
		print ("no objects detected")
		 

## define how to delete a group
def delete_group(group_id,ORG_ID,API_KEY):
	BASE = "https://api.meraki.com/api/v0"
	URL = BASE + "/organizations/" + ORG_ID + "/networkObjectGroups/" + str(group_id)
	print(URL)
	headers={"content-type":"application/json", "X-Cisco-Meraki-API-Key": API_KEY}
	r=session.delete(URL,headers=headers)
	print(r)
	return r.text

## iteratate through object groups, delete one at a time 
def delete_all_network_groups(API_KEY,ORG_ID):
	print (ORG_ID,API_KEY)
	network_objects = json.loads(get_all_network_groups(ORG_ID, API_KEY))
	for group in network_objects:
		print("Deleting group " + str(group["id"]))
		print(delete_group(group["id"],ORG_ID,API_KEY))

