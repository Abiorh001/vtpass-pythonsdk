# VTPass Python SDK

This repository provides the VTPass Python SDK to interact with various services provided by VTPass. The SDK allows you to perform operations such as checking wallet balance, purchasing airtime, and subscribing to data services.

## Prerequisites

- Python 3.7 or higher
- `vtpass` package
- `python-dotenv` package
- VTPass API Key
- VTPass Public Key
- VTPass Secret Key

## Installation

First, clone the repository and navigate to the project directory:

```sh
git clone https://github.com/yourusername/vtpass-pythonsdk.git
cd vtpass-pythonsdk
```

Then, install the required packages or skipp if you have already installed the vtpass-python-sdk package:

```sh
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root of your project directory and add the following environment variables:

```plaintext
API_KEY=your_api_key
PUBLIC_KEY=your_public_key
SECRET_KEY=your_secret_key
TIMEZONE=Africa/Lagos
JSON_RESPONSE=False # Set to True to return JSON response which is useful 
Sandbox_URL=https://sandbox.vtpass.com/api
Live_URL=https://live.vtpass.com/api
```

## Usage

### Import Required Modules

```python
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
```

### Get Wallet Balance

```python
# Get wallet balance
balance = vtPass.get_credit_wallet_balance(sandbox_url)
print(balance)
```

### Get Available Service Categories

```python
# Get available service categories
service_categories = vtPass.get_available_service_categories(sandbox_url)
try:
    # If JSON response is False
    for category in service_categories:
        print(f"Identifier: {category.get('identifier')}, Name: {category.get('name')}")
except Exception:
    # If JSON response is True
    print(service_categories)
```

### Get Available Service Details

```python
# Get available service details
identifier = ServiceIdentifierSchema(identifier="insurance")
service_details = vtPass.get_service_identify_details(sandbox_url, identifier)
try:
    # If JSON response is False
    for detail in service_details:
        print(f"Service Id: {detail.get('serviceID')}, Name: {detail.get('name')}")
except Exception:
    # If JSON response is True
    print(service_details)
```

### Get Service Variation Details

```python
# Get service variation details
service_id = ServiceIdVariationSchema(service_id="airtel-data")
service_variation_details = vtPass.get_service_variation_details(sandbox_url, service_id)
print(service_variation_details)
```

### Get Product Options

```python
# Get product options
product_option_schema = ProductOptionSchema(
    service_id="ui-insure",
    name="Third Party Motor Insurance - Universal Insurance"
)
service_product_options = vtPass.get_product_options(sandbox_url, product_option_schema)
print(service_product_options)
```

### Generate Request ID

```python
# Generate request ID
request_id = vtPass.generate_request_id()
print(request_id)
```

### Purchase Airtime

```python
# Purchase airtime
airtime_schema = AirtimeSchema(
    service_id="etisalat",
    phone_number="08011111111",
    amount=2000,
    request_id=request_id
)
purchase_airtime = vtpass_airtime.purchase_airtime(sandbox_url, airtime_schema=airtime_schema)
print(purchase_airtime)
```

### Get Service Variation Code

```python
# Get service variation code
service_id = ServiceIdSchema(service_id="spectranet")
service_variation_code = vtPass.get_service_variation_codes(sandbox_url, service_id)
print(service_variation_code)
```

### Verify Smile Email Address

```python
# Verify Smile email address
verify_smile_schema = VerifySmileEmailSchema(
    billers_code="tester@sandbox.com",
    service_id="smile-direct"
)
vtpass_smile_email_verify = vtpass_data_subscription.verify_smile_email(sandbox_url, verify_smile_schema)
print(vtpass_smile_email_verify)
```

### Buy Data Subscription

```python
# Buy data subscription
data_sub_schema = DataSubscriptionSchema(
    service_id="spectranet",
    variation_code="vt-5000",
    request_id=request_id,
    phone="08011111111",
    billers_code="1212121212",
)
data_subscription = vtpass_data_subscription.purchase_data_susbscription(sandbox_url, data_sub_schema)
print(data_subscription)
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Please feel free to submit issues, fork the repository and send pull requests!

---

This README provides a comprehensive guide on how to use the VTPass Python SDK with detailed examples. You can also check the [official documentation](https://www.vtpass.com/documentation/) for more information.