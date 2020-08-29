from threading import Thread
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ProxyTask(Thread):

    def __init__(self, proxy,filename):
        super().__init__()
        self._proxy = proxy
        self._filename=filename
    
    def run(self):
        url = 'https://httpbin.org/post'
        try:
            r1 = requests.post(url=url, proxies={"https": self._proxy}, verify=False, timeout=10)
            if r1.status_code==200:
                with open(self._filename[0:10] + '_temp', 'a+') as f:
                    entry = self.encrypt(self._proxy)
                    f.write('{0}\n'.format(format(entry)))
            else:
                pass
        except :
            pass

    def decrypt(self,encrypted):
        encrypted = int(encrypted)
        key_int = 19961225
        decrypted = encrypted ^ key_int
        length = (decrypted.bit_length() + 7) // 8
        decrypted_bytes = int.to_bytes(decrypted, length, 'big')
        return decrypted_bytes.decode()

    def encrypt(self, raw):
        raw_bytes = raw.encode()
        raw_int = int.from_bytes(raw_bytes, 'big')
        key_int = 19961225
        return raw_int ^ key_int