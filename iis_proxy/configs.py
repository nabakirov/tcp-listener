port_to_listen = 4442

send_to = \
    dict(
        var=dict(
                lat="lat",
                lng="lng",
                id="id",
                speed="speed",
                timestamp='timestamp',
                bearing='bearing'
        ),
        url='http://176.123.244.7/transport/v1/bus',
        method="POST",
        name='traccar',
        send_nulls=True
    )
