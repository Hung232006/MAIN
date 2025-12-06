import urllib.parse, hashlib

class vnpay:
    def __init__(self):
        self.requestData = {}

    def get_payment_url(self, base_url, secret_key):
        if not base_url or not secret_key:
            raise ValueError("base_url hoặc secret_key không được để trống")

        # Sắp xếp params theo key
        sorted_params = sorted(self.requestData.items())

        # Tạo query string
        query_string = urllib.parse.urlencode(sorted_params)

        # Chuỗi để hash
        hash_data = "&".join([f"{k}={v}" for k, v in sorted_params])

        # Tạo secure hash
        secure_hash = hashlib.sha512((secret_key + hash_data).encode("utf-8")).hexdigest()

        return f"{base_url}?{query_string}&vnp_SecureHash={secure_hash}"
