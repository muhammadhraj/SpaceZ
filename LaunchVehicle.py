import random
import time
from threading import Thread
import grpc
from resources.Payload_pb2 import Payload_pb2, Payload_pb2_grpc
from resources.LaunchVehicle_pb2 import LaunchVehicle_pb2_grpc, LaunchVehicle_pb2


class LaunchVehicle(LaunchVehicle_pb2_grpc.LaunchVehicleServiceServicer):
    def __init__(self, name, orbit, payload):
        self.name = name
        self.orbit = orbit
        self.payload = payload
        self.telemetry = {"altitude": 0,
                          "longitude": -80.576,
                          "latitude": 28.431,
                          "temperature": 298,
                          "timeToOrbit": (orbit // 3600) + 10}
        self.reachedOrbit = False
        self.transmitTelemetry = False
        self._stop_event = None
        self.port = None

    def move(self):
        while True:
            time.sleep(1)
            if not self.reachedOrbit:
                self.telemetry['altitude'] += (self.orbit // ((self.orbit // 3600) + 10))
                self.telemetry['temperature'] -= (15 / ((self.orbit // 3600) + 10))
            else:
                self.telemetry['altitude'] = random.randint(self.orbit - 1, self.orbit + 1)
                self.telemetry['temperature'] = random.randint(281, 285)
            self.telemetry['longitude'] += 0.1
            if self.telemetry['longitude'] > 90.0:
                self.telemetry['longitude'] = -self.telemetry['longitude'] + ((self.telemetry['longitude'] - 90.0))
            self.telemetry['latitude'] += 0.1
            if self.telemetry['latitude'] > 180.0:
                self.telemetry['latitude'] = -self.telemetry['latitude'] + (self.telemetry['latitude'] - 180.0)
            if not self.reachedOrbit:
                self.telemetry['timeToOrbit'] -= 1
                if self.telemetry['timeToOrbit'] == 0:
                    self.reachedOrbit = True

    def VehicleLaunch(self, request, context):
        movement = Thread(target=self.move)
        movement.start()
        while not self.reachedOrbit:
            time.sleep(.5)
            yield LaunchVehicle_pb2.VehicleLaunchResponse(responseCode=200,
                                                          responseMessage='Vehicle ascending.',
                                                          timeToOrbit=self.telemetry['timeToOrbit'])
        yield LaunchVehicle_pb2.VehicleLaunchResponse(responseCode=200,
                                                      responseMessage='Vehicle has reached orbit.',
                                                      timeToOrbit=self.telemetry['timeToOrbit'])

    def DeployPayload(self, request, context):
        port = self.payload.port
        channel = grpc.insecure_channel('localhost:{}'.format(port))
        stub = Payload_pb2_grpc.PayLoadServiceStub(channel)
        deploy_request = Payload_pb2.DeployRequest(altitude=self.telemetry['altitude'],
                                                   latitude=self.telemetry['latitude'],
                                                   longitude=self.telemetry['longitude'],
                                                   temperature=self.telemetry['temperature'],
                                                   orbit=self.orbit)
        stub.Deploy(request=deploy_request)
        return LaunchVehicle_pb2.DeployPayloadResponse(responseCode=200, responseMessage='Payload deployed!')

    def Deorbit(self, request, context):
        self._stop_event.set()
        return LaunchVehicle_pb2.DeorbitResponse(responseCode=200, responseMessage='Vehicle has deorbited.')

    def VehicleStartTelemetry(self, request, context):
        self.transmitTelemetry = True
        while self.transmitTelemetry:
            time.sleep(1)
            yield LaunchVehicle_pb2.VehicleStartTelemetryResponse(responseCode=200,
                                                                  responseMessage='Streaming.',
                                                                  altitude=self.telemetry['altitude'],
                                                                  longitude=self.telemetry['longitude'],
                                                                  latitude=self.telemetry['latitude'],
                                                                  temperature=self.telemetry['temperature'],
                                                                  timeToOrbit=self.telemetry['timeToOrbit'])

    def VehicleStopTelemetry(self, request, context):
        self.transmitTelemetry = False
        return LaunchVehicle_pb2.VehicleStopTelemetryResponse(responseCode=200,
                                                              responseMessage='Telemetry transmission stopped.')
