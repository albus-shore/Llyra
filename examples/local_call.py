from llyra import Llyra

model = Llyra('local')

response = model.call('<|User|>Evening!<|Assistant|>')

print(response)

log = model.get_log(-1)

print(log)