import time
import os

from bookingNaver import getAvailableSchedule
from sms import send_message

g_MY_PHONE_NUMBER = os.getenv('MY_PHONE_NUMBER')

if __name__ == '__main__':
    placeid = '57148'
    itemid = '4692569'
    print('> placeid: ', placeid, ' itemid: ', itemid)
    while True:
        availableSchedule = getAvailableSchedule(placeid=placeid, itemid=itemid, startDate='2023-01-14', endDate='2023-03-01', person=2)
        availableSchedule = sorted(availableSchedule)
        if len(availableSchedule) >= 1:
            message = 'https://booking.naver.com/booking/6/bizes/57148/items/' + itemid
            message += ' ' + str(availableSchedule)
            print(message)
            send_message(message, g_MY_PHONE_NUMBER)
            break
        time.sleep(5)