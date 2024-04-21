def triangle_print(n):
    for i in range(1,n+1):
        for j in range(n,0,-1):
            if j<=i:
                print(j,end=' ')
            else:
                print(len(str(j))*' ',end=' ')
        print()
triangle_print(12)
