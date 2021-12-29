import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
from adafruit_magtag.magtag import MagTag
import terminalio

numOfPlanefenceDisplayItems = 8

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise
 
print("Connecting to %s"%secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!"%secrets["ssid"])

pool = socketpool.SocketPool(wifi.radio)

def getPlanefenceList():
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    p = []
    response = requests.get(secrets["planefence"] + "/plane-alert/plane-alert.csv")
    for plane in response.text.splitlines():
        f = plane.split(",")
        p.append(f)
    return p

magtag = MagTag()
for x in range(numOfPlanefenceDisplayItems):
    magtag.add_text(
        text_font=terminalio.FONT,
        text_position=(
            10,
            x*15 + 5,
        ),
        text_scale=0.5,
    )

while True:
    pl = getPlanefenceList()
    for i in range(1, numOfPlanefenceDisplayItems):
        if i <= len(pl) and len(pl) > 0:
            magtag.set_text(pl[len(pl)- i][1] + " " + pl[len(pl)-i][3] + " " + pl[len(pl)-i][2], index=i, auto_refresh=False)
        else:
            magtag.set_text("No interesting planes from Planefence.")
 
    magtag.refresh()
    magtag.exit_and_deep_sleep(60 * 10)
    #magtag.enter_light_sleep(60) 
 