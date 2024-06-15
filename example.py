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

# Load environment variables from .env file
load_dotenv()

sandbox_url = os.getenv('Sandbox_URL')
live_url = os.getenv('Live_URL')


# get wallet balance
balance = vtPass.get_credit_wallet_balance(sandbox_url)
print(balance)

# get available service categories
service_categories = vtPass.get_available_service_categories(sandbox_url)
try:
    # if json response is False
    for category in service_categories:
        print(f"Identifier: {category.get('identifier')}, Name: {category.get('name')}")
except Exception:
    # if json response is True
    print(service_categories)

# get available service details
identifier = ServiceIdentifierSchema(identifier="insurance")
service_details = vtPass.get_service_identify_details(sandbox_url, identifier)
try:
    # if json response is False
    for detail in service_details:
        print(f"Service Id: {detail.get('serviceID')}, Name: {detail.get('name')}")
except Exception:
    # if json response is True
    print(service_details)

# get service variation details
service_id = ServiceIdVariationSchema(service_id="airtel-data")
service_variation_detials = vtPass.get_service_variation_details(sandbox_url, service_id)
print(service_variation_detials)

# get product options
product_option_schema = ProductOptionSchema(
    service_id="ui-insure",
    name="Third Party Motor Insurance - Universal Insurance"
)
service_product_options = vtPass.get_product_options(sandbox_url, product_option_schema)
print(service_product_options)

# generate request id
request_id = vtPass.generate_request_id()
print(request_id)

# purchase airtime
airtime_schema = AirtimeSchema(
    service_id="etisalat",
    phone_number="08011111111",
    amount=2000,
    request_id=request_id
)
purchase_airtime = vtpass_airtime.purchase_airtime(sandbox_url, airtime_schema=airtime_schema)
print(purchase_airtime)

# get service variation code
service_id = ServiceIdSchema(service_id="spectranet")
service_variation_code = vtPass.get_service_variation_codes(sandbox_url, service_id)
print(service_variation_code)


verify smile email address:
verify_smile_schema = VerifySmileEmailSchema(
    billers_code="tester@sandbox.com",
    service_id="smile-direct"
)
vtpass_smile_email_verify = vtpass_data_subscription.verify_smile_email(sandbox_url, verify_smile_schema)
print(vtpass_smile_email_verify)


# buy data subscription
data_sub_schema = DataSubscriptionSchema(
    service_id="spectranet",
    variation_code="vt-5000",
    request_id=request_id,
    phone="08011111111",
    billers_code="1212121212",
    
)
data_subscription = vtpass_data_subscription.purchase_data_susbscription(sandbox_url, data_sub_schema)
print(data_subscription)


