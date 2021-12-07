from decimal import Decimal
list_1=[(Decimal('1500.00'), Decimal('1500.00'), 3, '10000001', '10260005', '10270002', None)]
t=[tuple(str(n) for n in m) for  m in list_1]
print(t)
for i in range(len(t[0])):
    print(type(t[0][i]))