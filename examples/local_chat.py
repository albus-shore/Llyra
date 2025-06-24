from llyra import Llyra

model = Llyra('local')

response = model.chat('Evening!',True)

print(response)

response = model.chat("What's my first word's in learning language?",True)

print(response)

model.update_chat(addition='')
response = model.chat('Evening!',False)

print(response)

response = model.chat('What have I said before?',False)

print(response)

specific_log = model.get_log(1)
log = model.get_log(-1)

print(specific_log)
print(log)