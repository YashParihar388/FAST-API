from pydantic import BaseModel,EmailStr,AnyUrl,Field ,field_validator ,model_validator,computed_field# type:ignore
from typing import List,Dict ,Optional,Annotated

class Patient(BaseModel):
    name : Annotated[str,Field(max_length= 50,title='name of the patients',description='enter the names of the peoples'
                               ,example=['zade','adeline','riley'])]# type: ignore
    linkdin:AnyUrl
    email:EmailStr
    age:int
    weight:float=Field(gt=0,strict=True)
    height:float
    married:Optional[bool] = False
    allergy:List[str]
    contact:Dict[str,str]
    
    @computed_field
    @property
    def bmi(self) -> float:
            return self.weight/self.height**2
        
        
    
    @model_validator(mode='after')
    def validate(cls,model):
        if model.age>60 and 'emergency' not in model.contact:
            raise ValueError('above 60 should have emergency contact')
        return model
    
    @field_validator('email')
    @classmethod
    def check(cls,value):
        valid = ['icic.com','hdfc.com']
        domain =value.split('@')[-1]
        
        if domain not in valid:
            raise ValueError('not a valid domain')
        
        return value
    
    
        
                    
def insert(patient:Patient):
    print(patient.name)
    print(patient.linkdin)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.allergy)
    print(patient.contact)
    print(patient.married)
    print('bmi:',patient.bmi)
    print('inserted')
    

dict = {'name':'ayush','height':'6','linkdin':'https://localhost:8000','email':'abc@hdfc.com','age':61,'weight':40.0,'allergy':['dust','peanut'],'contact':{'num':
    'abc','emergency':'1234'}}

p = Patient(**dict)

insert(p)

