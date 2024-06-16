from vtpass.main import VtPassPythonSDK, jr
from .schema import TVSubscriptionSchema, VerifySmartCardNumberSchema
import requests
import json
import logging


logging.basicConfig(level=logging.INFO)


class TVSubscription(VtPassPythonSDK):
    def tv_susbscription(self, url: str, tv_sub_schema: TVSubscriptionSchema):
        """
            Purchase TV subscription for a smart card number

            :param serviceID: The service id of the TV subscription service e.g dstv, gotv, startimes
            :param phone: The phone number of the customer or recipient of this service
            :param amount: The amount of TV subscription to purchase specify by the variation code. If you specify amount, we will topup decoder with the amount. If you do not specify amount, then we will use the price set for the bouquet.
            :param request_id: This is a unique reference with which you can use to identify and query the status of a given transaction after the transaction has been executed.
            :param billersCode: The smart card number you wish to make the Subscription payment on
            :param variation_code: The variation code of the service e.g dstv-1, dstv-2           
            :param subscription_type: The type of subscription. for a new or exisiting customer that want to change their subscription this will be change. for an exisiting customer that want
            to renew their subscription this will be renew.
            : param quanntity: The number of months viewing month e.g 1. it can be optional if no quantity is specified it will be set to 1

            :return: The response of the transaction
            Error: If there is an error in the request to the API
            it returns the error message
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
            "quantity": tv_sub_schema.quantity
        }
        try:
            print(data)
            tv_subscription_url = f"{url}/pay"
            response = requests.post(tv_subscription_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            result = response.json()
           
            if "code" in result and result["code"] != "000":
                logging.error(f"An Error Response received: {response.json()}")
                return response.json()
            else:
                logging.info("TV Subscription purchased successfully")
                logging.debug(f"TV Subscription purchased successfully for {tv_sub_schema.billers_code}")
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
    
    def verify_smart_card_number(self, url: str, verify_smart_card: VerifySmartCardNumberSchema):
        """
            Verify smart card number for a TV subscription

            :param billersCode: The smart card number you wish to make the Subscription payment on.
            :param serviceID: The service id of the data subscription service e.g dstv

            :return: The response of the transaction
            Error: If there is an error in the request to the API
            it returns the error message
        """
        
        verify_smart_card_url = f"{url}/merchant-verify"
        headers = self.post_request_headers()
        data = {
            "serviceID": verify_smart_card.service_id,
            "billersCode": verify_smart_card.billers_code,
        }
        try:
            response = requests.post(verify_smart_card_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            result = response.json()
           
            if "code" in result and result["code"] != "000":
                logging.error(f"An Error Response received: {response.json()}")
                return response.json()
            else:
                logging.info("Smart Card Number verified successfully")
                logging.debug(f"Smart Card Number verified successfully for {verify_smart_card.billers_code}")
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