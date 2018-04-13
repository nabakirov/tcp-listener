port_to_listen = 4441

send_to = \
    dict(
        var=dict(
                lat="lat",
                lng="lon",
                id="id",
                speed="speed",
                timestamp='timestamp',
                bearing='bearing'
        ),
        url='http://traccar:5055',
        method="GET",
        name='traccar',
        send_nulls=False
    )
