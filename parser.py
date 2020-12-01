from multichaincli import Multichain
import json

rpcuser = 'multichainrpc'
rpcpasswd = '7yt5M1numoWyfkRSh2mMTuRUfk4wpjrEjn9vo61g11wu'
rpchost = 'localhost'
rpcport = '4366'
chainname = 'esiee-cyber-chain'

mychain = Multichain(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
infos = mychain.getinfo()
assets = mychain.listassets()
print("Blocks : "+str(infos['blocks']))
addresses = []

Wallet = {}
Adresses = {}

for asset in assets:
    print("========="+asset['name']+"=========")
    mychain.subscribe(asset['name'])
    Wallet[asset['name']] = 0
    for transaction in mychain.listassettransactions(asset['name']):
        try:
            message = ''.join(transaction['data'])
            message = bytearray.fromhex(message).decode()
        except:
            message = ''.join(transaction['data'])
            message = str(int(message,16))
        addresses = list(transaction['addresses'].keys())
        if len(addresses) > 1:
            amount = max(transaction['addresses'][addresses[1]],transaction['addresses'][addresses[0]])
            if transaction['addresses'][addresses[1]] < 0:
                recepteur = addresses[0]
                envoyeur = addresses[1]
            else:
                recepteur = addresses[1]
                envoyeur = addresses[0]
            print(envoyeur + " --> " + recepteur + " : " + str(amount) + " " + asset['name'] + ", data : " + message)
            
            if envoyeur not in Adresses:
                wallet = {asset['name'] : 0 }
                Adresses[envoyeur] = wallet
                Adresses[envoyeur][asset['name']] = -amount
            else:
                if asset['name'] not in Adresses[envoyeur]:
                    Adresses[envoyeur][asset['name']] = 0
                Adresses[envoyeur][asset['name']] -= amount

            if recepteur not in Adresses:
                wallet = {asset['name'] : 0 }
                Adresses[recepteur] = wallet
                Adresses[recepteur][asset['name']] = amount
            else:
                if asset['name'] not in Adresses[recepteur]:
                    Adresses[recepteur][asset['name']] = 0
                Adresses[recepteur][asset['name']] += amount




        else:
            amount = transaction['addresses'][addresses[0]]
            print(addresses[0] + " : " + str(amount) + " " + asset['name'] + ", data : " + message)


            if addresses[0] not in Adresses:
                wallet = {asset['name'] : 0 }
                Adresses[addresses[0]] = wallet
                Adresses[addresses[0]][asset['name']] = amount
            else:
                if asset['name'] not in Adresses[addresses[0]]:
                    Adresses[addresses[0]][asset['name']] = 0

                Adresses[addresses[0]][asset['name']] += amount



for adresse in Adresses:
    print()
    print("========="+adresse+"=========")
    print()
    for money in Adresses[adresse]:
        print("solde de "+money+"  :  "+ str(Adresses[adresse][money]))
        
