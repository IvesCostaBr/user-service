# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import consumer_pb2 as consumer__pb2


class ConsumerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Heathcheck = channel.stream_stream(
            "/Consumer.ConsumerService/Heathcheck",
            request_serializer=consumer__pb2.SendHelthCheck.SerializeToString,
            response_deserializer=consumer__pb2.HeathCheck.FromString,
        )
        self.GetConsumers = channel.unary_unary(
            "/Consumer.ConsumerService/GetConsumers",
            request_serializer=consumer__pb2.FindConsumers.SerializeToString,
            response_deserializer=consumer__pb2.ListConsumers.FromString,
        )
        self.GetCredentials = channel.unary_unary(
            "/Consumer.ConsumerService/GetCredentials",
            request_serializer=consumer__pb2.FindCredentials.SerializeToString,
            response_deserializer=consumer__pb2.ListCredentials.FromString,
        )
        self.GetProviders = channel.unary_unary(
            "/Consumer.ConsumerService/GetProviders",
            request_serializer=consumer__pb2.FindProviders.SerializeToString,
            response_deserializer=consumer__pb2.ListProviders.FromString,
        )
        self.GetJourney = channel.unary_unary(
            "/Consumer.ConsumerService/GetJourney",
            request_serializer=consumer__pb2.FindJouneys.SerializeToString,
            response_deserializer=consumer__pb2.ListJourneys.FromString,
        )


class ConsumerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Heathcheck(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetConsumers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetCredentials(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetProviders(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetJourney(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_ConsumerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "Heathcheck": grpc.stream_stream_rpc_method_handler(
            servicer.Heathcheck,
            request_deserializer=consumer__pb2.SendHelthCheck.FromString,
            response_serializer=consumer__pb2.HeathCheck.SerializeToString,
        ),
        "GetConsumers": grpc.unary_unary_rpc_method_handler(
            servicer.GetConsumers,
            request_deserializer=consumer__pb2.FindConsumers.FromString,
            response_serializer=consumer__pb2.ListConsumers.SerializeToString,
        ),
        "GetCredentials": grpc.unary_unary_rpc_method_handler(
            servicer.GetCredentials,
            request_deserializer=consumer__pb2.FindCredentials.FromString,
            response_serializer=consumer__pb2.ListCredentials.SerializeToString,
        ),
        "GetProviders": grpc.unary_unary_rpc_method_handler(
            servicer.GetProviders,
            request_deserializer=consumer__pb2.FindProviders.FromString,
            response_serializer=consumer__pb2.ListProviders.SerializeToString,
        ),
        "GetJourney": grpc.unary_unary_rpc_method_handler(
            servicer.GetJourney,
            request_deserializer=consumer__pb2.FindJouneys.FromString,
            response_serializer=consumer__pb2.ListJourneys.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "Consumer.ConsumerService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class ConsumerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Heathcheck(
        request_iterator,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            "/Consumer.ConsumerService/Heathcheck",
            consumer__pb2.SendHelthCheck.SerializeToString,
            consumer__pb2.HeathCheck.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetConsumers(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/Consumer.ConsumerService/GetConsumers",
            consumer__pb2.FindConsumers.SerializeToString,
            consumer__pb2.ListConsumers.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetCredentials(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/Consumer.ConsumerService/GetCredentials",
            consumer__pb2.FindCredentials.SerializeToString,
            consumer__pb2.ListCredentials.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetProviders(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/Consumer.ConsumerService/GetProviders",
            consumer__pb2.FindProviders.SerializeToString,
            consumer__pb2.ListProviders.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetJourney(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/Consumer.ConsumerService/GetJourney",
            consumer__pb2.FindJouneys.SerializeToString,
            consumer__pb2.ListJourneys.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
