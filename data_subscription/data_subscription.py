import json
import logging

import requests

from vtpass.main import VtPassPythonSDK, jr

from .schema import DataSubscriptionSchema, VerifySmileEmailSchema

logging.basicConfig(level=logging.INFO)


class DataSubscription(VtPassPythonSDK):
    """
        A class for handling data subscription via the VtPass API.

        This class provides a method to purchase data subscription for a specified phone number, and for verifying smile email.
        It inherits from the VtPassPythonSDK, which provides the base functionality for API interaction.
    """
    def purchase_data_susbscription(
        self, url: str, data_sub_schema: DataSubscriptionSchema
    ):
        """
        Purchase data subscription for a phone number

        :param serviceID: The service id of the data subscription service e.g mtn, glo, airtel, etisalat
        :param phone: The phone number to purchase data subscription for
        :param amount: The amount of data subscription to purchase. the amount will be ignored and be determined by the variation_code
        :param request_id: This is a unique reference with which you can use to identify and query the status of a given transaction after the transaction has been executed.
        :param billersCode: The phone number you wish to make the Subscription payment on
        :param variation_code: The variation code of the service e.g airt-50, airt-500
         it can be geerated using the `generate_request_id` method

        :return: The response of the transaction
        Error: If there is an error in the request to the API
        it returns the error message
        """
        purchase_data_subscription_url = f"{url}/pay"
        headers = self.post_request_headers()
        data = {
            "request_id": data_sub_schema.request_id,
            "serviceID": data_sub_schema.service_id,
            "amount": data_sub_schema.amount,
            "phone": data_sub_schema.phone,
            "billersCode": data_sub_schema.billers_code,
            "variation_code": data_sub_schema.variation_code,
        }
        try:
            purchase_data_subscription_url = f"{url}/pay"
            response = requests.post(
                purchase_data_subscription_url, headers=headers, data=json.dumps(data)
            )
            response.raise_for_status()
            result = response.json()

            if "code" in result and result["code"] != "000":
                logging.error(f"An Error Response received: {response.json()}")
                return response.json()
            else:
                logging.info("Data Subscription purchased successfully")
                logging.debug(
                    f"Data Subscription purchased successfully for {data_sub_schema.phone}"
                )
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

    def verify_smile_email(self, url: str, verify_smile_schema: VerifySmileEmailSchema):
        """
        This method allows you to verify the Email before attempting to make payment.

        :param billersCode: The smile email you wish to make the Subscription payment on.
        :param serviceID: The service id of the data subscription service e.g smile-direct

        :return: The response of the transaction
        Error: If there is an error in the request to the API
        it returns the error message
        """

        verify_smile_email_url = f"{url}i/merchant-verify/smile/email"
        headers = self.post_request_headers()
        data = {
            "serviceID": verify_smile_schema.service_id,
            "billersCode": verify_smile_schema.billers_code,
        }
        try:
            response = requests.post(
                verify_smile_email_url, headers=headers, data=json.dumps(data)
            )
            response.raise_for_status()
            result = response.json()

            if "code" in result and result["code"] != "000":
                logging.error(f"An Error Response received: {response.json()}")
                return response.json()
            else:
                logging.info("Email verified successfully")
                logging.debug(f"Email verified successfully for {email}")
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
