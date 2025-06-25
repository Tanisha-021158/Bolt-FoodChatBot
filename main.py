from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_management

app = FastAPI()

@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    # based on the structure of the WebhookRequest from Dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    if intent=="track.order-context: ongoing tracking":
        return track_order(parameters)
        
def track_order(parameters:dict):
    order_id=int(parameters["order_id"])
    order_status=db_management.get_order_status(order_id)

    if order_status:
        fulfillment_text=f"The order status for your order id {order_id} is {order_status}"
    else:
        fulfillment_text=f"Could not find order id: {order_id}"
    # (You can add your custom logic here and return a response)
    return JSONResponse(content={"fulfillmentText": fulfillment_text})
