# import me
# from datetime import datetime,date,time

# h='25'
# while(1):
# 	if(h!=datetime.now().strftime('%H')):
# 		h = datetime.now().strftime('%H')
# 		me.refresh(0)

import os
hostname = "netaccess.iitm.ac.in" #example
response = os.system("ping -c 1 " + hostname)

#and then check the response...
if response == 0:
  print hostname, 'is up!'
else:
  print hostname, 'is down!'