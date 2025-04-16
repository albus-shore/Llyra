from llyra import Model

model = Model()

response = model.call('Evening!')

print(response)

print(model.query)
print(model.response)
print(model.log.history)
