from pydantic import BaseModel,EmailStr,AnyUrl,Field ,field_validator # type:ignore
from typing import List,Dict ,Optional,Annotated

class Patient(BaseModel):
    name : Annotated[str,Field(max_length= 50,title='name of the patients',description='enter the names of the peoples'
                               ,example=['zade','adeline','riley'])]# type: ignore
    linkdin:AnyUrl
    email:EmailStr
    age:int
    weight:float=Field(gt=0,strict=True)
    married:Optional[bool] = False
    allergy:List[str]
    contact:Dict[str,str]
    
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
    print('inserted')
    

dict = {'name':'ayush','linkdin':'https://localhost:8000','email':'abc@hdfc.com','age':30,'weight':40.0,'allergy':['dust','peanut'],'contact':{'num':
    'abc'}}

p = Patient(**dict)

insert(p)

