import ipfshttpclient
client = ipfshttpclient.connect('/dns/localhost/tcp/5001/http') 
res = client.add('convert.py')
res
print(client.cat(res['Hash']))
