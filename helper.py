
import requests
import arrow
import gspread
from dateutil import tz
from oauth2client.client import SignedJwtAssertionCredentials


#Constants 
# -- sheetsu
SHEETSU_URL = "http://sheetsu.com/apis/4c61fd45"
MASTER_URL = "https://docs.google.com/spreadsheets/d/1fCtHu00KCcOAG124hyyrwu3iltEd6amJPYhhXrO3ptY"

# -- column names
ARROWTIME = 'arrowtime'
SHEETURL = 'SheetURL'
DATE = 'Day'
TIMENYC = 'TimeNYC'

#Other globals:
GC = None

def setup():
    json_key = json.load(open('Bernie-Balancer-oauth.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], bytes(json_key['private_key'], 'utf-8'), scope)
    gc = gspread.authorize(credentials)
    GC = gc



#Gets the master list of calls from spreadsheet
def allSlots(): 
    
    r = requests.get(SHEETSU_URL)
    try:
        all_slots = r.json()['result']
    except Exception as e:
        return {"Error":e}
    return all_slots

def getAvailableSlots():
    all_slots = allSlots()
    #available = in the future, and < 30 attendees
    possible_slots = possibleFilter(all_slots)
    available_slots = availableFilter(possible_slots)
    return available_slots

def updateSlots():
    all_slots = allSlots()
    possible_slots = possibleFilter(all_slots)
    #new = doesn't have a spreadsheet linked yet
    new_slots = newSlots(available_slots)
    #STUB: create google sheets
    return True

def availableFilter(possible_slots):
    #given a list of slots, figure out which still have open positions
    # return those
    #STUB
    return possible_slots



def possibleFilter(all_slots):
    #given a dict of times, filter in those in the future and those that aren't full
    # then filter in those that have a sheet URL
    for slot in all_slots:
        slot[ARROWTIME] = dateTimer(slot)
    
    sorted_slots = sorted(all_slots, key = lambda slot: slot[ARROWTIME], reverse=False)

    #now remove stuff earlier than today
    now = arrow.utcnow()
    while len(sorted_slots) > 0:
        slot = sorted_slots[0]
        if slot[ARROWTIME].to('utc') < now:
            sorted_slots.pop(0)
        else:
            break
    available_slots = sorted_slots 
    available_slots = [x for x in available_slots if x[SHEETURL] =! '']
    return available_slots

def newSlots(available_slots):
    #Given a dict of times, find only those that have no linked spreadsheet
    new_slots = [x for x in available_slots if x[SHEETURL] == '']
    return available_slots

def updateNewSlots(new_slots, available_slots, sheet_url):
    #for each new slot, create a google sheet, then link it to the master sheet and update the available_slots json
    #return the avaialble_slots json for use by the app
    return available_slots


def dateTimer(slot):
    datetime_text = slot[DATE] + " " + slot[TIMENYC]
    try:
        toreturn = arrow.get(datetime_text, 'M/D/YYYY H:m PP')
        toreturn.replace(tzinfo=tz.gettz("US/Eastern"))
    except:
        #print("ERROR" + datetime_text)
        toreturn = "ERROR" + slot[DATE] + " " + slot[TIMENYC]
    return toreturn