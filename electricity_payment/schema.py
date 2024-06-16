from enum import Enum

from pydantic import BaseModel, Field, field_validator


class ElectricityServiceIdEnum(str, Enum):
    ikeja_electric = ("ikeja-electric",)
    eko_electric = ("eko-electric",)
    abuja_electric = ("abuja-electric",)
    kano_electric = ("kano-electric",)
    portharcourt_electric = ("portharcourt-electric",)
    kaduna_electric = ("kaduna-electric",)
    ibadan_electric = ("ibadan-electric",)
    jos_electric = ("jos-electric",)
    enugu_electric = ("enugu-electric",)
    aba_electric = ("aba-electric",)
    yola_electric = ("yola-electric",)
    benin_electric = ("benin-electric",)


class MeterTypeEnum(str, Enum):
    prepaid = "prepaid"
    postpaid = "postpaid"


class VerifyMeterValueSchema(BaseModel):
    service_id: ElectricityServiceIdEnum = Field(
        ...,
        title="Service ID",
        description="Service ID as specified by VTpass. e.g ikeja-electric, eko-electric, abuja-electric, kano-electric, portharcourt-electric, kaduna-electric, ibadan-electric, jos-electric, enugu-electric, aba-electric, yola-electric, benin-electric",
    )
    type: MeterTypeEnum = Field(
        ..., title="Meter Type", description="The type of meter e.g prepaid, postpaid"
    )
    billers_code: str = Field(
        ...,
        title="Billers Code",
        description="The meter number you wish to make the bills payment on.",
    )

    @field_validator("service_id", "billers_code")
    def not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError("Field cannot be empty")
        return value

    class Config:
        use_enum_values = True


class ElectricityPaymentSchema(BaseModel):
    service_id: ElectricityServiceIdEnum = Field(
        ...,
        title="Service ID",
        description="Service ID as specified by VTpass. e.g ikeja-electric, eko-electric, abuja-electric, kano-electric, portharcourt-electric, kaduna-electric, ibadan-electric, jos-electric, enugu-electric, aba-electric, yola-electric, benin-electric",
    )
    billers_code: str = Field(
        ...,
        title="Billers Code",
        description="The meter number you wish to make the bills payment on.",
    )
    amount: int = Field(
        ...,
        title="Amount",
        description="The amount of the variation (as specified in the GET VARIATIONS endpoint as variation_amount)NOTE: This is optional.If you specify amount, we will topup decoder with the amount. If you do not specify amount, then we will use the price set for the bouquet (as returned in GET VARIATION CODES endpoint)",
    )
    request_id: str = Field(
        ...,
        title="Request ID",
        description="This is a unique reference with which you can use to identify and query the status of a given transaction after the transaction has been executed. it can be generated using the `generate_request_id` method",
    )
    variation_code: MeterTypeEnum = Field(
        ..., title="Meter Type", description="The type of meter e.g prepaid, postpaid"
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

    class Config:
        use_enum_values = True
