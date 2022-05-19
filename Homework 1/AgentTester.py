import Agent as a

testAgent = a.Agent("Daniel", 21, 79, 17)
testAgent2 = a.Agent("Daniel", 9, 79, 17)

print(testAgent.name)
print(testAgent.getName())
testAgent.setName("Dan")
print(testAgent.getName())
testAgent.MoveLocationRandom()
testAgent.MoveLocationRandom()
testAgent.MoveLocationSouth()
testAgent.MoveLocationBasedOnAge()
testAgent2.MoveLocationBasedOnAge()






