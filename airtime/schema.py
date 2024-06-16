from enum import Enum

from pydantic import BaseModel, Field, field_validator


class AirTimeServiceIdEnum(str, Enum):
    mtn = "mtn"
    glo = "glo"
    airtel = "airtel"
    etisalat = "etisalat"
    foreign_airtime = "foreign-airtime"


class AirTimeServiceIdSchema(BaseModel):
    service_id: AirTimeServiceIdEnum = Field(
        ...,
        title="Service ID",
        description="The service id of the service e.g mtn, glo, airtel, etisalat, dstv, gotv, startimes, airtel, smile, spectranet",
    )

    class Config:
        use_enum_values = True


class AirtimeSchema(BaseModel):
    service_id: AirTimeServiceIdEnum = Field(
        ...,
        title="Service ID",
        description="The service id of the airtime service e.g mtn, glo, airtel, etisalat",
    )
    phone_number: str = Field(
        ..., title="Phone Number", description="The phone number to recharge"
    )
    amount: int = Field(..., title="Amount", description="The amount to recharge")
    request_id: str = Field(
        ...,
        title="Request ID",
        description="This is a unique reference with which you can use to identify and query the status of a given transaction after the transaction has been executed. it can be generated using the `generate_request_id` method",
    )

    class Config:
        use_enum_values = True

    @field_validator("phone_number", "request_id")
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
