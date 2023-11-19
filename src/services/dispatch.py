import notifier_pb2_grpc, notifier_pb2, os, json

class DispatchServicer(notifier_pb2_grpc.NotifierStreamServicer):
    def Heathcheck(self, request, context):
        return notifier_pb2.HeathCheck(status="OK", version=os.environ.get("VERSION"))

    def Send(self, request_iterator, context):
        for request in request_iterator:
            channel = request.channel
            payload = json.loads(request.payload)
            return notifier_pb2.Response(id="123456789", sended=True)
        print("clossing connection!")