from llyra.remote import Remote

model = Remote()

response_1 = model.chat('Greeting',True)
response_2 = model.chat('Do you remember what I said at beginning?', True)

print(model.log.get(0))

response_3 = model.chat('Evening!',False)

print(model.log.get(-1))