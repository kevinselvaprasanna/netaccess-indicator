#!/usr/bin/env python
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
from mechanize import Browser
from gi.repository import Notify
import gnomekeyring as gk
import signal
import threading
from multiprocessing import Process
import thread
import MySQLdb
import os
#import gtk as Gtk


icon = '/usr/share/icons/ubuntu-mono-light/apps/22/distributor-logo.svg'
def show():
		with open("/home/kevinselvaprasanna/netaccess-indicator/netaccess.html",'r') as f:
			lines = f.readlines()
		print "Refresh3"
		for l in lines:
			words = l.split()
			if (len(words)>0):
				if (words[0]=="<b>Total"):
					data = words[2]+words[3][0]+words[3][1]
					ind.set_label(data,"netaccess-indicator")
					i = (float)(words[2])
					if(words[3][0]=='K'):
						i = i/1000
					c = (str)(1024.0-i)
					print "Refresh4"
					Notify.Notification.new("<b>Netaccess-indicator</b>","Data used: " +  data + " \nData remaining: "+ c + "MB", icon).show()
					print "Refresh ended....."


def login():
		# New browser object
		br = Browser()

		#Open Login page
		print "Logging in"
		page = br.open( 'https://netaccess.iitm.ac.in/account/login' )
		br.select_form( nr = 0 )

		# Fill in the fields
		br.form[ "userLogin" ] = roll
		br.form[ "userPassword" ] = password

		# Submit to login
		br.submit()

		print "Approving your IP"
		# Directly go to the approve page. Cookies taken care of by Mechanize browser
		resp = br.open( 'https://netaccess.iitm.ac.in/account/approve' )

		# Hardcoded response due to bad HTML on site
		hardcoded_resp = '''
		<form class="form-horizontal" method="post" action="/account/approve">
		<fieldset>
		<!-- Form Name -->
		<legend>Authorization</legend>
		<!-- Multiple Radios -->
		<div class="form-group">
		  <label class="col-md-4 control-label" for="radios">Duration</label>
		  <div class="col-md-4">
		  <div class="radio">
		    <label for="radios-0">
		      <input type="radio" name="duration" id="radios-0" value="1" checked="checked">
		      60 minutes (recommended for public machines)
		    </label>
		  </div>
		  <div class="radio">
		    <label for="radios-1">
		      <input type="radio" name="duration" id="radios-1" value="2">
		      1 day (hostel zone)
		    </label>
		  </div>
		  </div>
		</div>
		<!-- Button -->
		<div class="form-group">
		  <label class="col-md-4 control-label" for="approveBtn"></label>
		  <div class="col-md-4">
		    <button id="approveBtn" name="approveBtn" class="btn btn-primary">Authorize</button>
		  </div>
		</div>
		</fieldset>
		</form> 
		'''

		# Setting response for Page as the hardcoded response.
		resp.set_data( hardcoded_resp )
		br.set_response( resp )
		# Filling the form using the hardcoded response
		br.select_form( nr = 0 )

		# Set duration as 1 for one hour and 2 for one day
		br.form[ 'duration' ] = [ '2' ]
		response = br.submit()
		print "Logged in"
		f = open('/home/kevinselvaprasanna/netaccess-indicator/netaccess.html', 'w')
		f.write(response.read())
		f.close()

def refresh(w):
	if(w==0):
		th = threading.Timer(10*60, refresh, 'h')
		th.daemon = True
		th.start()
		print "thread"
	print "Refreshing"
	keyring = 'login'
	keyItems = gk.list_item_ids_sync(keyring)

	for keyItem in keyItems:
	    key = gk.item_get_info_sync(keyring, keyItem)
	    if  key.get_display_name() == 'https://netaccess.iitm.ac.in/account/login':
	        password= key.get_secret()
	roll = "ee14b028"
	print "Refresh2"
	hostname = "netaccess.iitm.ac.in" 
	response = os.system("ping -c 1 " + hostname)
	if response == 0:
	  login()
	  show()
	else:
	  print hostname, 'is down!'
	

def quit(source):
	Gtk.main_quit()
				
if __name__ == "__main__":
	ind = appindicator.Indicator.new("netaccess-indicator",icon,appindicator.IndicatorCategory.SYSTEM_SERVICES)
	ind.set_status(appindicator.IndicatorStatus.ACTIVE)
	menu = Gtk.Menu()

	for i in range(3):
		if(i==0):
			menu_items = Gtk.MenuItem("Refresh")
			menu.append(menu_items)
			menu_items.connect("activate",refresh)
			menu_items.show()
	item_quit = Gtk.MenuItem("Quit")
	item_quit.connect('activate',quit)
	menu.append(item_quit)
	item_quit.show()
	ind.set_menu(menu)
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	Notify.init("netaccess-indicator")
	#gtk.timeout_add(10 * 1000, refresh, 'h')
	#threading.Timer(5.0, refresh, 'h').start()
	# p = Process(target=refresh, args ='h')
	# p.start()
	#thread.start_new_thread(refresh, (0,))
	#threading.Thread(target=refresh, args="0").start()
	refresh(0)
	print "return"
	Gtk.main()