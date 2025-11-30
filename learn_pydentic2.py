from pydantic import BaseModel, EmailStr, Field , model_validator
from typing import List, Dict, Optional,Annotated


class Patient(BaseModel):
    name: str
    email:EmailStr
    age: int 
    weight: float  
    married: bool
    allergies: Optional[List[str]] = None
    contact_detail: Dict[str , str]
    
    @model_validator(mode = 'after') 
    def validate_emergency_contact(cls, model):
        if model.age > 60 and "emergency" not in model.contact_detail:
            raise ValueError('emergency number should be in')
        return model
    

def insert_patient_data(patient:Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    
    
Patient_info = { "name" : "mohan" , 'age' :  45, 'weight': 65.4 , 'married': True , "email" : "abc@gmail.com",'contact_detail': { "mobile": "975632089"}
}
patient = Patient(**Patient_info)

insert_patient_data(patient)