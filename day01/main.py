from collections import Counter

from utils import read_input

# get input
the_input = read_input("input.txt")
list1 = []
list2 = []
for line in the_input:
    first, second = line.split("   ")
    list1.append(int(first))
    list2.append(int(second))

list1.sort()
list2.sort()

total_distance = 0
for left, right in zip(list1, list2):
    total_distance += abs(left - right)

print(total_distance)  # solution to part 1

right_counter = Counter(list2)
sim_score = 0
for num in list1:
    sim_score += num * right_counter.get(num, 0)

print(sim_score)  # solution to part 2
