from vtpass import vtPass
from airtime import vtpass_airtime
from dotenv import load_dotenv
import os
from airtime.schema import AirtimeSchema
from data_subscription.schema import DataSubscriptionSchema, VerifySmileEmailSchema
from data_subscription import vtpass_data_subscription
from vtpass.schema import (
    ServiceIdentifierSchema,
    ServiceIdVariationSchema,
    ProductOptionSchema,
    ServiceIdSchema,
)
from tv_subscriptions import vtpass_tv_subscription
from tv_subscriptions.schema import TVSubscriptionSchema
from electricity_payment.schema import VerifyMeterValueSchema, ElectricityPaymentSchema
from electricity_payment import vtpass_electricity_payment

# Load environment variables from .env file
load_dotenv()

sandbox_url = os.getenv('Sandbox_URL')
live_url = os.getenv('Live_URL')


# get wallet balance
# balance = vtPass.get_credit_wallet_balance(sandbox_url)
# print(balance)

# get available service categories
# service_categories = vtPass.get_available_service_categories(sandbox_url)
# try:
#     # if json response is False
#     for category in service_categories:
#         print(f"Identifier: {category.get('identifier')}, Name: {category.get('name')}")
# except Exception:
#     # if json response is True
#     print(service_categories)

# # get available service details
# identifier = ServiceIdentifierSchema(identifier="insurance")
# service_details = vtPass.get_service_identify_details(sandbox_url, identifier)
# try:
#     # if json response is False
#     for detail in service_details:
#         print(f"Service Id: {detail.get('serviceID')}, Name: {detail.get('name')}")
# except Exception:
#     # if json response is True
#     print(service_details)

# # get service variation details
# service_id = ServiceIdVariationSchema(service_id="airtel-data")
# service_variation_detials = vtPass.get_service_variation_details(sandbox_url, service_id)
# print(service_variation_detials)

# # get product options
# product_option_schema = ProductOptionSchema(
#     service_id="ui-insure",
#     name="Third Party Motor Insurance - Universal Insurance"
# )
# service_product_options = vtPass.get_product_options(sandbox_url, product_option_schema)
# print(service_product_options)

# # generate request id
request_id = vtPass.generate_request_id()
# print(request_id)

# # purchase airtime
# airtime_schema = AirtimeSchema(
#     service_id="etisalat",
#     phone_number="08011111111",
#     amount=2000,
#     request_id=request_id
# )
# purchase_airtime = vtpass_airtime.purchase_airtime(sandbox_url, airtime_schema=airtime_schema)
# print(purchase_airtime)

# # get service variation code
# service_id = ServiceIdSchema(service_id="showmax")
# service_variation_code = vtPass.get_service_variation_codes(sandbox_url, service_id)
# print(service_variation_code)


# verify smile email address:
# verify_smile_schema = VerifySmileEmailSchema(
#     billers_code="tester@sandbox.com",
#     service_id="smile-direct"
# )
# vtpass_smile_email_verify = vtpass_data_subscription.verify_smile_email(sandbox_url, verify_smile_schema)
# print(vtpass_smile_email_verify)


# # buy data subscription
# data_sub_schema = DataSubscriptionSchema(
#     service_id="spectranet",
#     variation_code="vt-5000",
#     request_id=request_id,
#     phone="08011111111",
#     billers_code="1212121212",
    
# )
# data_subscription = vtpass_data_subscription.purchase_data_susbscription(sandbox_url, data_sub_schema)
# print(data_subscription)


# verify smart card number
# verify_smart_card_schema = VerifySmileEmailSchema(
#     billers_code="1212121212",
#     service_id="dstv"
# )
# vtpass_verify_smart_card = vtpass_tv_subscription.verify_smart_card_number(sandbox_url, verify_smart_card_schema)
# print(vtpass_verify_smart_card)

# buy tv subscription
# tv_sub_schema = TVSubscriptionSchema(
#     service_id="showmax",
#     variation_code="full",
#     request_id=request_id,
#     phone="08011111111",
#     billers_code="1212121212",
#     subscription_type="change",
#     amount=1000
    
   
    
# )
# # verify smart card number
# verify_smart_card_schema = VerifySmileEmailSchema(
#     billers_code="1212121212",
#     service_id="showmax"
# )

# # service id for starttimes and showmax
# services_ids = ["startimes", "showmax"]
# vtpass_verify_smart_card = vtpass_tv_subscription.verify_smart_card_number(sandbox_url, verify_smart_card_schema)
# if "error" in vtpass_verify_smart_card:
#     print(vtpass_verify_smart_card)
#     print("smart card number not verified")
# else:
#     # for exisiting customers it uses the Renewwal_Amount as the amount to be paid if the susbscription_type is renew
#     if tv_sub_schema.subscription_type == "renew":
#         tv_sub_schema.amount = vtpass_verify_smart_card.get("Renewal_Amount")
#         tv_sub_schema.quantity = None
#         tv_sub_schema.variation_code = None
    
#     elif tv_sub_schema.service_id in services_ids:
#         tv_sub_schema.subscription_type = None,
#         tv_sub_schema.quantity = None
#     tv_subscription = vtpass_tv_subscription.tv_susbscription(sandbox_url, tv_sub_schema)
#     print(tv_subscription)

# verify meter value
# verify_meter_value = VerifyMeterValueSchema(
#     service_id="ikeja-electric",
#     type="postpaid",
#     billers_code="1010101010101"
# )
# vtpass_verify_meter_value = vtpass_electricity_payment.verify_meter_value(sandbox_url, verify_meter_value)
# print(vtpass_verify_meter_value)


# electricity payment
electricity_payment_schema = ElectricityPaymentSchema(
    service_id="jos-electric",
    variation_code="postpaid",
    billers_code="1010101010101",
    amount=1000,
    request_id=request_id,
    phone="08011111111"
)
verify_meter_value = VerifyMeterValueSchema(
    service_id="jos-electric",
    type="postpaid",
    billers_code="1010101010101"
)
vtpass_verify_meter_value = vtpass_electricity_payment.verify_meter_value(sandbox_url, verify_meter_value)

if "error" in vtpass_verify_meter_value:
    print(vtpass_verify_meter_value)
    print("Meter number not verified")
else:
    electricity_payment = vtpass_electricity_payment.electricity_payment(sandbox_url, electricity_payment_schema)
    print(electricity_payment)