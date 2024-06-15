from vtpass.main import VtPassPythonSDK, jr
import requests
from airtime.schema import AirtimeSchema
import json
import logging


logging.basicConfig(level=logging.INFO)

# NOTE: "International Airtime is not done yet will be available soon"


class Airtime(VtPassPythonSDK):
    def purchase_airtime(self, url, airtime_schema: AirtimeSchema):
        """
            Purchase airtime for a phone number

            :param service_id: The service id of the airtime service e.g mtn, glo, airtel, etisalat
            :param phone_number: The phone number to purchase airtime for
            :param amount: The amount of airtime to purchase
            :param request_id: This is a unique reference with which you can use to identify and query the status of a given transaction after the transaction has been executed.
             it can be geerated using the `generate_request_id` method

            :return: The response of the transaction
            Error: If there is an error in the request to the API
            it returns the error message
        """
        purchase_airtime_url = f"{url}/pay"
        headers = self.post_request_headers()
        data = {
            "request_id": airtime_schema.request_id,
            "serviceID": airtime_schema.service_id,
            "amount": airtime_schema.amount,
            "phone": airtime_schema.phone_number,
        }
        try:
            response = requests.post(purchase_airtime_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            result = response.json()
           
            if "code" in result and result["code"] != "000":
                logging.error(f"An Error Response received: {response.json()}")
                return response.json()
            else:
                logging.info("Airtime purchased successfully")
                logging.debug(f"Airtime purchased successfully for {airtime_schema.phone_number}")
                if jr == "True":
                    return result
                else:
                    return result.get("content")
            
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err} - {response.json()}")
            return f"HTTP error occurred: {http_err} - {response.json()}"
        except Exception as err:
            logging.error(f"An error occurred: {err}")
            return f"An error occurred: {err}"