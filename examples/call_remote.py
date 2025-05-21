from llyra import Remote

model = Remote()

response = model.call('Everning!')

print(response)
print(model.log.get(0))