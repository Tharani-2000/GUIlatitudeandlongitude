import urllib.request, urllib.parse, urllib.error
import json
import ssl
from tkinter import *
import sys

api_key = False

if api_key is False:
    api_key = 42
    serviceurl = 'http://py4e-data.dr-chuck.net/json?'
else :
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def getlocation():
    address = et.get()
    if len(address) < 1:
        return 

    parms = dict()
    parms['address'] = address
    if api_key is not False: parms['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')

    try:
        js = json.loads(data)
    except:
        js = None

    if not js or 'status' not in js or js['status'] != 'OK':
        print('==== Failure To Retrieve ====')
        print(data)
        return

    lat = js['results'][0]['geometry']['location']['lat']
    lng = js['results'][0]['geometry']['location']['lng']
    print(lat,lng)
    l2.configure(text = "Lat:    "+str(lat))
    l3.configure(text = "Lon:    "+str(lng))

def exit_press():
    window.destroy()
    sys.exit()


window = Tk()
window.title("LatLong")
window.geometry("800x450")


Title = Label(window, text="Get the Latitude and the Longitude", font=("Arial Bold",14))
l1 = Label(window, text="Enter the Adress") 
bt = Button(window,text="Enter", command=getlocation)
btn = Button(window, text="Quit",command=exit_press)


et = Entry(window,width = 40)
l2 = Label(window, text="Lat:    ") 
l3 = Label(window, text="Lon:    ") 

Title.grid(row=0,column=1)
l1.grid(row=2, column=0)
et.grid(row=2, column=1)
bt.grid(row=4, column=1)
btn.grid(row=5,column=1)
l2.grid(row=7, column=0)
l3.grid(row=8, column=0)

while True:
    window.mainloop()
