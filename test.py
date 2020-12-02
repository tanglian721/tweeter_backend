# aa = [     
#     [1,4],
#       [2,4],
#       [2,3],
#       [4,1],
#       [2,4],
#       [5,4],
#       [2,4]
#       ]
# print(aa)
# newaa = []
# for a in aa:
#     # print([a[0], a[1]])
#     # print([a[1], a[0]])
#     # print(newaa)
#     if [a[0], a[1]] not in newaa and [a[1], a[0]] not in newaa:
#        newaa.append([a[0], a[1]])
       


# print(newaa)

# test_list = [1, 3, 5, 6, 3, 5, 6, 1] 
# print ("The original list is : " +  str(test_list)) 
# res = [] 
# for i in test_list: 
#     if i not in res: 
#         res.append(i) 
# print ("The original list is : " +  str(res)) 

a = {
    "key1": "a",
    "key2": "b",
}

a["key3"] = a ["key2"]
a.pop('key2')
print(a)