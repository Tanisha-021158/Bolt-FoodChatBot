# 🍽️ Food Order Chatbot (FastAPI + Dialogflow + MySQL)

This project is a backend chatbot server built using **FastAPI** and connected to **Dialogflow** for natural language interaction. It helps users to **track orders**, **get order prices**, **insert items**, and **remove items** from their food orders, all stored and managed through a **MySQL** database.

---

## 🚀 Features

- ✅ Track order status by `order_id`
- ✅ Get total or specific order price
- ✅ Insert food items into orders
- ✅ Remove food items from orders
- ✅ Store and update order tracking status
- ✅ Integrated with Dialogflow via webhook
- ✅ Localhost exposed using `ngrok`

---

## 🗂️ Project Structure

```
Bolt-FoodChatBot/
├── main.py               # FastAPI app with all route handling
├── db_management.py      # All DB-related functions
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 🛠️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Bolt-FoodChatBot.git
   cd Bolt-FoodChatBot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI server**
   ```bash
   uvicorn main:app --reload
   ```

4. **Expose local server using ngrok**
   ```bash
   ngrok http 8000
   ```

5. **Paste the generated ngrok URL** into Dialogflow’s webhook URL.

---

## 💬 Dialogflow Integration

### ✅ Intents Handled:
- `track.order-context: ongoing tracking`
- `insert.food-item`
- `remove.food-item`

### ✅ Sample User Input:
```
Remove 2 samosas and 1 chole bhature
```

### ✅ Sample Webhook JSON (Dialogflow → FastAPI):
```json
{
  "queryResult": {
    "intent": {
      "displayName": "remove.food-item"
    },
    "parameters": {
      "food-item": ["samosas", "chole bhature"],
      "number": [2, 1]
    }
  }
}
```

---

## 🔧 Example Functions in `db_management.py`

- `get_order_status(order_id)`
- `get_order_price(order_id)`
- `insert_order_item(food_item, quantity, order_id)`
- `insert_order_tracking(order_id, status)`
- `remove_order_item(food_item, quantity, order_id)`

---

## 🗃️ MySQL Tables Description

### `food_items`

| item_id | name           | price (USD) |
|---------|----------------|-------------|
| 1       | samosas        | 2.50        |
| 2       | chole bhature  | 4.00        |

Stores the available food items with their prices.

---

### `order_tracking`

| order_id | status       |
|----------|--------------|
| 101      | Delivered    |
| 102      | In Progress  |

Tracks the delivery status of each order.

---

### `orders`

| order_id | item_id | quantity | total_price (USD) |
|----------|---------|----------|-------------------|
| 101      | 1       | 2        | 5.00              |
| 101      | 2       | 1        | 4.00              |

Records the items in each order along with quantity and calculated total price.

---

## 🔐 Notes

- ✅ Make sure MySQL is running and the credentials match in `db_management.py`
- ❗ Ngrok URLs expire after each session — update webhook URL in Dialogflow every time
- ❗ Keep your DB password secure; consider using environment variables or `.env` files

---

## 🧪 Example API Test

```http
POST /
Content-Type: application/json

{
  "queryResult": {
    "intent": {
      "displayName": "track.order-context: ongoing tracking"
    },
    "parameters": {
      "order_id": 101
    },
    "outputContexts": []
  }
}
```

---

## 📈 Future Scope

- Add user authentication
- Admin dashboard for managing orders
- Integrate payment API for real-time price calculations
- Store deleted items in a history table

---

## 📜 License

MIT License. Use, modify, and distribute freely.
