import http.client

zone = '00001.dns.army'
token = 'QcxNtFcxsE7213H8KM8zkpARYQFEf4'


def dynv6_update(ipv6):
    conn = http.client.HTTPSConnection('dynv6.com', source_address=('0.0.0.0', 0))
    conn.request(
        'GET',
        f'/api/update?ipv6={ipv6}&zone={zone}&token={token}'
    )
    res = conn.getresponse()
    data = res.read()
    return data.decode('utf-8')
