from ctypes import sizeof


llista = [1,2,3,4,5,6,7]
roots = []
lists = []
lists.append(llista)
for llist in lists:
    mid = len(llist)//2

    if len(llist) == 1:
        roots.append(llist[0])
    else:
        left = llist[:mid]
        right = llist[mid+1:]
        lists.append(left)
        lists.append(right)
        print(lists)
        print(mid, left, right, llist)
        print()

        roots.append(llist[mid])
print(sizeof([1,2,3,4,5,6,7,8]))