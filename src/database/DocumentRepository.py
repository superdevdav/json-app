from sqlalchemy.sql import text
from database.models import DocumentORM, new_session
from typing import Any, Dict
import uuid
import json

class DocumentRepository:
      @staticmethod
      async def get_document(kind: str, uuid: str):
            try:
                  async with new_session() as session:
                        query = text('SELECT * FROM apps WHERE kind = :kind AND "UUID" = :uuid;')
                        result = await session.execute(query, {'kind': kind, 'uuid': uuid})
                        document = [dict(zip(result.keys(), row)) for row in result.fetchall()][0]
                        return document
            except Exception as e:
                  print(e)
      
      @staticmethod
      async def get_document_state(kind: str, uuid: str):
            try:
                  async with new_session() as session:
                        query = text('SELECT state FROM apps WHERE kind = :kind AND "UUID" = :uuid;')
                        result = await session.execute(query, {'kind': kind, 'uuid': uuid})
                        
                        row = result.fetchone()
                        if row:
                              return row[0]
                        return {'message': 'Error in getting state'}
                  
            except Exception as e:
                  print(e)

      @staticmethod
      async def insert_document(doc_data: Dict[str, Any]):
            doc_data['UUID'] = uuid.uuid4()
            json_data = json.dumps({k: v for k, v in doc_data.items() if k != 'UUID'}, indent=2)
            flag_inserted = None
            try:
                  async with new_session() as session:
                        document = DocumentORM(
                              UUID=doc_data['UUID'],
                              kind=doc_data.get('kind'),
                              name=doc_data.get('name'),
                              version=doc_data.get('version'),
                              description=doc_data.get('description'),
                              json=json_data
                        )
                        session.add(document)
                        await session.commit()
                        flag_inserted = True
                        return document.UUID
            except Exception as e:
                  print(f"Error in inserting document: {e}")
                  flag_inserted = False
            return flag_inserted

      @staticmethod
      async def update_document_state(kind: str, uuid: str, state: str):
            try:
                  async with new_session() as session:
                     query = text('UPDATE apps SET state = :state  WHERE kind = :kind AND "UUID" = :uuid;')
                     await session.execute(query, {'kind': kind, 'uuid': uuid, 'state': state})
                     await session.commit()
            except Exception as e:
                  print(f"Error in updating document state: {e}")

      @staticmethod
      async def update_document_settings(kind: str, uuid: str, new_settings: dict):
            try:
                  async with new_session() as session:
                        query = text('SELECT json FROM apps WHERE kind = :kind AND "UUID" = :uuid;')
                        result = await session.execute(query, {'kind': kind, 'uuid': uuid})
                        
                        row = result.fetchone()
                        if row:
                              json_data_str = row[0]
                              new_json = json.loads(json_data_str)
                              new_json['configuration']['settings'] = new_settings
                        else:
                              return {'message': 'Error in getting JSON'}
                        
                        query = text('UPDATE apps SET json = :json WHERE kind = :kind AND "UUID" = :uuid;')
                        await session.execute(query, {'json': json.dumps(new_json, indent=2), 'kind': kind, 'uuid': uuid})
                        await session.commit()
                        return {'message': 'Document settings updated successfully'}
            except Exception as e:
                  print(f'Error in updating document settings: {e}')
            
      @staticmethod
      async def update_document_specification(kind: str, uuid: str, new_specification: dict):
            try:
                  async with new_session() as session:
                        query = text('SELECT json FROM apps WHERE kind = :kind AND "UUID" = :uuid;')
                        result = await session.execute(query, {'kind': kind, 'uuid': uuid})
                        
                        row = result.fetchone()
                        if row:
                              json_data_str = row[0]
                              new_json = json.loads(json_data_str)
                              new_json['configuration']['specification'] = new_specification
                        else:
                              return {'message': 'Error in getting JSON'}
                        
                        query = text('UPDATE apps SET json = :json WHERE kind = :kind AND "UUID" = :uuid;')
                        await session.execute(query, {'json': json.dumps(new_json, indent=2), 'kind': kind, 'uuid': uuid})
                        await session.commit()
                        return {'message': 'Document specification updated successfully'}
            except Exception as e:
                  print(f'Error in updating document specification: {e}')                  

      @staticmethod
      async def delete_document(kind: str, uuid: str):
            flag_deleted = None
            try:
                  async with new_session() as session:
                        query = text('DELETE FROM apps WHERE kind = :kind AND "UUID" = :uuid;')
                        await session.execute(query, {'kind': kind, 'uuid': uuid})
                        await session.flush()
                        await session.commit()
                        flag_deleted = True
            except Exception as e:
                  print(f'Error in deleting document: {e}')
                  flag_deleted = False
            return flag_deleted