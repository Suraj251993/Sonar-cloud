from fastapi import FastAPI, HTTPException
import psycopg2
from databasepg import create_postgres_connection
app = FastAPI()


@app.post('/create/')
async def create_record(column_name: str):
    try:
        connection = create_postgres_connection()
        cursor = connection.cursor()

        insert_query = "INSERT INTO mwpoidata (column_name) VALUES (%s);"
        cursor.execute(insert_query, (column_name,))

        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Record created successfully"}

    except Exception as e:
        return {"error": str(e)}

@app.get('/get/{mw_poi_id}')
async def get_record(mw_poi_id: str):
    try:
        connection = create_postgres_connection()
        cursor = connection.cursor()

        select_query = "SELECT * FROM mwpoidata WHERE mw_poi_id = %s;"
        cursor.execute(select_query, (mw_poi_id,))
        record = cursor.fetchone()

        cursor.close()
        connection.close()

        if record:
            return {"record": record}
        else:
            raise HTTPException(status_code=404, detail="Record not found")

    except Exception as e:
        return {"error": str(e)}

@app.put('/update/{mw_poi_id}')
async def update_record(mw_poi_id: str, new_column_name: str):
    try:
        connection = create_postgres_connection()
        cursor = connection.cursor()

        update_query = "UPDATE mwpoidata SET column_name = %s WHERE mw_poi_id = %s;"
        cursor.execute(update_query, (new_column_name, mw_poi_id))

        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Record updated successfully"}

    except Exception as e:
        return {"error": str(e)}

@app.delete('/delete/{mw_poi_id}')
async def delete_record(mw_poi_id: str):
    try:
        connection = create_postgres_connection()
        cursor = connection.cursor()

        delete_query = "DELETE FROM mwpoidata WHERE mw_poi_id = %s;"
        cursor.execute(delete_query, (mw_poi_id,))

        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Record deleted successfully"}

    except Exception as e:
        return {"error": str(e)}