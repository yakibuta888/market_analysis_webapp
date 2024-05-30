# src/domain/services/email_service.py
import requests

from time import sleep

from src.settings import logger


class EmailService:
    def __init__(self, gas_url: str, max_retries: int = 3, retry_interval: int = 5):
        self.gas_url = gas_url
        self.max_retries = max_retries
        self.retry_interval = retry_interval


    def send_verification_email(self, email: str, token: str) -> None:
        payload = {
            "action": "sendVerificationEmail",
            "email": email,
            "token": token
        }
        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.post(self.gas_url, json=payload)
                logger.info(f'response: {response.text}')
                response.raise_for_status()
                logger.info(f"Verification email sent to {email}. token: {token}")
                return
            except requests.exceptions.RequestException as e:
                retries += 1
                logger.error(f"Failed to send verification email:{email} detail:{e}")
                if retries >= self.max_retries:
                    raise Exception(f"Failed to send verification email after {self.max_retries} attempts: {e}")
                sleep(self.retry_interval)
