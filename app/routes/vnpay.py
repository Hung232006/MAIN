import urllib.parse, hashlib

class vnpay:
    def __init__(self):
        self.requestData = {}

    def get_payment_url(self, base_url, secret_key):
        sorted_params = sorted(self.requestData.items())
        query_string = urllib.parse.urlencode(sorted_params)
        hash_data = "&".join([f"{k}={v}" for k, v in sorted_params])
        secure_hash = hashlib.sha512((secret_key + hash_data).encode("utf-8")).hexdigest()
        return f"{base_url}?{query_string}&vnp_SecureHash={secure_hash}"
