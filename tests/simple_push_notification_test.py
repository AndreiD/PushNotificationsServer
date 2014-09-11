#!/usr/bin/python
# -*- coding: utf-8 -*-

# Project Number: 283442064750
# API KEY AIzaSyDejSxmynqJzzBdyrCS-IqMhp0BxiGWL1M

from gcm import *


gcm = GCM("AIzaSyDejSxmynqJzzBdyrCS-IqMhp0BxiGWL1M")
data = {'the_message': 'You have x new friends', 'param2': 'value2'}




# Plaintext request
reg_id = 'APA91bHDRCRNIGHpOfxivgwQt6ZFK3isuW4aTUOFwMI9qJ6MGDpC3MlOWHtEoe8k6PAKo0H_g2gXhETDO1dDKKxgP5LGulZQxTeNZSwva7tsIL3pvfNksgl0wu1xGbHyQxp2CexeZDKEzvugwyB5hywqvT1-UJY0KNqpL4EUXTWOm0RXE5CrpMk'
gcm.plaintext_request(registration_id=reg_id, data=data)
