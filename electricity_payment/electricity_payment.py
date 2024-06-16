from .schema import VerifyMeterValueSchema, ElectricityPaymentSchema
from vtpass.main import VtPassPythonSDK, jr
import json
import logging
import requests

logger = logging.basicConfig(level=logging.INFO)


class ElectricityPayment(VtPassPythonSDK):
    def verify_meter_value(self, url: str, verify_meter_value: VerifyMeterValueSchema):
        """
        This method is used to verify the meter value of a meter number
        :param serviceId : The service id of the electricity service e.g benin-electric, ikeja-electric
        :param type : The type of meter e.g prepaid, postpaid
        :param billersCode : The meter number you wish to make the bills payment on.
        :return: The response of the transaction
        Error: If there is an error in the request to the API
        it returns the error message
        """
        verify_meter_value_url = f"{url}/merchant-verify"
        headers = self.post_request_headers()
        data = {
            "serviceID": verify_meter_value.service_id,
            "type": verify_meter_value.type,
            "billersCode": verify_meter_value.billers_code,
        }
        try:
            response = requests.post(verify_meter_value_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            result = response.json()
            if "code" in response and response["code"] != "000":
                logging.error(f"An Error Response received: {response}")
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
    
    def electricity_payment(self, url: str, electricity_payment_schema: ElectricityPaymentSchema):
        """
        This method is used to make a electricity payment
        :param serviceID : The service id of the electricity service e.g benin-electric, ikeja-electric
        :param variation_code : The type of meter e.g prepaid, postpaid
        :param billersCode : The meter number you wish to make the bills payment on.
        :param amount : The amount to be paid
        :param phone : The phone number of the customer
        :param request_id : A unique identifier for the request
        :return: The response of the transaction
        Error: If there is an error in the request to the API
        it returns the error message
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
            response = requests.post(electricity_payment_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            result = response.json()
            if "code" in response and response["code"] != "000":
                logging.error(f"An Error Response received: {response}")
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
        