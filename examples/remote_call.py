from llyra import Llyra

model = Llyra('remote')

response = model.call('Evening!')

print(response)

log = model.get_log(-1)

print(log)