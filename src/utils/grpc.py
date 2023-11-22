import grpc, threading, time, logging


logger = logging.getLogger(__name__)


class GrpcClient:
    def __init__(self, service_name: str, host: str, stubClass: object, models: object):
        self.host = host
        self.service_name = service_name
        self.stuClass = stubClass
        self.stub = None
        self.model = models
        self.is_connected = False
        self.__start__connection()

    def __start__connection(self):
        try:
            self.channel = grpc.insecure_channel(self.host)
            self.stub = self.stuClass(self.channel)
            print("starting connection grpc!")
            self.is_connected = True
            threading.Thread(target=self.validate_connection).start()
        except:
            threading.Thread(target=self.validate_connection).start()

    def validate_connection(self):
        """Receiver heathchecks."""
        try:
            request = self.model.SendHelthCheck(service=self.service_name, ping="pong")
            while True:
                resp_stream = self.stub.Heathcheck(iter([request]))
                for each in resp_stream:
                    print(
                        f"[ {each.datetime} ] - serivce <{each.service_name}> healthcheck received: {each.status}"
                    )
                time.sleep(30)
        except Exception as e:
            self.is_connected = False
            print("error connection grpc...wait 5 seconds to reconnect!")
            time.sleep(5)
            self.__start__connection()

    # async def bidi_stream(self, method, object_type, data_generator, function=None):
    #     """Realiza comunicação de streaming bidirecional gRPC."""
    #     try:
    #         # Obtenha o método de streaming bidirecional no stub
    #         bidi_method = getattr(self.stub, method)
    #         object_type = getattr(self.objects, object_type)

    #         # Crie um objeto de stream gRPC bidirecional
    #         async def start_receiver():
    #             call = bidi_method(object_type(**data_generator))
    #             for response in call:
    #                 await function(response.data)

    #         def execute_stream():
    #             asyncio.run(start_receiver())

    #         thread = threading.Thread(target=execute_stream)
    #         thread.start()
    #         thread.join()
    #     except Exception as rpc_error:
    #         print(f"Erro no streaming: {rpc_error}")

    def __close__connection(self):
        print("clossing connection grpc!")
        self.channel.close()

    def call(self, method: str, objectName: str, payload: dict):
        """Call grpc_method."""
        try:
            if not self.is_connected:
                raise Exception("send grpc message to {}".format(self.service_name))
            bidi_method = getattr(self.stub, method)
            object_type = getattr(self.model, objectName)
            call = bidi_method(object_type(**payload))
            if call.sended:
                return True
            logger.critical(
                "error send message, returned error -> {}".format(call.message)
            )
            print(call.message)
            return False
        except Exception as e:
            return False
