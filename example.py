from CMDBuild import CMDBuildNLMK as cmdb

cd = cmdb(username='',password='')

r1 = cd.connect()

r3 = cd.get_classes_NetworkBox()
print (r3)

new_NetBox_card = {
    "Code":"TEST_ITEM_api",
    "Hostname":"TEST_ITEM_api",
    "Availability":72, 
}

r4 = cd.

r2 = cd.close()
