from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class SubscriptionTypeEnum(str, Enum):
    change = "change"
    renew = "renew"


class TVSubscriptionSchema(BaseModel):
    service_id: str = Field(
        ...,
        title="Service ID",
        description="Service ID as specified by VTpass. e.g mtn-data, smile-direct",
    )
    billers_code: str = Field(
        ...,
        title="Smart Card Number",
        description="The smart card number you wish to make the Subscription payment on",
    )
    amount: Optional[int] = Field(
        None,
        title="Amount",
        description="The amount of the variation (as specified in the GET VARIATIONS endpoint as variation_amount)NOTE: This is optional.If you specify amount, we will topup decoder with the amount. If you do not specify amount, then we will use the price set for the bouquet (as returned in GET VARIATION CODES endpoint)",
    )
    request_id: str = Field(
        ...,
        title="Request ID",
        description="This is a unique reference with which you can use to identify and query the status of a given transaction after the transaction has been executed. it can be generated using the `generate_request_id` method",
    )
    variation_code: str = Field(
        ...,
        title="Variation Code",
        description="The variation code of the service e.g 30-days, 1-month, 3-months, 6-months, 1-year, 1-day, 7-days, 14-days, 21-days, 28-days, 30-days, 60-days, 90-days, 180-days, 365-days, 1-week, 2-weeks, 3-weeks, 4-weeks, 1-month, 2-months, 3-months, 6-months, 1-year",
    )
    phone: str = Field(
        ...,
        title="Phone Number",
        description="The phone number of the customer or recipient of this service",
    )
    subscription_type: Optional[SubscriptionTypeEnum] = Field(
        None,
        title="Subscription Type",
        description="The type of subscription in this case change.",
    )
    quantity: Optional[int] = Field(
        None, title="Quantity", description="The number of months viewing month e.g 1"
    )

    @field_validator(
        "service_id", "phone", "request_id", "variation_code", "billers_code"
    )
    def not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError("Field cannot be empty")
        return value

    class Config:
        use_enum_values = True


class VerifySmartCardNumberSchema(BaseModel):
    service_id: str = Field(
        ...,
        title="Service ID",
        description="Service ID as specified by VTpass. e.g dstv",
    )
    billers_code: str = Field(
        ..., title="The smart card number you wish to make the Subscription payment on"
    )

    @field_validator("service_id", "billers_code")
    def not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError("Field cannot be empty")
        return value
