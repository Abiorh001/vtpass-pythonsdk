import json
import logging
import os
import sys
import uuid
from datetime import datetime

import pytz
import requests
from dotenv import load_dotenv

from vtpass.schema import (
    ProductOptionSchema,
    ServiceIdentifierSchema,
    ServiceIdSchema,
    ServiceIdVariationSchema,
)

logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

# json full response
jr = os.getenv("JSON_RESPONSE")


class VtPassPythonSDK(object):
    """
    VtPassPythonSDK is a Python SDK for interacting with the VtPass API.

    This SDK requires the following environment variables to be set:
    - API_KEY
    - PUBLIC_KEY
    - SECRET_KEY

    The SDK provides methods to interact with the VtPass API to perform the following operations:
    - Get the balance of the wallet associated with the API key
    - Get the all the available service categories
    - Get the details of a service identified by its ID
    - Get the details of a service variation identified by its ID
    - Getting product options for products that have options on the VTpass RESTful API
    - Generate a request ID for a transaction
    - Get the service variation codes for a service variation identified by its ID
    - Get the status of a transaction identified by its request ID
    - Purchase airtime for a phone number
    - Purchase data subscription for a phone number
    - Verify smile email
    - Purchase TV subscription for a smart card number
    - verify smart card number
    - verify meter number
    - Purchase electricity token for a meter number
    - Purchase insurance for a policy number
    - Purchase educational payment e.g jamb, waec
    - verify jamb profile id

    Attributes:
        api_key (str): The API key for authentication.
        public_key (str): The public key for authentication.
        secret_key (str): The secret key for authentication.
    """

    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.public_key = os.getenv("PUBLIC_KEY")
        self.secret_key = os.getenv("SECRET_KEY")
        # Verify if the api_key, public_key and secret_key are set
        self.verify_keys_added()

    def verify_keys_added(self):
        """
        Verify that the necessary API keys are set.

        This method checks if the API key, public key, and secret key are set as environment variables.
        If any of these keys are missing, the program will print an error message and terminate.
        """
        if not self.api_key or not self.public_key or not self.secret_key:
            print(
                "API_KEY, PUBLIC_KEY, SECRET_KEY are required to be set in environment variables"
            )
            sys.exit(1)

    def get_request_headers(self):
        """
        Generate headers for GET requests.

        This method returns the headers required for making GET requests to the VtPass API.

        :return: A dictionary containing the headers.
        """
        return {
            "api-key": self.api_key,
            "public-key": self.public_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def post_request_headers(self):
        """
        Generate headers for POST requests.

        This method returns the headers required for making POST requests to the VtPass API.

        :return: A dictionary containing the headers.
        """
        return {
            "api-key": self.api_key,
            "secret-key": self.secret_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def get_credit_wallet_balance(self, url: str):
        """
        Retrieve the balance of the wallet associated with the API key.

        This method sends a GET request to the provided URL to fetch the credit wallet balance.

        :param url: The base URL for the VtPass API.
        :return: The balance of the wallet if the request is successful.
             In case of an error, it returns the error message.
        """
        balance_url = f"{url}/balance"
        headers = self.get_request_headers()
        try:
            response = requests.get(balance_url, headers=headers)
            response.raise_for_status()
            logging.info("Credit Wallet Balance Retrieved successfully")
            if jr == "False":
                return response.json()
            else:
                return response.json().get("contents").get("balance")
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err} - {response.text}")
            return f"HTTP error occurred: {http_err} - {response.text}"
        except Exception as err:
            logging.error(f"An error occurred: {err}")
            return f"An error occurred: {err}"

    def get_available_service_categories(self, url: str):
        """
        Retrieve all the available service categories.

        This method sends a GET request to the provided URL to fetch the available service categories.

        :param url: The base URL for the VtPass API.
        :return: The available service categories. Each category includes an identifier and name.
                In case of an error, it returns the error message.
        """
        service_categories_url = f"{url}/service-categories"
        headers = self.get_request_headers()
        try:
            response = requests.get(service_categories_url, headers=headers)
            response.raise_for_status()
            logging.info("Available Service Categories Retrieved successfully")
            if jr == "True":
                return response.json()
            else:
                categories = response.json().get("content")
                return categories

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err} - {response.text}")
            return f"HTTP error occurred: {http_err} - {response.text}"
        except Exception as err:
            logging.error(f"An error occurred: {err}")
            return f"An error occurred: {err}"

    def get_service_identify_details(
        self, url: str, identifier_schema: ServiceIdentifierSchema
    ):
        """
        Get the details of a service identified by its ID
        service_identifier: The identifier of the service it is the one that was retrieved from
        the available service categories the key is "identifier" and the value is the what you pass as the identifier

        :return: The details of the service
        serviceID means the service id of the service
        Name means the name of the service
        Error: If there is an error in the request to the API
        it returns the error message
        """
        service_identifier = identifier_schema.identifier
        service_details_url = f"{url}/services?identifier={service_identifier}"
        headers = self.get_request_headers()
        try:
            response = requests.get(service_details_url, headers=headers)
            response.raise_for_status()
            result = response.json()
            if "errors" in result:
                logging.info(f"An Error Response received: {result['errors']}")
                return result
            else:
                logging.info("Service Details Retrieved successfully")
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

    def get_service_variation_details(
        self, url: str, service_id_schema: ServiceIdVariationSchema
    ):
        """
        Get the details of a service variation identified by its ID
        This section contains the recommended flow for getting variation codes for products that have variations on the VTpass RESTful API.

        Variation code are available for some products that have multiple options like (different data plans, different bouquets for CableTV etc).

        This section shows how to get variation codes in a generic form even though you can find something similar on the individual. service details.
        serviceID: The identifier of the service variation it is the one that was retrieved from
        the available service details the key is "serviceID" and the value is the what you pass as the service_id

        :return: The details of the service variation
        Error: If there is an error in the request to the API
        it returns the error message
        """
        service_id = service_id_schema.service_id
        service_variation_details_url = (
            f"{url}/service-variations?serviceID={service_id}"
        )
        headers = self.get_request_headers()
        try:
            response = requests.get(service_variation_details_url, headers=headers)
            response.raise_for_status()
            result = response.json()
            if "errors" in result:
                logging.info(f"An Error Response received: {result['errors']}")
                return result
            else:
                logging.info("Service Variation Details Retrieved successfully")
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

    def get_product_options(
        self, url: str, product_options_schema: ProductOptionSchema
    ):
        """
        getting product options for products that have options on the VTpass RESTful API.
        service_id refers to the serviceID of the product you want to get the options for.
        name: This refers to the option name as specified by VTpass. In this case, it is passenger_type. Other option name include trip_type.

        :return: The details of the service variation
        Error: If there is an error in the request to the API
        it returns the error message
        """
        service_id = product_options_schema.service_id
        name = product_options_schema.name
        product_options_url = f"{url}/options?serviceID={service_id}&name={name}"
        headers = self.get_request_headers()
        try:
            response = requests.get(product_options_url, headers=headers)
            response.raise_for_status()
            result = response.json()
            if "errors" in result:
                logging.error(f"An Error Response received: {result['errors']}")
                return result
            else:
                logging.info("Product Options Retrieved successfully")
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

    def generate_request_id(self):
        """
        Generate a request ID for a transaction
        :return: The request ID
        Error: If there is an error in the request to the API
        it returns the error message
        """
        try:
            timezone = pytz.timezone(os.getenv("TIMEZONE"))
            time_now = datetime.now(timezone)

            # Generate a UUID and remove hyphens
            _id = str(uuid.uuid4()).replace("-", "")

            # Combine the timestamp and UUID to form the request ID
            logging.info("Request ID generated successfully")
            return f"{time_now.strftime('%Y%m%d%H%M')}{_id}"
        except Exception as err:
            logging.error(f"An error occurred: {err}")
            return f"An error occurred: {err}"

    def get_service_variation_codes(self, url: str, service_id_schema: ServiceIdSchema):
        """
        Get the service variation codes for a service variation identified by its ID
        service_id: The identifier of the service variation it is the one that was retrieved from
        the available service details the key is "serviceID" and the value is the what you pass as the service_id

        :return: The service variation codes
        Error: If there is an error in the request to the API
        it returns the error message
        """
        service_id = service_id_schema.service_id
        service_variation_codes_url = f"{url}/service-variations?serviceID={service_id}"
        headers = self.get_request_headers()
        try:
            response = requests.get(service_variation_codes_url, headers=headers)
            response.raise_for_status()
            result = response.json()
            if "errors" in result:
                logging.info(f"An Error Response received: {result['errors']}")
                return result
            else:
                logging.info("Service Variation Codes Retrieved successfully")
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

    def get_transaction_status(self, url: str, request_id: str):
        """
        Get the status of a transaction identified by its request ID
        request_id: The request ID of the transaction

        :return: The status of the transaction
        Error: If there is an error in the request to the API
        it returns the error message
        """
        transaction_status_url = f"{url}/requery"
        headers = self.post_request_headers()
        data = {"request_id": request_id}
        try:
            response = requests.post(
                transaction_status_url, headers=headers, data=json.dumps(data)
            )
            response.raise_for_status()
            result = response.json()
            if "code" in result and result["code"] != "000":
                logging.info(f"An Error Response received: {result}")
                return result
            else:
                logging.info("Transaction Status Retrieved successfully")
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
