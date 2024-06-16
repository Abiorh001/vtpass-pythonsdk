import json
import logging

import requests

from vtpass.main import VtPassPythonSDK, jr

from .schema import TVSubscriptionSchema, VerifySmartCardNumberSchema

logging.basicConfig(level=logging.INFO)


class TVSubscription(VtPassPythonSDK):
    """
    A class for handling TV subscription payments via the VtPass API.

    This class provides methods to verify smart card numbers and process TV subscription payments.
    It inherits from the VtPassPythonSDK, which provides the base functionality for API interaction.
    """

    def tv_susbscription(self, url: str, tv_sub_schema: TVSubscriptionSchema):
        """
        Purchase a TV subscription for a smart card number.

        This method sends a POST request to the VtPass API to process a TV subscription using the provided schema.

        :param url: The base URL for the VtPass API.
        :param tv_sub_schema: An instance of TVSubscriptionSchema containing the request ID, service ID, amount, phone, billers code, variation code, subscription type, and quantity.
        :return: The response from the API as a dictionary. If the request is successful, the response content is returned.
                In case of an error, the error message is returned.
        """
        tv_subscription_url = f"{url}/pay"
        headers = self.post_request_headers()
        data = {
            "request_id": tv_sub_schema.request_id,
            "serviceID": tv_sub_schema.service_id,
            "amount": tv_sub_schema.amount,
            "phone": tv_sub_schema.phone,
            "billersCode": tv_sub_schema.billers_code,
            "variation_code": tv_sub_schema.variation_code,
            "subscription_type": tv_sub_schema.subscription_type,
            "quantity": tv_sub_schema.quantity,
        }
        try:
            print(data)
            tv_subscription_url = f"{url}/pay"
            response = requests.post(
                tv_subscription_url, headers=headers, data=json.dumps(data)
            )
            response.raise_for_status()
            result = response.json()

            if "code" in result and result["code"] != "000":
                logging.error(f"An Error Response received: {response.json()}")
                return response.json()
            else:
                logging.info("TV Subscription purchased successfully")
                logging.debug(
                    f"TV Subscription purchased successfully for {tv_sub_schema.billers_code}"
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

    def verify_smart_card_number(
        self, url: str, verify_smart_card: VerifySmartCardNumberSchema
    ):
        """
        Verify a smart card number for a TV subscription.

        This method sends a POST request to the VtPass API to verify a smart card number using the provided schema.

        :param url: The base URL for the VtPass API.
        :param verify_smart_card: An instance of VerifySmartCardNumberSchema containing the service ID and billers code.
        :return: The response from the API as a dictionary. If the request is successful, the response content is returned.
                In case of an error, the error message is returned.
        """

        verify_smart_card_url = f"{url}/merchant-verify"
        headers = self.post_request_headers()
        data = {
            "serviceID": verify_smart_card.service_id,
            "billersCode": verify_smart_card.billers_code,
        }
        try:
            response = requests.post(
                verify_smart_card_url, headers=headers, data=json.dumps(data)
            )
            response.raise_for_status()
            result = response.json()

            if "code" in result and result["code"] != "000":
                logging.error(f"An Error Response received: {response.json()}")
                return response.json()
            else:
                logging.info("Smart Card Number verified successfully")
                logging.debug(
                    f"Smart Card Number verified successfully for {verify_smart_card.billers_code}"
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
