import random
import time
from threading import Thread
from resources.Payload_pb2 import Payload_pb2, Payload_pb2_grpc


class Payload(Payload_pb2_grpc.PayLoadServiceServicer):
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self._stop_event = None
        self.port = None
        self.orbit = 0
        self.telemetry = {'altitude': 0,
                          'longitude': 0.0,
                          'latitude': 0.0,
                          'temperature': 0
                          }
        self.transmitTelemetry = False
        self.transmitData = False
        self.images = ["resources/satellite_imagery/image{}.png".format(i) for i in range(1, 25)]
        self.deployed = False

    def move(self):
        while True:
            time.sleep(1)
            self.telemetry['longitude'] += 0.1
            if self.telemetry['longitude'] > 90.0:
                self.telemetry['longitude'] = -self.telemetry['longitude'] + ((self.telemetry['longitude'] - 90.0))
            self.telemetry['latitude'] += 0.1
            if self.telemetry['latitude'] > 180.0:
                self.telemetry['latitude'] = -self.telemetry['latitude'] + (self.telemetry['latitude'] - 180.0)
            self.telemetry['altitude'] = random.randint(self.orbit - 1, self.orbit + 1)
            self.telemetry['temperature'] = random.randint(281, 285)

    def Deploy(self, request, context):
        self.deployed = True
        self.telemetry['altitude'] = request.altitude
        self.telemetry['latitude'] = request.latitude
        self.telemetry['longitude'] = request.longitude
        self.telemetry['temperature'] = request.temperature
        self.orbit = request.orbit
        movement = Thread(target=self.move)
        movement.start()
        return Payload_pb2.DeployResponse(responseCode=200, responseMessage='Payload Deployed.')

    def StartSciData(self, request, context):
        self.transmitData = True
        while self.transmitData:
            rainfall = random.randint(0, 50)
            humidity = random.randint(0, 100)
            snow = random.randint(0, 30)
            yield Payload_pb2.StartSciDataResponse(responseCode=200,
                                                   responseMessage="Transmitting Sci data.",
                                                   rainfall=rainfall,
                                                   humidity=humidity,
                                                   snow=snow)
            time.sleep(3)

    def StartCommsData(self, request, context):
        self.transmitData = True
        while self.transmitData:
            download = random.randint(0, 10000)
            upload = random.randint(0, 1000)
            yield Payload_pb2.StartCommsDataResponse(responseCode=200,
                                                     responseMessage="Transmitting Comms Data.",
                                                     downloadSpeed=download,
                                                     uploadSpeed=upload)
            time.sleep(3)

    def StartSpyData(self, request, context):
        self.transmitData = True
        i = 0
        while self.transmitData and i < len(self.images):
            with open(self.images[i], 'rb') as image_file:
                content = image_file.read()
            yield Payload_pb2.StartSpyDataResponse(responseCode=200,
                                                   responseMessage="Transmitting Spy Data.",
                                                   image=content)
            i += 1
            time.sleep(3)

    def StopData(self, request, context):
        self.transmitData = False
        return Payload_pb2.StopDataResponse(responseCode=200, responseMessage='Data transmission stopped.')

    def Decommission(self, request, context):
        self.deployed = False
        self._stop_event.set()
        return Payload_pb2.DecommissionResponse(responseCode=200, responseMessage='Payload decommissioned.')

    def PayloadStartTelemetry(self, request, context):
        self.transmitTelemetry = True
        while self.transmitTelemetry:
            time.sleep(1)
            yield Payload_pb2.PayloadStartTelemetryResponse(responseCode=200,
                                                            responseMessage='Streaming.',
                                                            altitude=self.telemetry['altitude'],
                                                            longitude=self.telemetry['longitude'],
                                                            latitude=self.telemetry['latitude'],
                                                            temperature=self.telemetry['temperature'])

    def PayloadStopTelemetry(self, request, context):
        self.transmitTelemetry = False
        return Payload_pb2.PayloadStopTelemetryResponse(responseCode=200,
                                                        responseMessage='Telemetry transmission stopped.')
