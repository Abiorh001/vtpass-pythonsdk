import json
import logging

import requests

from airtime.schema import AirtimeSchema
from vtpass.main import VtPassPythonSDK, jr

logging.basicConfig(level=logging.INFO)

# NOTE: "International Airtime is not done yet will be available soon"


class Airtime(VtPassPythonSDK):
    """
    A class for handling airtime purchases via the VtPass API.

    This class provides a method to purchase airtime for a specified phone number.
    It inherits from the VtPassPythonSDK, which provides the base functionality for API interaction.
    """

    def purchase_airtime(self, url, airtime_schema: AirtimeSchema):
        """
        Purchase airtime for a phone number.

        This method sends a POST request to the VtPass API to purchase airtime using the provided schema.

        :param url: The base URL for the VtPass API.
        :param airtime_schema: An instance of AirtimeSchema containing the request ID, service ID, amount, and phone number.
        :return: The response from the API as a dictionary. If the request is successful, the response content is returned.
                In case of an error, the error message is returned.
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
            response = requests.post(
                purchase_airtime_url, headers=headers, data=json.dumps(data)
            )
            response.raise_for_status()
            result = response.json()

            if "code" in result and result["code"] != "000":
                logging.error(f"An Error Response received: {response.json()}")
                return response.json()
            else:
                logging.info("Airtime purchased successfully")
                logging.debug(
                    f"Airtime purchased successfully for {airtime_schema.phone_number}"
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
