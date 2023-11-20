from dotenv import load_dotenv
from src.services import dispatch
from concurrent import futures
import grpc, notifier_pb2_grpc


load_dotenv()


def serve(port: int = 50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    notifier_pb2_grpc.add_NotifierStreamServicer_to_server(
        dispatch.DispatchServicer(), server
    )
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server started at [::]:{port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
