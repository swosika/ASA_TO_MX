import asaparser as ap
import meraki_messenger as mm

FNAME = input("Enter File Name: ")#ASA File for reading


##################################################################################
#lets begin by clearning the network
print("\n==========CLEARING THE NETWORK FOR TESTING===========")
print("this may take a while...")

mm.delete_all_network_groups()
mm.delete_all_network_objects()
##################################################################################

print("\nreading the asa file...")

#now we're going to read the asa file
object_groups = ap.gather_data(FNAME)

print("\n==========CREATING THE NETWORK GROUPS AND OBJECTS===========")
#now we're going to create the network groups and objects
mm.create_network_groups(object_groups)
