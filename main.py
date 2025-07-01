from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import db_management
import generic_helper

app = FastAPI()

# Mount static and template directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

in_progress_order = {}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    session_id = generic_helper.extract_session_id(output_contexts[0]["name"])

    intent_handling_dict = {
        "track.order-context: ongoing tracking": track_order,
        "order.complete-context: ongoing-order": complete_order,
        "order.remove-context:ongoing-order": remove_from_order,
        "order.add-context:ongoing-order": add_order,
        "get.order.summary": get_order_summary

    }

    return intent_handling_dict[intent](parameters, session_id)


def get_order_summary(parameters: dict, session_id: str):
    # Get the last placed order ID
    order_id = db_management.get_max_order_id()
    if order_id!=1:
        order_id = db_management.get_max_order_id()-1
    print("Getting summary for order ID:", order_id)

    # Fetch total price and status
    total_price = db_management.get_total_order_price(order_id)
    status = db_management.get_order_status(order_id)

    # Fetch item list from 'orders' table
    order_items = db_management.get_items_in_order(order_id)

    if total_price is None or status is None or not order_items:
        return JSONResponse(content={"fulfillmentText": "Sorry! Could not retrieve your latest order summary."})

    # Format items nicely
    items_str = "\n".join([f"{item}: {qty}" for item, qty in order_items.items()])

    fulfillment_text = (
        f"Here is your order summary:\n"
        f"Order ID: {order_id}\n"
        f"Items:\n{items_str}\n"
        f"Total Price: ${total_price}\n"
        f"Status: {status}"
    )

    return JSONResponse(content={"fulfillmentText": fulfillment_text})

def remove_from_order(parameters: dict, session_id: str):
    if session_id not in in_progress_order:
        return JSONResponse(content={"fulfillmentText": "Sorry, couldn't find order. Place your order again."})

    current_order = in_progress_order[session_id]
    food_items = parameters["food-item"]
    removed_items, no_such_items = [], []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    fulfillment_text = ""
    if removed_items:
        fulfillment_text += f"Removed {', '.join(removed_items)} from your order. "
    if no_such_items:
        fulfillment_text += f"Your current order doesn't have {', '.join(no_such_items)}. "

    if not current_order:
        fulfillment_text += "Your order is empty."
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f"Your order is {order_str}."

    return JSONResponse(content={"fulfillmentText": fulfillment_text})

def add_order(parameters: dict, session_id: str):
    food_items = parameters["food-item"]
    number = parameters["number"]

    if len(food_items) != len(number):
        fulfillment_text = "Sorry, couldn't understand. Please specify food quantities clearly."
    else:
        new_food_dict = dict(zip(food_items, number))
        if session_id in in_progress_order:
            in_progress_order[session_id].update(new_food_dict)
        else:
            in_progress_order[session_id] = new_food_dict

        order_str = generic_helper.get_str_from_food_dict(in_progress_order[session_id])
        fulfillment_text = f"So far you have: {order_str}. Do you want anything else?"

    return JSONResponse(content={"fulfillmentText": fulfillment_text})
def save_to_db(order: dict):
    next_order_id = db_management.get_max_order_id()
    for food_item, quantity in order.items():
        rcode = db_management.insert_order_item(food_item, quantity, next_order_id)
        if rcode == -1:
            return -1
    db_management.insert_order_tracking(next_order_id, "in progress")
    return next_order_id

def complete_order(parameters: dict, session_id: str):
    if session_id not in in_progress_order:
        return JSONResponse(content={"fulfillmentText": "Can't find your order. Please try placing a new one."})

    order = in_progress_order[session_id]
    order_id = save_to_db(order)
    print("Saved to database")

    if order_id == -1:
        fulfillment_text = "Could not place your order due to backend issue. Please place a new order."
    else:
        order_total = db_management.get_total_order_price(order_id)
        fulfillment_text = f"Order placed! ID: {order_id}. Total: ${order_total} payable at delivery."

    del in_progress_order[session_id]
    return JSONResponse(content={"fulfillmentText": fulfillment_text})



def track_order(parameters: dict, session_id: str):
    order_id = int(parameters["order_id"])
    order_status = db_management.get_order_status(order_id)
    if order_status:
        fulfillment_text = f"The order status for your order id {order_id} is {order_status}"
    else:
        fulfillment_text = f"Could not find order id: {order_id}"
    return JSONResponse(content={"fulfillmentText": fulfillment_text})