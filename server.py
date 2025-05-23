import grpc
from concurrent import futures
import orders_pb2
import orders_pb2_grpc

# --- Sample in-memory data ---------------------------------------------------
_SAMPLE_ORDERS = {
    "A100": [
        {"sku": "SKU-1", "qty": 2, "price": 19.99},
        {"sku": "SKU-2", "qty": 1, "price": 5.49},
    ],
    "B200": [
        {"sku": "SKU-3", "qty": 5, "price": 2.25},
    ],
}

# --- Service implementation --------------------------------------------------
class OrdersPricingService(orders_pb2_grpc.OrdersPricingServiceServicer):
    def GetOrder(self, request, context):
        items = _SAMPLE_ORDERS.get(request.order_id, [])
        return orders_pb2.GetOrderResponse(
            order_id=request.order_id,
            items=[
                orders_pb2.LineItem(sku=i["sku"], qty=i["qty"], price=i["price"])
                for i in items
            ],
        )

    def GetPrice(self, request, context):
        items = _SAMPLE_ORDERS.get(request.order_id, [])
        total = sum(i["qty"] * i["price"] for i in items)
        return orders_pb2.GetPriceResponse(order_id=request.order_id, total_price=total)


def serve(host: str = "0.0.0.0", port: int = 50051) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    orders_pb2_grpc.add_OrdersPricingServiceServicer_to_server(OrdersPricingService(), server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    print(f"gRPC OrdersPricingService running on {host}:{port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
