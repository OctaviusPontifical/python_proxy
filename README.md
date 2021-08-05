# python_proxy

## Black list <br/>
####  Format file <br/>
Site:Domain:Port:SubDomain:Source <br/>
Empty - ignore  <br/>
all - block all data <br/>
80,443 - block only 80 and 443 <br/>
###### Example for adservice.google.com:443 <br/>
google:::adservice: - block only subdomain <br/>
google:com::: - block only domain com <br/>
google::all:: - block all port for google <br/>
google:all:::192.128.1.20 block all site for 192.168.1.20 <br/>
