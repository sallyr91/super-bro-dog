class Yo:
	def __init__(self, x):
		self.x = x
		
	def __str__(self):
		return 'value: {0}'.format(self.x)

list1 = [Yo(y) for y in range(10)]
list2 = list1

#list2.extend([list1[0], list1[1], list1[2]])

list2.remove(list2[2])



#list3.remove(list3[13])

for yo in list1:
	print(yo)