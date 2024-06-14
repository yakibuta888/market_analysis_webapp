# tests/domain/services/test_email_service.py
import pytest
import requests
import requests_mock
from unittest.mock import patch, Mock

from src.domain.services.email_service import EmailService

GAS_URL = "http://mock-gas-url.com"

@pytest.fixture
def email_service():
    return EmailService(gas_url=GAS_URL)

def test_send_verification_email_success(email_service: EmailService):
    with requests_mock.Mocker() as mock:
        mock.post(GAS_URL, status_code=200)

        action = "sendVerificationEmail"
        email = "test@example.com"
        token = "sample_token"

        email_service.send_verification_email(email, token)

        assert mock.called
        assert mock.call_count == 1
        request = mock.request_history[0]
        assert request.json() == {"action": action, "email": email, "token": token}


def test_send_verification_email_retries(email_service: EmailService):
    email = "test@example.com"
    token = "testtoken"

    # Mock requests.post to always raise a RequestException
    with patch('requests.post', side_effect=requests.exceptions.RequestException) as mock_post:
        with pytest.raises(Exception, match="Failed to send verification email"):
            email_service.send_verification_email(email, token)

        # Assert that requests.post was called 3 times due to retries
        assert mock_post.call_count == 3


def test_send_verification_email_success_after_retries(email_service: EmailService):
    action = "sendVerificationEmail"
    email = "test@example.com"
    token = "testtoken"

    # Create a mock response that will fail the first two times and succeed the third time
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = [requests.exceptions.RequestException, requests.exceptions.RequestException, None]

    with patch('requests.post', return_value=mock_response) as mock_post:
        email_service.send_verification_email(email, token)

        # Assert that requests.post was called 3 times due to retries
        assert mock_post.call_count == 3
        request = mock_post.call_args_list[2]
        assert request[1]['json'] == {"action": action, "email": email, "token": token}
