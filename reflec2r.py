'''
                    ,...  ,,
                  .d' ""`7MM
                  dM`     MM
`7Mb,od8 .gP"Ya  mMMmm    MM  .gP"Ya   ,p6"bo  pd*"*b. `7Mb,od8
  MM' "',M'   Yb  MM      MM ,M'   Yb 6M'  OO (O)   j8   MM' "'
  MM    8M""""""  MM      MM 8M"""""" 8M          ,;j9   MM
  MM    YM.    ,  MM      MM YM.    , YM.    , ,-='      MM
.JMML.   `Mbmmd'.JMML.  .JMML.`Mbmmd'  YMbmd' Ammmmmmm .JMML.

----------------------------------------------------------------

Description: Send payments back to original users.
Author: David Stancu (@mach-kernel)
'''

from dwolla import transactions as t, constants as c
from models import *
from sys import exit

import datetime, os

c.client_id = os.getenv('DWOLLA_KEY', '?')
c.client_secret = os.getenv('DWOLLA_SECRET', '?')
c.access_token = os.getenv('DWOLLA_TOKEN', '?')
c.pin = os.getenv('DWOLLA_PIN', '0000')
c.sandbox = os.getenv('DWOLLA_SANDBOX', '?')

try:  
    # Make sure only one instance running
    shitty_mutex = ReflectorSettings.get(ReflectorSettings.key == 'running')

    if shitty_mutex.value == '1':
        print "reflec2r: Another instance already running; exiting."
        exit(-1)
    else:
        print "reflec2r: Lock obtained, starting application."
        shitty_mutex.value = '1'
        shitty_mutex.save()

    # Retrieve the last 800 transactions. Check all new transactions
    # against them for insurance that we will not pay something 
    # which has already been processed.
    old_tx_ids = [i for sub in Reflector.select(Reflector.tx).order_by(Reflector.id.desc()).limit(800).tuples() for i in sub]

    print "reflec2r: Fetching transactions from Dwolla."

    # Query Dwolla for transactions
    txlist = t.get(types='money_received', limit=200) \
        + t.get(types='money_received', limit=200, skip=200) \
        + t.get(types='money_received', limit=200, skip=400) \
        + t.get(types='money_received', limit=200, skip=600) \
        + t.get(types='money_received', limit=200, skip=800) \

    # Reimburse those that qualify
    for tx in txlist:
        if tx['Id'] not in old_tx_ids:
            r = t.send(tx['Source']['Id'], tx['Amount'])
            Reflector.create(amount=tx['Amount'], date=datetime.datetime.now(), refund=r, tx=tx['Id']).save()
            print "reflec2r: Successfully sent $" + str(tx['Amount']) + " to " + str(tx['Source']['Id'])
        else:
            print "reflec2r: Skipping transaction #" + str(tx['Id']) + ", already reflected."

    # Unlock mutex, exit
    shitty_mutex.value = 0
    shitty_mutex.save()

    print "reflec2r: Gracefully executed, quitting application."
    exit(0)

except Exception as e:
    print "reflec2r: Execution failed on " + str(datetime.datetime.now()) + ", dumping exception, unlocking and quitting."
    print "reflec2r: " + e.message
    shitty_mutex.value = 0
    shitty_mutex.save()
    exit(-1)
