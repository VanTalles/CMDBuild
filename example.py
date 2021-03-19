from CMDBuild import CMDBuildNLMK as cmdb

cd = cmdb(username='',password='')

r1 = cd.connect()


r3a = cd.get_ProductsInfo(bname = 'WS-C2950G-12-EI')  

print (r3a)
ret = {
    'Model' : r3a['data'][0]['_id'],
    'Brand' : r3a['data'][0]['Brand'],
}

print (ret)


r3 = cd.get_classes_NetworkBox()
print (r3)

new_NetBox_card = {
    "Code":"TEST_ITEM_api",
    "Hostname":"TEST_ITEM_api",
    "Availability":72, 
    "State":121,
    "Model": r3a['data'][0]['_id'],
    "Brand": r3a['data'][0]['Brand'],
}

r4 = cd.insert_card_NetworkBox(card_data = new_NetBox_card)
print (r4)



r2 = cd.close()
