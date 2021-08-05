# python_proxy

## Black list
####  Format file
Site:Domain:Port:SubDomain:Source
Empty - ignore 
all - block all data
80,443 - block only 80 and 443
###### Example for adservice.google.com:443 
google:::adservice: - block only subdomain
google:com::: - block only domain com 
google::all:: - block all port for google
google:all:::192.128.1.20 block all site for 192.168.1.20
