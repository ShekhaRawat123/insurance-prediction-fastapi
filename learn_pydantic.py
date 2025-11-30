from pydantic import BaseModel, EmailStr, Field , field_validator
from typing import List, Dict, Optional,Annotated


class Patient(BaseModel):
    name: Annotated[str, Field(max_length = 50 , title="enter your name" ,description= "enter your name according to   college id")]
    email: EmailStr
    age: int = Field(gt=0, lt= 120)
    weight: float = Field(gt = 0)
    married: bool
    allergies: Optional[List[str]] = None
    contact_detail: Dict[str , str]
    @field_validator('email')
    @classmethod
    def email_validator(cls , value):
        valid_domain = ['hdfc.com', "icic.com"]
        domain_name = value.split("@")[-1]
        if domain_name not in valid_domain :
            raise  ValueError("invalid domain ha bro")
        else:
            return value
    
    @field_validator('name')
    @classmethod
    def name_validator(cls, value):
        return value.upper()
def insert_patient_data(patient:Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    
    
Patient_info = { "name" : "mohan" , 'age' :"80",'weight': 65.4 , 'married': True , "email" : "abc@hdfc.com",'contact_detail': {"mobile":"9743547585"} }
 
patient = Patient(**Patient_info)

insert_patient_data(patient)