from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse
from database.DocumentRepository import DocumentRepository
from rest.models.engine.Engine import Engine as MyModel
from kafka.producer import send_message
import json
import os

router = APIRouter()

def check_valid(item):
    try:
        MyModel(**item)
        return True
    except Exception as _:
        return False


def get_schema_path(kind: str) -> str:
     current_dir = os.path.dirname(__file__)
     project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
     project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir, os.pardir, os.pardir))
     schema_path = os.path.join(project_root, f'{kind}-schema.json')
     return schema_path


@router.get("/{kind}/{uuid}")
async def read_document(kind: str, uuid: str):
     try:
          doc = await DocumentRepository.get_document(kind, uuid)
          if doc is not None:
               return doc
          else:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
     except HTTPException as http_ex:
          raise http_ex
     except Exception as ex:
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)


@router.get("/{kind}/{uuid}/state")
async def read_document_state(kind: str, uuid: str):
     try:
          doc_state = await DocumentRepository.get_document_state(kind, uuid)
          return JSONResponse(content=doc_state, status_code=status.HTTP_200_OK)
     except Exception as ex:
          HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)


@router.post("/{kind}/")
async def add_document(kind: str):
     schema_path = get_schema_path(kind)
     if not os.path.exists(schema_path):
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schema file not found")

     with open (schema_path, 'r') as file:
          data = json.load(file)

     try:
          if check_valid(data):
               document = MyModel(**data)
               if await DocumentRepository.insert_document(document.model_dump()):
                    send_message('post_topic', {'action': 'post', 'kind': kind})
                    return JSONResponse(content={"message": "Document added successfully"}, status_code=status.HTTP_201_CREATED)
               else:
                    return JSONResponse(content={"message": "Document not added"}, status_code=status.HTTP_409_CONFLICT)
          else:
               raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Document not valid")
     except HTTPException as http_ex:
          raise http_ex
     except Exception as ex:
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)


@router.put("/{kind}/{uuid}/state")
async def update_document_state(kind: str, uuid: str, request: Request):
     try:
          params = dict(request.query_params)
          new_state = params['']
          if new_state in ('NEW', 'INSTALLING', 'RUNNING'):
               await DocumentRepository.update_document_state(kind, uuid, new_state)
               send_message('put_topic', f'Updated {uuid} {{state: {new_state}}}')
               return JSONResponse(content={'message': 'Document state updated successfully'}, status_code=status.HTTP_200_OK)
          else:
               raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect state value')
     except HTTPException as http_ex:
          raise http_ex
     except Exception as ex:
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)


@router.put('/{kind}/{uuid}/configuration/')
async def update_document_specification(kind: str, uuid: str, request: Request):
     try:
          params = dict(request.query_params)
          result =  await DocumentRepository.update_document_specification(kind, uuid, params)

          if result == {'message': 'Error in getting JSON'}:
               status_code = status.HTTP_400_BAD_REQUEST
          else:
               status_code = status.HTTP_200_OK

          send_message('put_topic', f'Updated {uuid} {{specification: {params}}}')
          return JSONResponse(content=result, status_code=status_code)
     except Exception as ex:
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)


@router.put("/{kind}/{uuid}/settings/")
async def update_document_settings(kind: str, uuid: str, request: Request):
     try:
          params = dict(request.query_params)
          result = await DocumentRepository.update_document_settings(kind, uuid, params)
          
          if result == {'message': 'Error in getting JSON'}:
               status_code = status.HTTP_400_BAD_REQUEST
          else:
               status_code = status.HTTP_200_OK
          
          send_message('put_topic', f'Updated {uuid} {{settings: {params}}}')
          return JSONResponse(content=result, status_code=status_code)
     except Exception as ex:
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)


@router.delete("/{kind}/{uuid}/")
async def delete_document(kind: str, uuid: str):
     try:
          if await DocumentRepository.delete_document(kind, uuid):
               send_message('delete_topic', f'Deleted {uuid}')
               return JSONResponse(content={'message': 'Document deleted successfully'}, status_code=status.HTTP_200_OK)
          else:
               return JSONResponse(content={'message': 'Document not deleted'}, status_code=status.HTTP_400_BAD_REQUEST)
     except Exception as ex:
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)