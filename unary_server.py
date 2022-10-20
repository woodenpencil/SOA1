import grpc
import sqlite3
from concurrent import futures
import time
import unary_pb2_grpc as pb2_grpc
import unary_pb2 as pb2



class UnaryService(pb2_grpc.UnaryServicer):

    def __init__(self, *args, **kwargs):
        pass

    def GetServerResponse(self, request, context):

        # get the string from the incoming request
        district = request.district
        town = request.town
        town_type = request.town_type
        population = request.population
        result = f'Hello I am up and running received "{district}" message from you'
        result = {'message': result, 'received': True}
        try:
            sqliteConnection = sqlite3.connect('C:\\Users\\Win10\\source\\flask\\cars.db')
            sqlite_insert_querry = "INSERT INTO TOWN (TOWN_NAME, DISTRICT_ID, TOWN_TYPE, POPULATION) VALUES ('{}', {}, '{}', {});".format(town, district, town_type,population)
            print(sqlite_insert_querry)
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")
            cursor.execute(sqlite_insert_querry)
            sqliteConnection.commit()
            print("SQLite insertion executed")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while insertion: ", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("sqlite connection is closed")
        return pb2.MessageResponse(**result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_UnaryServicer_to_server(UnaryService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()




if __name__ == '__main__':
    serve()