from CMDBuild import CMDBuildNLMK as cmdb

cd = cmdb(username='',password='')

r1 = cd.connect()

r3 = cd.get_classes_NetworkBox()
print (r3)

r2 = cd.close()
