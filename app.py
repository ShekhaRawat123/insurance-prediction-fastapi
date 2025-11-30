from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, computed_field,Field
from typing import Literal, Annotated
import pandas as pd
import pickle

with open("model.pkl" , "rb" ) as f:
    model = pickle.load(f)
tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

app = FastAPI()
class UserInput(BaseModel):
    age:  Annotated[int , Field(..., gt= 0 ,lt = 120,  description= "enter your age" )]
    weight: Annotated[int, Field(..., gt = 0 , description="enter your  weight" )]
    height: Annotated[int , Field(..., gt = 0 ,description= "enter your height" )]
    income_lpa: Annotated[int, Field(..., gt = 0 , description="enter your salary")]
    smoker: Annotated[bool , Field(..., description="do you  smoke" )]
    city: Annotated[str , Field(... , description = "where is your city")]
    occupation: Annotated[Literal['retired', "freelancer", "student",  'government_job', 'business_owner', 'unemployed', 'private_job'] , Field(..., description= "what is your occupation")]

    @computed_field
    @property
    def bmi(self)-> float:
        return self.weight/(self.height**2)
                 
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi >30 :
            return  "high"
        if self.smoker and self.bmi > 27 :
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> str :
        if self.age < 25 :
            return "young"
        if self.age < 45 :
            return "adult"
        if self.age < 60 :
            return "middle age"
        return "senior"

    @computed_field
    @property
    def city_tier(self)-> int:
        if self.city in tier_1_cities:
            return 1
        if self.city in tier_2_cities:
            return 2
        else:
            return 3

@app.post('/predict')
def predict_premium(data: UserInput):
    
    
    input_df = pd.DataFrame([{
   "bmi" :data.bmi,
   "age_group": data.age_group,
   "lifestyle_risk" : data.lifestyle_risk,
   "city_tier": data.city_tier,
   "income_lpa": data.income_lpa,
   "occupation" : data.occupation

    }])
    prediction = model.predict(input_df)[0]
    return JSONResponse(status_code=200, content={'predicted_category': prediction})
