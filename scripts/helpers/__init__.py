from datetime import datetime

from .rsa_cryptography import RSACryptography

cryptography = RSACryptography(2048)

class timestamp:

    @staticmethod
    def now():
        currentDatetime = datetime.now()
        currentSecond = datetime.timestamp(currentDatetime)
        currentMillisecond = currentSecond * 1000
        currentTimestamp = int(currentMillisecond)
        return currentTimestamp