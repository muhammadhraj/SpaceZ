# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from resources.Payload_pb2 import Payload_pb2 as Payload__pb2


class PayLoadServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Deploy = channel.unary_unary(
                '/PayLoadService/Deploy',
                request_serializer=Payload__pb2.DeployRequest.SerializeToString,
                response_deserializer=Payload__pb2.DeployResponse.FromString,
                )
        self.StartSciData = channel.unary_stream(
                '/PayLoadService/StartSciData',
                request_serializer=Payload__pb2.PayloadRequest.SerializeToString,
                response_deserializer=Payload__pb2.StartSciDataResponse.FromString,
                )
        self.StartCommsData = channel.unary_stream(
                '/PayLoadService/StartCommsData',
                request_serializer=Payload__pb2.PayloadRequest.SerializeToString,
                response_deserializer=Payload__pb2.StartCommsDataResponse.FromString,
                )
        self.StartSpyData = channel.unary_stream(
                '/PayLoadService/StartSpyData',
                request_serializer=Payload__pb2.PayloadRequest.SerializeToString,
                response_deserializer=Payload__pb2.StartSpyDataResponse.FromString,
                )
        self.StopData = channel.unary_unary(
                '/PayLoadService/StopData',
                request_serializer=Payload__pb2.PayloadRequest.SerializeToString,
                response_deserializer=Payload__pb2.StopDataResponse.FromString,
                )
        self.Decommission = channel.unary_unary(
                '/PayLoadService/Decommission',
                request_serializer=Payload__pb2.PayloadRequest.SerializeToString,
                response_deserializer=Payload__pb2.DecommissionResponse.FromString,
                )
        self.PayloadStartTelemetry = channel.unary_stream(
                '/PayLoadService/PayloadStartTelemetry',
                request_serializer=Payload__pb2.PayloadRequest.SerializeToString,
                response_deserializer=Payload__pb2.PayloadStartTelemetryResponse.FromString,
                )
        self.PayloadStopTelemetry = channel.unary_unary(
                '/PayLoadService/PayloadStopTelemetry',
                request_serializer=Payload__pb2.PayloadRequest.SerializeToString,
                response_deserializer=Payload__pb2.PayloadStopTelemetryResponse.FromString,
                )


class PayLoadServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Deploy(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartSciData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartCommsData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartSpyData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StopData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Decommission(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PayloadStartTelemetry(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PayloadStopTelemetry(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PayLoadServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Deploy': grpc.unary_unary_rpc_method_handler(
                    servicer.Deploy,
                    request_deserializer=Payload__pb2.DeployRequest.FromString,
                    response_serializer=Payload__pb2.DeployResponse.SerializeToString,
            ),
            'StartSciData': grpc.unary_stream_rpc_method_handler(
                    servicer.StartSciData,
                    request_deserializer=Payload__pb2.PayloadRequest.FromString,
                    response_serializer=Payload__pb2.StartSciDataResponse.SerializeToString,
            ),
            'StartCommsData': grpc.unary_stream_rpc_method_handler(
                    servicer.StartCommsData,
                    request_deserializer=Payload__pb2.PayloadRequest.FromString,
                    response_serializer=Payload__pb2.StartCommsDataResponse.SerializeToString,
            ),
            'StartSpyData': grpc.unary_stream_rpc_method_handler(
                    servicer.StartSpyData,
                    request_deserializer=Payload__pb2.PayloadRequest.FromString,
                    response_serializer=Payload__pb2.StartSpyDataResponse.SerializeToString,
            ),
            'StopData': grpc.unary_unary_rpc_method_handler(
                    servicer.StopData,
                    request_deserializer=Payload__pb2.PayloadRequest.FromString,
                    response_serializer=Payload__pb2.StopDataResponse.SerializeToString,
            ),
            'Decommission': grpc.unary_unary_rpc_method_handler(
                    servicer.Decommission,
                    request_deserializer=Payload__pb2.PayloadRequest.FromString,
                    response_serializer=Payload__pb2.DecommissionResponse.SerializeToString,
            ),
            'PayloadStartTelemetry': grpc.unary_stream_rpc_method_handler(
                    servicer.PayloadStartTelemetry,
                    request_deserializer=Payload__pb2.PayloadRequest.FromString,
                    response_serializer=Payload__pb2.PayloadStartTelemetryResponse.SerializeToString,
            ),
            'PayloadStopTelemetry': grpc.unary_unary_rpc_method_handler(
                    servicer.PayloadStopTelemetry,
                    request_deserializer=Payload__pb2.PayloadRequest.FromString,
                    response_serializer=Payload__pb2.PayloadStopTelemetryResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'PayLoadService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PayLoadService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Deploy(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PayLoadService/Deploy',
            Payload__pb2.DeployRequest.SerializeToString,
            Payload__pb2.DeployResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StartSciData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/PayLoadService/StartSciData',
            Payload__pb2.PayloadRequest.SerializeToString,
            Payload__pb2.StartSciDataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StartCommsData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/PayLoadService/StartCommsData',
            Payload__pb2.PayloadRequest.SerializeToString,
            Payload__pb2.StartCommsDataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StartSpyData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/PayLoadService/StartSpyData',
            Payload__pb2.PayloadRequest.SerializeToString,
            Payload__pb2.StartSpyDataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StopData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PayLoadService/StopData',
            Payload__pb2.PayloadRequest.SerializeToString,
            Payload__pb2.StopDataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Decommission(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PayLoadService/Decommission',
            Payload__pb2.PayloadRequest.SerializeToString,
            Payload__pb2.DecommissionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PayloadStartTelemetry(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/PayLoadService/PayloadStartTelemetry',
            Payload__pb2.PayloadRequest.SerializeToString,
            Payload__pb2.PayloadStartTelemetryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PayloadStopTelemetry(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PayLoadService/PayloadStopTelemetry',
            Payload__pb2.PayloadRequest.SerializeToString,
            Payload__pb2.PayloadStopTelemetryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)