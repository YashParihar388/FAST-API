from pydantic import BaseModel

class Address(BaseModel):
    house:str
    city:str
    pin:str
    
class Patient(BaseModel):
    id:str
    department:str
    address:Address
addr={'house':'good','city':'agra','pin':'4500'}
b = Address(**addr)

a = {'id':'123','department':'eyes','address':b}

c = Patient(**a)

def details(c):
    print(c.id)
    print(c.address)
    

print(c.model_dump())
print(type(c.model_dump()))