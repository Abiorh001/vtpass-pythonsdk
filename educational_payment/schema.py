from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class EducationalServiceIdEnum(str, Enum):
    waec = "waec"
    waec_registration = "waec-registration"
    jamb = "jamb"


class VerifyJambProfileSchema(BaseModel):
    service_id: EducationalServiceIdEnum = Field(
        ...,
        title="Service ID",
        description="Service ID as specified by VTpass. e.g waec, waec-registration, jamb",
    )
    type: str = Field(
        ...,
        title="Type",
        description="The code of the variation as specified in the GET VARIATIONS endpoint as variation_code",
    )
    billers_code: str = Field(
        ...,
        title="Billers Code",
        description="The Profile ID number you wish to make payment on.",
    )

    @field_validator("service_id", "billers_code", "type")
    def not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError("Field cannot be empty")
        return value

    class Config:
        use_enum_values = True


class EducationalPaymentSchema(BaseModel):
    service_id: EducationalServiceIdEnum = Field(
        ...,
        title="Service ID",
        description="Service ID as specified by VTpass. e.g waec, waec-registration, jamb",
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
        description="The code of the variation  as specified in the GET VARIATIONS endpoint as variation_code",
    )
    phone: str = Field(
        ...,
        title="Phone Number",
        description="The phone number of the customer or recipient of this service",
    )
    quantity: Optional[int] = Field(
        None,
        title="Quantity",
        description="The quantity of the result checker PIN you wish to purchase.This quantity will be defaulted to 1 if it is not passed in your request",
    )

    @field_validator("service_id", "phone", "request_id", "variation_code")
    def not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError("Field cannot be empty")
        return value

    @field_validator("amount", "quantity")
    def positive(cls, value):
        if value <= 0 or value > 100000:
            raise ValueError(
                "Amount must be positive and greater than 0 and less than or equal 100000"
            )
        return value

    class Config:
        use_enum_values = True


class JambEducationalPaymentSchema(BaseModel):
    service_id: EducationalServiceIdEnum = Field(
        ...,
        title="Service ID",
        description="Service ID as specified by VTpass. e.g waec, waec-registration, jamb",
    )
    billers_code: str = Field(
        ...,
        title="Billers Code",
        description="The Profile ID you wish to make the payment on",
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
        description="The code of the variation  as specified in the GET VARIATIONS endpoint as variation_code",
    )
    phone: str = Field(
        ...,
        title="Phone Number",
        description="The phone number of the customer or recipient of this service",
    )

    @field_validator(
        "service_id", "phone", "request_id", "variation_code", "billers_code"
    )
    def not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError("Field cannot be empty")
        return value

    @field_validator("amount")
    def positive(cls, value):
        if value <= 0 or value > 100000:
            raise ValueError(
                "Amount must be positive and greater than 0 and less than or equal 100000"
            )
        return value

    class Config:
        use_enum_values = True
