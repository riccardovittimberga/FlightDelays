from database.DB_connect import DBConnect
from model.airport import Airport
from model.connessione import Connessione


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(Nmin, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select tmp.ID, tmp.IATA_CODE, count(*) as N
                        from (
                        SELECT a.ID , a.IATA_CODE , f.AIRLINE_ID, count(*) as n
                        FROM airports a , flights f 
                        WHERE a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID 
                        group by a.ID , a.IATA_CODE , f.AIRLINE_ID
                        ) as tmp
                        group by tmp.ID, tmp.IATA_CODE
                        having N >= %s
                        order by N desc"""

        cursor.execute(query, (Nmin,))

        for row in cursor:
            result.append(idMap[row["ID"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV1(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID , count(*) as n
                        FROM flights f 
                        group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                        order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, n desc """

        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(idMap[row["ORIGIN_AIRPORT_ID"]],
                                      idMap[row["DESTINATION_AIRPORT_ID"]],
                                      row["n"]))

        cursor.close()
        conn.close()
        return result

