
from fastapi import FastAPI,Path,HTTPException,Query
import json
app = FastAPI()



def load():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data


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
     
     
     
     
