from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_management
import generic_helper

app = FastAPI()

in_progress_order={
    
}


@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    # based on the structure of the WebhookRequest from Dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    session_id=generic_helper.extract_session_id(output_contexts[0]["name"])

    intent_handling_dict={
        "track.order-context: ongoing tracking":track_order,
        "order.complete-context: ongoing-order":complete_order,
        # "order.remove-context:ongoing-order":remove_from_order,
        "order.add-context:ongoing-order":add_order
    }

    return intent_handling_dict[intent](parameters,session_id)



def add_order(parameters:dict,session_id:str):
    food_items=parameters["food-item"]
    number=parameters["number"]

    if len(food_items)!=len(number):
        fulfillemet_text=f"Sorry didnot understand...Please specify the food quantities clearly..."
    else:

        new_food_dict=dict(zip(food_items,number))

        if session_id in in_progress_order:
            in_progress_order[session_id].update(new_food_dict)
            
        else:
            in_progress_order[session_id]=new_food_dict
        
        order_str=generic_helper.get_str_from_food_dict(in_progress_order[session_id])


        fulfillemet_text=f"So far you have: {order_str}. Do you want anything else?"
    return JSONResponse(content={"fulfillmentText": fulfillemet_text})


def complete_order(parameters:dict,session_id:str):
    if session_id not in in_progress_order:
        fulfillment_text=f"I am having trouble in finding your order...Please try placing a new order."
    else:
        order=in_progress_order[session_id]
        order_id=save_to_db(order)

        if order_id==-1:
            fulfillment_text="Could not place your order due to backend issue...Try again"\
                            "Please place a new order."
        else:
            order_total=db_management.get_total_order_price(order_id)
            fulfillment_text=f"Sucessfully placed your order! "\
                            f"Here is your order id {order_id}. "\
                            f"Your order total is {order_total} which you can pay at the time of delivery."
        del in_progress_order[session_id]
    return JSONResponse(content={"fulfillmentText": fulfillment_text})


def save_to_db(order:dict):
    next_order_id=db_management.get_max_order_id()
    for food_item,quantity in order.items():
        rcode=db_management.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )

        if rcode==-1:
            return -1
    db_management.insert_order_tracking(next_order_id,"in progress")
    return next_order_id

def track_order(parameters:dict,session_id:str):
    order_id=int(parameters["order_id"])
    order_status=db_management.get_order_status(order_id)

    if order_status:
        fulfillment_text=f"The order status for your order id {order_id} is {order_status}"
    else:
        fulfillment_text=f"Could not find order id: {order_id}"
    # (You can add your custom logic here and return a response)
    return JSONResponse(content={"fulfillmentText": fulfillment_text})
