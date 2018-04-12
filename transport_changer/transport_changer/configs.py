TRACCAR_USER = dict(
    login='inobi',
    password='BaKT0#@123&7230p'
)

PERCENT_SCALE = 40


PYTHON_ADMIN_TOKEN = 'ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6STFOaUo5LmV5SnNaV3dpT2lKclpXc2lMQ0p6YjIxbElqb2lkbUZzZFdVaUxDSnVieUk2SW1SaGRHRWlMQ0pwWkNJNkluUmxjM1FpTENKelkyOXdaWE1pT2xzaWRHVnpkQ0lzSW5SeVlXNXpjRzl5ZEY5aFpHMXBiaUpkTENKcFlYUWlPakUxTVRBeU1qZ3dORFI5Lmw0blkxT3NzN0dGVHpGWUF4eVFuaXljUzg4cEJvUy1RY2VMSXdiVWs1WUE='

psql = dict(
    dbname='inobi',
    user='inobi',
    password='YQv5tb>d1',
    host='pgsql'
)
psql2 = dict(
    dbname='traccar',
    user='traccar',
    password='Sa1T0#@!10!72301',
    host='pgsql'
)

TRACCAR_DB = 'traccar'
SERVER_DB = 'inobi'

inobi_conn = ' '.join('{}={}'.format(k, v) for k, v in psql.items())
traccar_conn = ' '.join('{}={}'.format(k, v) for k, v in psql2.items())

emails = [
    "nabakirov@gmail.com",
    "management-ml@tez.kg",
    "irsalabd@gmail.com",
    "maksat@tez.kg",
    "begaiym@tez.kg",
    "ernis@tez.kg"
]

sender = dict(
    email='inobisender@gmail.com',
    password='AviSa123'
)

