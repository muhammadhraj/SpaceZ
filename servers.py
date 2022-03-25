import sys
import os
import threading
from concurrent import futures
import json
from multiprocessing.context import Process
import grpc
import LaunchVehicle
from resources.LaunchVehicle_pb2 import LaunchVehicle_pb2_grpc
import Payload
from resources.Payload_pb2 import Payload_pb2_grpc


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def populate_vehicles_and_payloads():
    file = open('resources/config.json', 'r')
    data = json.load(file)
    vehicles = []
    payloads = []
    all_vehicles = []
    port = 50050
    for vehicle in data:
        vehicles_payload = Payload.Payload(vehicle['payload']['name'], vehicle['payload']['type'])
        new_vehicle = LaunchVehicle.LaunchVehicle(vehicle['name'], vehicle['orbit'], vehicles_payload)
        new_vehicle.port = port
        port += 1
        vehicles_payload.port = port
        port += 1
        vehicles.append(new_vehicle)
        payloads.append(vehicles_payload)
        all_vehicles.append(new_vehicle)
        all_vehicles.append(vehicles_payload)
    return all_vehicles, vehicles, payloads

def serve(all_vehicles, i):
    try:
        stop_event = threading.Event()
        all_vehicles[i]._stop_event = stop_event
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        if i%2 == 0:
            LaunchVehicle_pb2_grpc.add_LaunchVehicleServiceServicer_to_server(all_vehicles[i], server)
        else:
            Payload_pb2_grpc.add_PayLoadServiceServicer_to_server(all_vehicles[i], server)
        server.add_insecure_port('localhost:{}'.format(all_vehicles[i].port))
        server.start()
        print('Server running at port {}...\n'.format(all_vehicles[i].port))
        # server.wait_for_termination()
        # time.sleep(30)
        stop_event.wait()
        print('Shutting server at port {} down...\n'.format(all_vehicles[i].port))
        server.stop(0)
    except KeyboardInterrupt:
        print("Server at port {} shut down.".format(all_vehicles[i].port))

def main():
    try:
        workers = []
        all_vehicles, vehicles, payloads = populate_vehicles_and_payloads()
        for i in range(len(all_vehicles)):
            worker = Process(target=serve, args=(all_vehicles, i))
            worker.start()
            workers.append(worker)

        # for worker in workers:
        #     worker.join()
        #
        # sys.exit(0)
        return workers
    except KeyboardInterrupt:
        print("Program ended.")

def stop(workers):
    for worker in workers:
        worker.terminate()
    sys.exit(0)


