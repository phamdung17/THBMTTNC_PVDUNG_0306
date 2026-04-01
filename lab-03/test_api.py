import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"


# ═══════════════════════════════════════════════════════════
#  RSA TEST CASES
# ═══════════════════════════════════════════════════════════

class TestRSAGenerateKeys:

    def test_generate_keys_status_200(self):
        """Tạo khóa trả về status 200"""
        res = requests.get(f"{BASE_URL}/api/rsa/generate_keys")
        assert res.status_code == 200

    def test_generate_keys_message(self):
        """Tạo khóa trả về message đúng"""
        res = requests.get(f"{BASE_URL}/api/rsa/generate_keys")
        assert res.json()["message"] == "Keys generated successfully"

    def test_generate_keys_returns_json(self):
        """Response phải là JSON"""
        res = requests.get(f"{BASE_URL}/api/rsa/generate_keys")
        assert res.headers["Content-Type"] == "application/json"

    def test_generate_keys_multiple_times(self):
        """Gọi generate nhiều lần không bị lỗi"""
        for _ in range(3):
            res = requests.get(f"{BASE_URL}/api/rsa/generate_keys")
            assert res.status_code == 200


class TestRSAEncrypt:

    def setup_method(self):
        requests.get(f"{BASE_URL}/api/rsa/generate_keys")

    def test_encrypt_status_200(self):
        """Mã hóa thành công trả về 200"""
        res = requests.post(f"{BASE_URL}/api/rsa/encrypt",
                            json={"message": "Hello HUTECH", "key_type": "public"})
        assert res.status_code == 200

    def test_encrypt_has_encrypted_message_field(self):
        """Response có field encrypted_message"""
        res = requests.post(f"{BASE_URL}/api/rsa/encrypt",
                            json={"message": "Hello HUTECH", "key_type": "public"})
        assert "encrypted_message" in res.json()

    def test_encrypt_result_is_valid_hex(self):
        """Kết quả mã hóa là chuỗi hex hợp lệ"""
        res = requests.post(f"{BASE_URL}/api/rsa/encrypt",
                            json={"message": "Hello HUTECH", "key_type": "public"})
        hex_str = res.json()["encrypted_message"]
        assert all(c in "0123456789abcdef" for c in hex_str)

    def test_encrypt_result_not_empty(self):
        """Kết quả mã hóa không rỗng"""
        res = requests.post(f"{BASE_URL}/api/rsa/encrypt",
                            json={"message": "Hello HUTECH", "key_type": "public"})
        assert len(res.json()["encrypted_message"]) > 0

    def test_encrypt_result_different_from_plaintext(self):
        """Ciphertext khác với plaintext gốc"""
        message = "Hello HUTECH"
        res = requests.post(f"{BASE_URL}/api/rsa/encrypt",
                            json={"message": message, "key_type": "public"})
        assert res.json()["encrypted_message"] != message

    def test_encrypt_same_message_different_result(self):
        """Mã hóa cùng message 2 lần cho kết quả khác nhau (OAEP padding)"""
        payload = {"message": "Hello HUTECH", "key_type": "public"}
        r1 = requests.post(f"{BASE_URL}/api/rsa/encrypt", json=payload).json()
        r2 = requests.post(f"{BASE_URL}/api/rsa/encrypt", json=payload).json()
        assert r1["encrypted_message"] != r2["encrypted_message"]

    def test_encrypt_short_message(self):
        """Mã hóa message ngắn (1 ký tự)"""
        res = requests.post(f"{BASE_URL}/api/rsa/encrypt",
                            json={"message": "A", "key_type": "public"})
        assert res.status_code == 200
        assert "encrypted_message" in res.json()

    def test_encrypt_message_with_numbers(self):
        """Mã hóa message chứa số"""
        res = requests.post(f"{BASE_URL}/api/rsa/encrypt",
                            json={"message": "HUTECH 2024", "key_type": "public"})
        assert res.status_code == 200

    def test_encrypt_message_with_special_chars(self):
        """Mã hóa message chứa ký tự đặc biệt"""
        res = requests.post(f"{BASE_URL}/api/rsa/encrypt",
                            json={"message": "Hello@HUTECH!", "key_type": "public"})
        assert res.status_code == 200

    def test_encrypt_invalid_key_type(self):
        """key_type không hợp lệ trả về error"""
        res = requests.post(f"{BASE_URL}/api/rsa/encrypt",
                            json={"message": "Hello", "key_type": "invalid"})
        assert "error" in res.json()

    def test_encrypt_with_private_key(self):
        """Mã hóa bằng private key cũng hoạt động"""
        res = requests.post(f"{BASE_URL}/api/rsa/encrypt",
                            json={"message": "Hello", "key_type": "private"})
        assert res.status_code == 200


class TestRSADecrypt:

    def setup_method(self):
        requests.get(f"{BASE_URL}/api/rsa/generate_keys")

    def _encrypt(self, message):
        return requests.post(f"{BASE_URL}/api/rsa/encrypt",
                             json={"message": message, "key_type": "public"}).json()["encrypted_message"]

    def test_decrypt_status_200(self):
        """Giải mã thành công trả về 200"""
        ct = self._encrypt("Hello HUTECH")
        res = requests.post(f"{BASE_URL}/api/rsa/decrypt",
                            json={"ciphertext": ct, "key_type": "private"})
        assert res.status_code == 200

    def test_decrypt_correct_message(self):
        """Giải mã cho lại đúng message gốc"""
        message = "Hello HUTECH"
        ct = self._encrypt(message)
        dec = requests.post(f"{BASE_URL}/api/rsa/decrypt",
                            json={"ciphertext": ct, "key_type": "private"}).json()
        assert dec["decrypted_message"] == message

    def test_decrypt_short_message(self):
        """Giải mã message 1 ký tự"""
        ct = self._encrypt("A")
        dec = requests.post(f"{BASE_URL}/api/rsa/decrypt",
                            json={"ciphertext": ct, "key_type": "private"}).json()
        assert dec["decrypted_message"] == "A"

    def test_decrypt_message_with_numbers(self):
        """Giải mã message chứa số"""
        msg = "HUTECH 2024"
        ct = self._encrypt(msg)
        dec = requests.post(f"{BASE_URL}/api/rsa/decrypt",
                            json={"ciphertext": ct, "key_type": "private"}).json()
        assert dec["decrypted_message"] == msg

    def test_decrypt_message_with_special_chars(self):
        """Giải mã message chứa ký tự đặc biệt"""
        msg = "Hello@HUTECH!"
        ct = self._encrypt(msg)
        dec = requests.post(f"{BASE_URL}/api/rsa/decrypt",
                            json={"ciphertext": ct, "key_type": "private"}).json()
        assert dec["decrypted_message"] == msg

    def test_roundtrip_multiple_messages(self):
        """Encrypt rồi Decrypt nhiều message đều đúng"""
        messages = ["HUTECH", "Python 3", "RSA 123", "Test!@#", "abc XYZ"]
        for msg in messages:
            ct = self._encrypt(msg)
            dec = requests.post(f"{BASE_URL}/api/rsa/decrypt",
                                json={"ciphertext": ct, "key_type": "private"}).json()
            assert dec["decrypted_message"] == msg, f"Failed for message: {msg}"

    def test_decrypt_invalid_key_type(self):
        """key_type không hợp lệ trả về error"""
        ct = self._encrypt("Hello")
        res = requests.post(f"{BASE_URL}/api/rsa/decrypt",
                            json={"ciphertext": ct, "key_type": "invalid"})
        assert "error" in res.json()


class TestRSASign:

    def setup_method(self):
        requests.get(f"{BASE_URL}/api/rsa/generate_keys")

    def test_sign_status_200(self):
        """Ký số thành công trả về 200"""
        res = requests.post(f"{BASE_URL}/api/rsa/sign",
                            json={"message": "HUTECH University"})
        assert res.status_code == 200

    def test_sign_has_signature_field(self):
        """Response có field signature"""
        res = requests.post(f"{BASE_URL}/api/rsa/sign",
                            json={"message": "HUTECH University"})
        assert "signature" in res.json()

    def test_sign_returns_valid_hex(self):
        """Chữ ký là chuỗi hex hợp lệ"""
        res = requests.post(f"{BASE_URL}/api/rsa/sign",
                            json={"message": "HUTECH University"})
        sig = res.json()["signature"]
        assert len(sig) > 0
        assert all(c in "0123456789abcdef" for c in sig)

    def test_sign_different_messages_different_signatures(self):
        """Message khác nhau → chữ ký khác nhau"""
        s1 = requests.post(f"{BASE_URL}/api/rsa/sign",
                           json={"message": "Message A"}).json()["signature"]
        s2 = requests.post(f"{BASE_URL}/api/rsa/sign",
                           json={"message": "Message B"}).json()["signature"]
        assert s1 != s2

    def test_sign_short_message(self):
        """Ký message ngắn"""
        res = requests.post(f"{BASE_URL}/api/rsa/sign", json={"message": "A"})
        assert res.status_code == 200
        assert "signature" in res.json()

    def test_sign_message_with_numbers(self):
        """Ký message chứa số"""
        res = requests.post(f"{BASE_URL}/api/rsa/sign",
                            json={"message": "HUTECH 2024"})
        assert res.status_code == 200


class TestRSAVerify:

    def setup_method(self):
        requests.get(f"{BASE_URL}/api/rsa/generate_keys")

    def _sign(self, message):
        return requests.post(f"{BASE_URL}/api/rsa/sign",
                             json={"message": message}).json()["signature"]

    def test_verify_valid_signature_true(self):
        """Chữ ký hợp lệ → is_verified = True"""
        msg = "HUTECH University"
        sig = self._sign(msg)
        res = requests.post(f"{BASE_URL}/api/rsa/verify",
                            json={"message": msg, "signature": sig}).json()
        assert res["is_verified"] is True

    def test_verify_wrong_message_false(self):
        """Message sai → is_verified = False"""
        sig = self._sign("HUTECH University")
        res = requests.post(f"{BASE_URL}/api/rsa/verify",
                            json={"message": "Wrong message",
                                  "signature": sig}).json()
        assert res["is_verified"] is False

    def test_verify_tampered_signature_false(self):
        """Chữ ký bị sửa → is_verified = False"""
        msg = "HUTECH University"
        sig = self._sign(msg)
        tampered = sig[:-4] + "0000"
        res = requests.post(f"{BASE_URL}/api/rsa/verify",
                            json={"message": msg, "signature": tampered}).json()
        assert res["is_verified"] is False

    def test_verify_empty_signature_false(self):
        """Chữ ký giả → is_verified = False"""
        res = requests.post(f"{BASE_URL}/api/rsa/verify",
                            json={"message": "HUTECH", "signature": "00" * 128}).json()
        assert res["is_verified"] is False

    def test_verify_multiple_messages(self):
        """Ký và xác thực nhiều message đều đúng"""
        messages = ["HUTECH", "Python", "RSA Test", "Hello 2024"]
        for msg in messages:
            sig = self._sign(msg)
            res = requests.post(f"{BASE_URL}/api/rsa/verify",
                                json={"message": msg, "signature": sig}).json()
            assert res["is_verified"] is True, f"Failed for: {msg}"

    def test_verify_cross_message_false(self):
        """Chữ ký của message A không xác thực được message B"""
        sig_a = self._sign("Message A")
        res = requests.post(f"{BASE_URL}/api/rsa/verify",
                            json={"message": "Message B", "signature": sig_a}).json()
        assert res["is_verified"] is False

    def test_verify_status_200(self):
        """Verify trả về status 200"""
        msg = "HUTECH"
        sig = self._sign(msg)
        res = requests.post(f"{BASE_URL}/api/rsa/verify",
                            json={"message": msg, "signature": sig})
        assert res.status_code == 200

    def test_verify_signature_from_old_keys_false(self):
        """Chữ ký từ key cũ không hợp lệ sau khi generate key mới"""
        msg = "HUTECH University"
        sig_old = self._sign(msg)
        requests.get(f"{BASE_URL}/api/rsa/generate_keys")  # tạo key mới
        res = requests.post(f"{BASE_URL}/api/rsa/verify",
                            json={"message": msg, "signature": sig_old}).json()
        assert res["is_verified"] is False


# ═══════════════════════════════════════════════════════════
#  ECC TEST CASES
# ═══════════════════════════════════════════════════════════

class TestECCGenerateKeys:

    def test_generate_keys_status_200(self):
        """Tạo khóa ECC trả về 200"""
        res = requests.get(f"{BASE_URL}/api/ecc/generate_keys")
        assert res.status_code == 200

    def test_generate_keys_message(self):
        """Tạo khóa ECC trả về message đúng"""
        res = requests.get(f"{BASE_URL}/api/ecc/generate_keys")
        assert res.json()["message"] == "Keys generated successfully"

    def test_generate_keys_returns_json(self):
        """Response phải là JSON"""
        res = requests.get(f"{BASE_URL}/api/ecc/generate_keys")
        assert res.headers["Content-Type"] == "application/json"

    def test_generate_keys_multiple_times(self):
        """Gọi generate nhiều lần không bị lỗi"""
        for _ in range(3):
            res = requests.get(f"{BASE_URL}/api/ecc/generate_keys")
            assert res.status_code == 200


class TestECCSign:

    def setup_method(self):
        requests.get(f"{BASE_URL}/api/ecc/generate_keys")

    def test_sign_status_200(self):
        """Ký số ECC thành công trả về 200"""
        res = requests.post(f"{BASE_URL}/api/ecc/sign",
                            json={"message": "HUTECH University"})
        assert res.status_code == 200

    def test_sign_has_signature_field(self):
        """Response có field signature"""
        res = requests.post(f"{BASE_URL}/api/ecc/sign",
                            json={"message": "HUTECH University"})
        assert "signature" in res.json()

    def test_sign_returns_valid_hex(self):
        """Chữ ký là chuỗi hex hợp lệ"""
        res = requests.post(f"{BASE_URL}/api/ecc/sign",
                            json={"message": "HUTECH University"})
        sig = res.json()["signature"]
        assert len(sig) > 0
        assert all(c in "0123456789abcdef" for c in sig)

    def test_sign_same_message_different_signature(self):
        """Ký cùng message 2 lần → chữ ký khác nhau (random nonce)"""
        payload = {"message": "HUTECH University"}
        s1 = requests.post(f"{BASE_URL}/api/ecc/sign", json=payload).json()["signature"]
        s2 = requests.post(f"{BASE_URL}/api/ecc/sign", json=payload).json()["signature"]
        assert s1 != s2

    def test_sign_different_messages_different_signatures(self):
        """Message khác nhau → chữ ký khác nhau"""
        s1 = requests.post(f"{BASE_URL}/api/ecc/sign",
                           json={"message": "Message A"}).json()["signature"]
        s2 = requests.post(f"{BASE_URL}/api/ecc/sign",
                           json={"message": "Message B"}).json()["signature"]
        assert s1 != s2

    def test_sign_short_message(self):
        """Ký message ngắn (1 ký tự)"""
        res = requests.post(f"{BASE_URL}/api/ecc/sign", json={"message": "A"})
        assert res.status_code == 200
        assert "signature" in res.json()

    def test_sign_message_with_numbers(self):
        """Ký message chứa số"""
        res = requests.post(f"{BASE_URL}/api/ecc/sign",
                            json={"message": "HUTECH 2024"})
        assert res.status_code == 200

    def test_sign_message_with_special_chars(self):
        """Ký message chứa ký tự đặc biệt"""
        res = requests.post(f"{BASE_URL}/api/ecc/sign",
                            json={"message": "Hello@ECC!"})
        assert res.status_code == 200


class TestECCVerify:

    def setup_method(self):
        requests.get(f"{BASE_URL}/api/ecc/generate_keys")

    def _sign(self, message):
        return requests.post(f"{BASE_URL}/api/ecc/sign",
                             json={"message": message}).json()["signature"]

    def test_verify_valid_signature_true(self):
        """Chữ ký hợp lệ → is_verified = True"""
        msg = "HUTECH University"
        sig = self._sign(msg)
        res = requests.post(f"{BASE_URL}/api/ecc/verify",
                            json={"message": msg, "signature": sig}).json()
        assert res["is_verified"] is True

    def test_verify_wrong_message_false(self):
        """Message sai → is_verified = False"""
        sig = self._sign("HUTECH University")
        res = requests.post(f"{BASE_URL}/api/ecc/verify",
                            json={"message": "Wrong message",
                                  "signature": sig}).json()
        assert res["is_verified"] is False

    def test_verify_tampered_signature_false(self):
        """Chữ ký bị sửa → is_verified = False"""
        msg = "HUTECH University"
        sig = self._sign(msg)
        tampered = sig[:-4] + "0000"
        res = requests.post(f"{BASE_URL}/api/ecc/verify",
                            json={"message": msg, "signature": tampered}).json()
        assert res["is_verified"] is False

    def test_verify_empty_signature_false(self):
        """Chữ ký giả (sai độ dài) → is_verified = False"""
        res = requests.post(f"{BASE_URL}/api/ecc/verify",
                            json={"message": "HUTECH",
                                  "signature": "00" * 48}).json()
        assert res["is_verified"] is False

    def test_verify_status_200(self):
        """Verify trả về status 200"""
        msg = "HUTECH"
        sig = self._sign(msg)
        res = requests.post(f"{BASE_URL}/api/ecc/verify",
                            json={"message": msg, "signature": sig})
        assert res.status_code == 200

    def test_verify_multiple_messages(self):
        """Ký và xác thực nhiều message đều đúng"""
        messages = ["HUTECH", "ECC Test", "Hello 123", "Python ECC"]
        for msg in messages:
            sig = self._sign(msg)
            res = requests.post(f"{BASE_URL}/api/ecc/verify",
                                json={"message": msg, "signature": sig}).json()
            assert res["is_verified"] is True, f"Failed for: {msg}"

    def test_verify_cross_message_false(self):
        """Chữ ký của message A không xác thực được message B"""
        sig_a = self._sign("Message A")
        res = requests.post(f"{BASE_URL}/api/ecc/verify",
                            json={"message": "Message B",
                                  "signature": sig_a}).json()
        assert res["is_verified"] is False

    def test_verify_signature_from_old_keys_false(self):
        """Chữ ký từ bộ key cũ không hợp lệ sau khi generate key mới"""
        msg = "HUTECH University"
        sig_old = self._sign(msg)
        requests.get(f"{BASE_URL}/api/ecc/generate_keys")  # tạo key mới
        res = requests.post(f"{BASE_URL}/api/ecc/verify",
                            json={"message": msg, "signature": sig_old}).json()
        assert res["is_verified"] is False
