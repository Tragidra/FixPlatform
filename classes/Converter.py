import hashlib

import segno
from segno import helpers


class DB:
    def queryset_to_values(self, value1, value2=None):
        if value2 is None:
            return list(value1)
        else:
            return list(value1)[0][value2]

    def data_to_hash(self, value):
        value = hashlib.sha1(value.encode()).hexdigest()
        return value

    def create_qr(self, value1, value2):
        qrcode = helpers.make_mecard(name=value1,
                                     email=value2,
                                     url=['http://127.0.0.1:8000'])
        qrcode.save('files/images/qr-cods/' + str(value2)+'.png', dark="orange", light="#323524", scale=5)
