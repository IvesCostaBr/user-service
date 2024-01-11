from src.utils.grpc import GrpcClient
import notifier_pb2_grpc, notifier_pb2, consumer_pb2_grpc, consumer_pb2, os

notifier_grpc_client = GrpcClient(
    f"notifier-service-{os.environ.get('ENVIRONMENT')}",
    os.environ.get("GRPC_HOST_NOTIFIER"),
    notifier_pb2_grpc.NotifierStub,
    notifier_pb2,
    True
)
admin_grpc_client = GrpcClient(
    f"admin-service-{os.environ.get('ENVIRONMENT')}",
    os.environ.get("GRPC_HOST_CONSUMER"),
    consumer_pb2_grpc.ConsumerServiceStub,
    consumer_pb2,
    True,
)
