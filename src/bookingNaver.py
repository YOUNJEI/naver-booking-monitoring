import requests

from datetime import datetime

def getInStockDate(placeid, itemid, startDate, endDate, person):
    url = 'https://api.booking.naver.com/v3.0/businesses/' + placeid + '/biz-items/' + str(
        itemid) + '/hourly-schedules?noCache=' + str(datetime.now().timestamp()) + '&endDateTime=' + endDate + 'T00:00:00&startDateTime=' + startDate + 'T00:00:00'
    j = requests.get(url).json()
    inStockDate = set()
    for object in j:
        if object['isUnitSaleDay'] == True and object['stock'] - object['bookingCount'] >= person:
            inStockDate.add(object['unitStartTime'][0:10])
    return inStockDate

def getOpenedScheduleList(placeid, itemid, startDate, endDate, inStockDate):
    url = 'https://api.booking.naver.com/v3.0/businesses/' + placeid + '/biz-items/' + str(itemid) + '/daily-schedules?noCache=' + str(datetime.now().timestamp()) + '&endDateTime=' + endDate + 'T00:00:00&isRestaurant=true&startDateTime=' + startDate + 'T00:00:00'
    j = requests.get(url).json()
    openedScheduleList = set()
    for targetDate in inStockDate:
        if j[targetDate]['isHoliday'] == False and j[targetDate]['isSaleDay'] == True:
            openedScheduleList.add(targetDate)
    return openedScheduleList

# https://booking.naver.com/booking/6/bizes/57148/items/4692569
# placeid: 57148 (업체번호)
# itemid: 4692569 (상품ID)
# startDate: 2023-01-14
# endDate: 2023-02-28
# person: 2 (예약할 인원 수)
def getAvailableSchedule(placeid, itemid, startDate, endDate, person):
    inStockDate = getInStockDate(placeid, itemid, startDate, endDate, person)
    openedScheduleList = getOpenedScheduleList(placeid, itemid, startDate, endDate, inStockDate)
    return openedScheduleList