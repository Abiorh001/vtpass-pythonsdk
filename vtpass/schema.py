from pydantic import BaseModel, Field, field_validator
from enum import Enum

# NOTE - events is not available for now
class ServiceIdentifierEnum(str, Enum):
    airtime = "airtime"
    data = "data"
    tv_subscription = "tv-subscription"
    electricity_bill = "electricity-bill"
    education = "education"
    funds = "funds"
    # events = "events"
    other_services = "other-services"
    insurance = "insurance"


class ServiceIdSchema(BaseModel):
    service_id: str = Field(..., title="Service ID", description="The service id of the service e.g mtn, glo, airtel, etisalat, dstv, gotv, startimes, airtel, smile, spectranet")
    
    @field_validator('service_id')
    def not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError('Field cannot be empty')
        return value


class ServiceIdentifierSchema(BaseModel):
    identifier: ServiceIdentifierEnum = Field(..., title="Service Identifier", description="The identifier of the service e.g airtime, data, tv-subscription, electricity-bill, education, funds, events, other-services, insurance")
    
    class Config:
        use_enum_values = True


class ServiceIdVariationEnum(str, Enum):
    airtel_data = "airtel-data",
    mtn_data = "mtn-data",
    glo_data = "glo-data",
    etisalat_data = "9mobile-data",
    smile_direct = "smile-direct",
    spectranet = "spectranet",
    _9mobile_sme_data = "9mobile-sme-data",
    waec = "waec",
    waec_registration = "waec-registration",
    jamb = "jamb",
    ikeja_electric = "ikeja-electric",
    eko_electric = "eko-electric",
    abuja_electric = "abuja-electric",
    kano_electric = "kano-electric",
    portharcourt_electric = "portharcourt-electric",
    kaduna_electric = "kaduna-electric",
    ibadan_electric = "ibadan-electric",
    jos_electric = "jos-electric",
    enugu_electric = "enugu-electric",
    aba_electric = "aba-electric",
    yola_electric = "yola-electric",
    benin_electric = "benin-electric",
    bank_deposit = "bank-deposit",
    ui_insure = "ui-insure",
    health_insurance_rhl = "health-insurance-rhl",
    personal_accident_insurance = "personal-accident-insurance",
    home_cover_insurance = "home-cover-insurance",
    web_design_deal = "web-design-deal",
    dstv = "dstv",
    gotv = "gotv",
    startimes = "startimes",
    showmax = "showmax",


class ServiceIdVariationSchema(BaseModel):
    service_id: ServiceIdVariationEnum = Field(..., title="Service ID", description="The service id of the service e.g mtn-data, glo-data, airtel-data, dstv, gotv, startimes, showmax, smile-direct, spectranet, 9mobile-sme-data, waec, waec-registration, jamb, ikeja-electric, eko-electric, abuja-electric, kano-electric, portharcourt-electric, kaduna-electric, ibadan-electric, jos-electric, enugu-electric, aba-electric, yola-electric, benin-electric, bank-deposit, ui-insure, health-insurance-rhl, personal-accident-insurance, home-cover-insurance, web-design-deal")
    
    class Config:
        use_enum_values = True


class ProductOptionSchema(BaseModel):
    name: str = Field(..., title="Name", description="The name of the product option")
    service_id: ServiceIdSchema = Field(..., title="Service ID", description="The service id of the service e.g mtn, glo, airtel, etisalat, dstv, gotv, startimes, airtel, smile, spectranet")

    @field_validator('name', 'service_id')
    def not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError('Field cannot be empty')
        return value