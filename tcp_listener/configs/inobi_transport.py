# TCP Listener will listen this port
LISTENER_PORT = 2222

# variables
id = 'id'
lat = 'lat'
lng = 'lng'
timestamp = 'timestamp'
speed = 'speed'
bearing = 'bearing'


# URL = 'http://176.123.244.7/transport/v1/bus'
# URL = 'http://192.168.1.241:5000/transport/bus'
URL = 'http://nginx:8963/transport/bus'
request_method = 'POST'
# if method is post data will send json object

# type of request if method is GET
# http://{url}?{id}=imei&{lat}=123123&{lng}=1231&{timestamp}=123&{speed}=123&{bearing}=131


# if authorization is require otherwise comment TOKEN
# token will be added in the headers
# {Authorization:{TOKEN}}
TOKEN = 'Bearer ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SndhRzl1WlNJNklpczVPVFl4TVRFeE1URXhNVEVpTENKNExXbHpjeTEwYVcxbElqb2lNakF4Tmkwd09TMHlPRlF3T0Rvek16b3hOaUlzSW5ndGRYTmxjaTFoWkdSeVpYTnpJam9pTWpFeUxqRXhNaTR4TURZdU1Ua3dJaXdpYzJOdmNHVWlPaUp3WVhOelpXNW5aWElzZFhObGNpSXNJbWx6Y3lJNkluUmxlaTA1T1RZdE1EQXVZWHAxY21WM1pXSnphWFJsY3k1dVpYUWlMQ0p1WVcxbElqb2lYSFV3TkRGaFhIVXdORE0xWEhVd05EUXlYSFV3TkRReVhIVXdORE00WEhVd05ETXhYSFV3TkRNMVhIVXdORE5oSW4wLmtFeUNvZ3VWZTBLZkNONk81eFNrc3RHal80SXdLd1V1NHV3QlJPc1FjYWc'

