generate:
	@python -m grpc_tools.protoc -I./protos --python_out=. --pyi_out=. --grpc_python_out=. ./protos/notifier.proto

generate-consumer:
	@python -m grpc_tools.protoc -I./protos --python_out=./ --pyi_out=./ --grpc_python_out=./ ./protos/consumer.proto
