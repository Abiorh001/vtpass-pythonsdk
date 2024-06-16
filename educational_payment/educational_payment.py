from .schema import VerifyJambProfileSchema, EducationalPaymentSchema
from vtpass.main import VtPassPythonSDK, jr
import json
import logging
import requests

logger = logging.basicConfig(level=logging.INFO)


class EducationalPayment(VtPassPythonSDK):
    def verify_jamb_profile(self, url: str, verify_jamb_schema: VerifyJambProfileSchema):
        """
        This method is used to verify the jamb profile of a jamb candidate
        :param serviceID : The service id of the jamb service e.g jamb-smart
        :param billersCode : The Profile ID number you wish to make payment on.
        :param type : The code of the variation as specified in the GET VARIATIONS method as variation_code.
        :return: The response of the transaction
        Error: If there is an error in the request to the API
        it returns the error message
        """
        verify_jamb_profile_url = f"{url}/merchant-verify"
        headers = self.post_request_headers()
        data = {
            "serviceID": verify_jamb_schema.service_id,
            "type": verify_jamb_schema.type,
            "billersCode": verify_jamb_schema.billers_code,
        }
        try:
            response = requests.post(verify_jamb_profile_url, headers=headers, data=json.dumps(data))
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
    
    def educational_payment(self, url: str, educational_payment_schema: EducationalPaymentSchema):
        """
        This method is used to make a educational payment
        :param serviceID : The service id of the educational service e.g jamb-smart
        :param billersCode : The Profile ID number you wish to make payment on.
        :param amount : The amount of the variation (as specified in the GET VARIATIONS endpoint as variation_amount)
            This amount will be ignored as the variation code determine the price of the data bundle.
        :param phone : The phone number of the customer
        :param request_id : A unique identifier for the request
        :param quantity : The quantity of the result checker PIN you wish to purchase.
            This quantity will be defaulted to 1 if it is not passed in your request
        :param variation_code : The code of the variation (as specified in the GET VARIATIONS method as variation_code).
        :return: The response of the transaction
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
            "billersCode": educational_payment_schema.billers_code,
        }
        try:
            response = requests.post(educational_payment_url, headers=headers, data=json.dumps(data))
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
        