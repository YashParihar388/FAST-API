from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
from fastapi.responses import JSONResponse # type:ignore
from fastapi import FastAPI,Path,HTTPException,Query # type:ignore
import json
app = FastAPI()


class Patient(BaseModel):
    id:Annotated[str,Field(...,description='enter patiend id',examples=['P001'])]
    name:Annotated[str,Field(...,description='enter the patient name')]
    city:Annotated[str,Field(...,description='enter name of city')]
    age:Annotated[int,Field(...,gt=0,lt=120,description='enter the age of patient')]
    gender:Annotated[Literal['male','female','other'],Field(...,description='gender of the patient')]
    height:Annotated[float,Field(...,gt=0,description='height of patient')]
    weight:Annotated[float,Field(...,gt=0,description='weight of patient')]
    
    @computed_field()
    @property
    def bmi(self)->float:
        temp = round(self.weight/(self.height**2),2)
        return temp
    
    
    @computed_field
    @property
    def verdict(self)->str:
        if(self.bmi <18.5):
            return 'underweight'
        elif(self.bmi<25):
            return 'normal'
        elif(self.bmi<28):
            return 'normal'
        else:
            return 'obese'
        
    
    
        
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
    
def load():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

def save(data):
    with open('patients.json','w') as f:
        json.dump(data,f)
    
    


@app.get('/')
def hello():
    return {'message':'Welcome to patients manager  system '}


@app.get('/about')
def about():
    return"this is about"


@app.get('/view')
def view():
    data = load()
    return data


@app.get('/patient/{patient_id}')
def patient(patient_id:str=Path(...,description='enter the patient id',example="P001")):
    data = load()

    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code = 404,detail='patient not found')

@app.get('/sort')
def sort(sort_by:str = Query(...,description = 'sort by the weight,height and bmi')
         ,order: str = Query(...,description = 'sort in asc or desc order') ):
    details = ['weight','height','bmi']
    
    if sort_by not in details:
        raise HTTPException(status_code=400,detail=f'invalid feild select from  {details}')
    
    if order not in ['asc' , 'desc' ]:
        raise HTTPException(status_code=400,detail ='select from asc and desc only')
    
    data = load()
    
    sort_oder = True if order=='desc' else False
    
    sorted_data = sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=sort_oder)
    
    return sorted_data
     

@app.post('/create')
def create(patient:Patient):
    data = load()
    
    if patient.id in data:
        raise HTTPException(status_code=400,detail='patient already exists for this id')
    
    data[patient.id]=patient.model_dump(exclude=['id'])
    
    save(data)
    
    return JSONResponse(status_code=201,content={"message":"patient added successfully"})
    
    
     
     
@app.put('/update/{patient_id}')
def update(patient_id : str,patient_update: PatientUpdate):
    data = load()
    
    if patient_id not in data:
        raise HTTPException(status_code = 404,detail='not exists')
    
    
    old_data=data[patient_id]
    new_data=patient_update.model_dump(exclude_unset=True)
    
    for key,value in new_data.items():
        old_data[key] = value
        
    old_data['id'] = patient_id
    
    obj = Patient(**old_data)
    
    old_data = obj.model_dump(exclude=['id'])
    
    data[patient_id] = old_data
    
    save(data)
    
    return JSONResponse(status_code=200,content={'message':'user updated'})



@app.delete('/delete/{patient_id}')
def delete(patient_id : str):
    data = load()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='patient not found')
    
    del data[patient_id]
    
    save(data)
    
    return JSONResponse(status_code = 200,content={'message':'patient deleted successfully'})