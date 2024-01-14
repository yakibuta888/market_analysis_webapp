import pytest

from src.domain.value_objects.email import Email


class TestEmail:

    def test_create_email_with_valid_address(self):
        # 有効なメールアドレスでEmailオブジェクトを作成
        email_address = "example@example.com"
        email = Email(email_address)
        assert email.email == email_address

    def test_create_email_with_invalid_address_raises_error(self):
        # 無効なメールアドレスでEmailオブジェクトを作成しようとするとエラー
        invalid_email_address = "example"
        with pytest.raises(ValueError) as exc_info:
            Email(invalid_email_address)
        assert "無効なメールアドレスです。" in str(exc_info.value)

    def test_email_equality(self):
        # 同じメールアドレスのEmailオブジェクトは等価であるべき
        email_address = "example@example.com"
        email1 = Email(email_address)
        email2 = Email(email_address)
        assert email1 == email2
