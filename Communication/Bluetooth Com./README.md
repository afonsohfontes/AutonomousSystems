# BLUETOOTH COMMUNICATION

Na comunicação Bluetooth no nosso projeto iremos trabalhar com o módulo PyBluez, sendo ele um módulo de extensão python que permite os acessos que precisamos.

# Exemplo

```
# Exemplo Simples
import Bluetooth # Importa o módulo Bluetooth

nearby_devices = bluetooth.discover_devices(lookup_names=True) #Localização de dispositivos)
print("found %d devices" % len(nearby_devices)) #Print dos dispositivos localizados

for addr, name in nearby_devices:
    print("  %s - %s" % (addr, name))
# Bluetooth modo conservação de energia
from bluetooth.ble import DiscoveryService

service = DiscoveryService()
devices = service.discover(2)

for address, name in devices.items():
    print("name: {}, address: {}".format(name, address))
```
