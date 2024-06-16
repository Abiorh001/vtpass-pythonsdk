import json
import logging

import requests

from vtpass.main import VtPassPythonSDK, jr

from .schema import (
    EducationalPaymentSchema,
    JambEducationalPaymentSchema,
    VerifyJambProfileSchema,
)

logger = logging.basicConfig(level=logging.INFO)


class EducationalPayment(VtPassPythonSDK):
    """
    A class for handling educational payments via the VtPass API.

    This class provides methods to verify JAMB profiles and process various educational payments.
    It inherits from the VtPassPythonSDK, which provides the base functionality for API interaction.
    """

    def verify_jamb_profile(
        self, url: str, verify_jamb_schema: VerifyJambProfileSchema
    ):
        """
        Verify the JAMB profile of a candidate.

        This method sends a POST request to the VtPass API to verify a JAMB profile using the provided schema.

        :param url: The base URL for the VtPass API.
        :param verify_jamb_schema: An instance of VerifyJambProfileSchema containing the service ID, type, and billers code.
        :return: The response from the API as a dictionary. If the request is successful, the response content is returned.
             In case of an error, the error message is returned.
        """
        verify_jamb_profile_url = f"{url}/merchant-verify"
        headers = self.post_request_headers()
        data = {
            "serviceID": verify_jamb_schema.service_id,
            "type": verify_jamb_schema.type,
            "billersCode": verify_jamb_schema.billers_code,
        }
        try:
            response = requests.post(
                verify_jamb_profile_url, headers=headers, data=json.dumps(data)
            )
            response.raise_for_status()
            result = response.json()
            if "code" in response and response["code"] != "000":
                logging.error(f"An Error Response received: {response}")
                return result
            else:
                logging.info("Jamb profile verified successfully")
                if jr == "True":
                    return result
                else:
                    return result.get("content")
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err} - {response.text}")
            return f"HTTP error occurred: {http_err} - {response.text}"
        except Exception as err:
            logging.error(f"An error occurred: {err}")
            return f"An error occurred: {err}"

    def educational_payment(
        self, url: str, educational_payment_schema: EducationalPaymentSchema
    ):
        """
        Make an educational payment.

        This method sends a POST request to the VtPass API to process an educational payment using the provided schema.

        :param url: The base URL for the VtPass API.
        :param educational_payment_schema: An instance of EducationalPaymentSchema containing service ID, variation code, amount, phone, request ID, and quantity.
        :return: The response from the API as a dictionary. If the request is successful, the response content is returned.
                In case of an error, the error message is returned.
        """
        educational_payment_url = f"{url}/pay"
        headers = self.post_request_headers()
        data = {
            "serviceID": educational_payment_schema.service_id,
            "variation_code": educational_payment_schema.variation_code,
            "amount": educational_payment_schema.amount,
            "phone": educational_payment_schema.phone,
            "request_id": educational_payment_schema.request_id,
            "quantity": educational_payment_schema.quantity,
        }
        try:
            response = requests.post(
                educational_payment_url, headers=headers, data=json.dumps(data)
            )
            response.raise_for_status()
            result = response.json()
            if "code" in result and result["code"] != "000":
                logging.error(f"An Error Response received: {result}")
                return result
            else:
                logging.info("Educational payment successful")
                if jr == "True":
                    return result
                else:
                    return result.get("content")
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err} - {response.text}")
            return f"HTTP error occurred: {http_err} - {response.text}"
        except Exception as err:
            logging.error(f"An error occurred: {err}")

    def jamb_educational_payment(
        self, url: str, jamb_edu_payment_schema: JambEducationalPaymentSchema
    ):
        """
        Make a JAMB educational payment.

        This method sends a POST request to the VtPass API to process a JAMB educational payment using the provided schema.

        :param url: The base URL for the VtPass API.
        :param jamb_edu_payment_schema: An instance of JambEducationalPaymentSchema containing service ID, variation code, amount, phone, request ID, and billers code.
        :return: The response from the API as a dictionary. If the request is successful, the response content is returned.
                In case of an error, the error message is returned.
        """
        jamb_edu_payment_url = f"{url}/pay"
        headers = self.post_request_headers()
        data = {
            "serviceID": jamb_edu_payment_schema.service_id,
            "variation_code": jamb_edu_payment_schema.variation_code,
            "amount": jamb_edu_payment_schema.amount,
            "phone": jamb_edu_payment_schema.phone,
            "request_id": jamb_edu_payment_schema.request_id,
            "billersCode": jamb_edu_payment_schema.billers_code,
        }
        try:
            response = requests.post(
                jamb_edu_payment_url, headers=headers, data=json.dumps(data)
            )
            response.raise_for_status()
            result = response.json()
            if "code" in result and result["code"] != "000":
                logging.error(f"An Error Response received: {result}")
                return result
            else:
                logging.info("Jamb Educational payment successful")
                if jr == "True":
                    return result
                else:
                    return result.get("content")
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err} - {response.text}")
            return f"HTTP error occurred: {http_err} - {response.text}"
        except Exception as err:
            logging.error(f"An error occurred: {err}")
