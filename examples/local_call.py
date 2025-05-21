from llyra import Local

model = Local()

response = model.call('Evening!')

print(response)

print(model.query)
print(model.response)
print(model.log.get(0))
