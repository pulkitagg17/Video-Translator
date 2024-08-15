a = float(input("Weight: "))
b = str(input("In (K)kg or (L)lbs: "))
if(b == 'K' or b == 'k'):
    print(str(a*2.2)+'kg')
else:
    print(str(a * 0.45) + 'kg')