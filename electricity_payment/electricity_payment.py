import json
import logging

import requests

from vtpass.main import VtPassPythonSDK, jr

from .schema import ElectricityPaymentSchema, VerifyMeterValueSchema

logger = logging.basicConfig(level=logging.INFO)


class ElectricityPayment(VtPassPythonSDK):
    """
    A class for handling electricity payments via the VtPass API.

    This class provides methods to verify meter values and process electricity payments.
    It inherits from the VtPassPythonSDK, which provides the base functionality for API interaction.
    """

    def verify_meter_value(self, url: str, verify_meter_value: VerifyMeterValueSchema):
        """
        Verify the meter value of a given meter number.

        This method sends a POST request to the VtPass API to verify a meter number using the provided schema.

        :param url: The base URL for the VtPass API.
        :param verify_meter_value: An instance of VerifyMeterValueSchema containing the service ID, type, and billers code.
        :return: The response from the API as a dictionary. If the request is successful, the response content is returned.
                In case of an error, the error message is returned.
        """
        verify_meter_value_url = f"{url}/merchant-verify"
        headers = self.post_request_headers()
        data = {
            "serviceID": verify_meter_value.service_id,
            "type": verify_meter_value.type,
            "billersCode": verify_meter_value.billers_code,
        }
        try:
            response = requests.post(
                verify_meter_value_url, headers=headers, data=json.dumps(data)
            )
            response.raise_for_status()
            result = response.json()
            if "code" in result and result["code"] != "000":
                logging.error(f"An Error Response received: {result}")
                return result
            else:
                logging.info("Meter value verified successfully")
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

    def electricity_payment(
        self, url: str, electricity_payment_schema: ElectricityPaymentSchema
    ):
        """
        Make an electricity payment.

        This method sends a POST request to the VtPass API to process an electricity payment using the provided schema.

        :param url: The base URL for the VtPass API.
        :param electricity_payment_schema: An instance of ElectricityPaymentSchema containing service ID, variation code, billers code, amount, phone, and request ID.
        :return: The response from the API as a dictionary. If the request is successful, the response content is returned.
                In case of an error, the error message is returned.
        """
        electricity_payment_url = f"{url}/pay"
        headers = self.post_request_headers()
        data = {
            "serviceID": electricity_payment_schema.service_id,
            "variation_code": electricity_payment_schema.variation_code,
            "billersCode": electricity_payment_schema.billers_code,
            "amount": electricity_payment_schema.amount,
            "phone": electricity_payment_schema.phone,
            "request_id": electricity_payment_schema.request_id,
        }
        try:
            response = requests.post(
                electricity_payment_url, headers=headers, data=json.dumps(data)
            )
            response.raise_for_status()
            result = response.json()
            if "code" in result and result["code"] != "000":
                logging.error(f"An Error Response received: {result}")
                return result
            else:
                logging.info("Electricity payment successful")
                if jr == "True":
                    return result
                else:
                    return result.get("content")
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err} - {response.text}")
            return f"HTTP error occurred: {http_err} - {response.text}"
        except Exception as err:
            logging.error(f"An error occurred: {err}")
