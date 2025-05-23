import grpc
import orders_pb2
import orders_pb2_grpc

def main():
    # Connect to the gRPC server
    channel = grpc.insecure_channel("localhost:50051")
    stub = orders_pb2_grpc.OrdersPricingServiceStub(channel)

    # Test GetOrder
    order_id = "A100"
    order_response = stub.GetOrder(orders_pb2.GetOrderRequest(order_id=order_id))
    print(f"Order ID: {order_response.order_id}")
    for item in order_response.items:
        print(f" - {item.sku}: {item.qty} × ${item.price}")

    # Test GetPrice
    price_response = stub.GetPrice(orders_pb2.GetPriceRequest(order_id=order_id))
    print(f"\nTotal Price for {price_response.order_id}: ${price_response.total_price:.2f}")

if __name__ == "__main__":
    main()
