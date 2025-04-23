from llyra import Model

model = Model()

response_1 = model.chat('Evening!',keep=True)

print(response_1)

#response_2 = model.chat('What inference engin you are running on?',True)

#print(response_2)

response_3 = model.chat('What I said at the beginning?',True)

print(response_3)

print(model.prompt.iteration)
print(model.log.history)

response_4 = model.chat('Evening!',keep=False)

print(response_4)

print(model.prompt.iteration)
print(model.log.history)