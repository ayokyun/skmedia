from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('127.0.0.1')

print(client.is_socket_open())
r = client.read_holding_registers(0, count=2)
print(r.registesr)
# client.write_coil(1, True)
# result = client.read_coils(1,1)
# print(result.bits[0])
client.close()
