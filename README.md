# pyscitq2
Python workflow lib for scitq2

## gRPC update

- Copy scitq2 .proto file in this repo proto folder
- make sure you have the right python package:
```sh
pip install grpcio grpcio-tools
```
- Type in the following command:
```sh
python -m grpc_tools.protoc \
  -I proto \
  --python_out=src/scitq2/pb \
  --grpc_python_out=src/scitq2/pb \
  --proto_path=proto \
  --experimental_allow_proto3_optional \
  proto/taskqueue.proto
sed -i '' 's/^import taskqueue_pb2/from . import taskqueue_pb2/' src/scitq2/pb/taskqueue_pb2_grpc.py
```