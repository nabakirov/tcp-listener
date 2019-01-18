from decouple import config


PORT = config('PORT', cast=int)
ID_KEY = config('ID_KEY', cast=str, default='id')
LAT_KEY = config('LAT_KEY', cast=str, default='lat')
LNG_KEY = config('LNG_KEY', cast=str, default='lng')
TIMESTAMP_KEY = config('TIMESTAMP_KEY', cast=str, default='timestamp')
SPEED_KEY = config('SPEED_KEY', cast=str, default='speed')
BEARING_KEY = config('BEARING_KEY', cast=str, default='bearing')

REQUEST_URL = config('REQUEST_URL', cast=str)

RAW_KEY = config('RAW_KEY', cast=str, default=None)

DEFAULT_TOKEN = 'Bearer ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SndhRzl1WlNJNklpczVPVFl4TVRFeE1URXhNVEVpTENKNExXbHpjeTEwYVcxbElqb2lNakF4Tmkwd09TMHlPRlF3T0Rvek16b3hOaUlzSW5ndGRYTmxjaTFoWkdSeVpYTnpJam9pTWpFeUxqRXhNaTR4TURZdU1Ua3dJaXdpYzJOdmNHVWlPaUp3WVhOelpXNW5aWElzZFhObGNpSXNJbWx6Y3lJNkluUmxlaTA1T1RZdE1EQXVZWHAxY21WM1pXSnphWFJsY3k1dVpYUWlMQ0p1WVcxbElqb2lYSFV3TkRGaFhIVXdORE0xWEhVd05EUXlYSFV3TkRReVhIVXdORE00WEhVd05ETXhYSFV3TkRNMVhIVXdORE5oSW4wLmtFeUNvZ3VWZTBLZkNONk81eFNrc3RHal80SXdLd1V1NHV3QlJPc1FjYWc'

TOKEN = config('TOKEN', default=DEFAULT_TOKEN)

LOG_LEVEL = config('LOG_LEVEL', cast=str, default='INFO')
