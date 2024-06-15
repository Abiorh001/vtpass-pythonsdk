from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import Optional


class DataSubscriptionSchema(BaseModel):
    service_id: str = Field(..., title="Service ID", description="Service ID as specified by VTpass. e.g mtn-data, smile-direct")
    billers_code: str = Field(..., title="Phone Number", description="This is the phone number or email address if it is for smile-direct on which you want to make the subscription payment. It identifies the subscriber's account.")
    amount: Optional[int] = Field(None, title="Amount", description="This amount will be ignored as the variation code determine the price of the data bundle.")
    request_id: str = Field(..., title="Request ID", description="This is a unique reference with which you can use to identify and query the status of a given transaction after the transaction has been executed. it can be generated using the `generate_request_id` method")
    variation_code: str = Field(..., title="Variation Code", description="The variation code of the service e.g 30-days, 1-month, 3-months, 6-months, 1-year, 1-day, 7-days, 14-days, 21-days, 28-days, 30-days, 60-days, 90-days, 180-days, 365-days, 1-week, 2-weeks, 3-weeks, 4-weeks, 1-month, 2-months, 3-months, 6-months, 1-year")
    phone: str = Field(..., title="Phone Number", description=" This is the phone number of the customer or the recipient who will receive the data subscription. It identifies who the service is being provided to.")
    
    @field_validator('service_id', 'phone',  'request_id', 'variation_code', "billers_code")
    def not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError('Field cannot be empty')
        return value


class VerifySmileEmailSchema(BaseModel):
    service_id: str = Field(..., title="Service ID", description="Service ID as specified by VTpass. e.g smile-direct")
    billers_code: str = Field(..., title="	The smile email you wish to make the Subscription payment on")
    
    @field_validator('service_id', "billers_code")
    def not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError('Field cannot be empty')
        return value