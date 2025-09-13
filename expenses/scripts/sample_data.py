from expenses.models import Expense
from django.contrib.auth.models import User
from datetime import date


def run():
    user = User.objects.get(username='prash56688')  # replace with your username

    data = [
        {"title": "Breakfast at Café", "amount": 120, "category": "Food", "description": "Café coffee & sandwich",
         "date": date(2025, 6, 1), "payment_method": "UPI"},
        {"title": "Grocery Shopping", "amount": 900, "category": "Groceries", "description": "Monthly supplies",
         "date": date(2025, 6, 3), "payment_method": "Debit Card"},
        {"title": "Office Cab", "amount": 300, "category": "Travel", "description": "Ola cab to office",      "date": date(2025, 6, 4), "payment_method": "UPI"},
        {"title": "Netflix Recharge", "amount": 500, "category": "Entertainment", "description": "Monthly subscription",
         "date": date(2025, 6, 6), "payment_method": "Credit Card"},
        {"title": "Electricity Bill", "amount": 1200, "category": "Utilities", "description": "June bill",
         "date": date(2025, 6, 10), "payment_method": "Net Banking"},
        {"title": "Room Rent", "amount": 8000, "category": "Rent", "description": "Monthly room rent",
         "date": date(2025, 6, 12), "payment_method": "Cash"},
        {"title": "Lunch with Friends", "amount": 450, "category": "Food", "description": "Restaurant lunch",
         "date": date(2025, 6, 14), "payment_method": "UPI"},
        {"title": "Mobile Recharge", "amount": 250, "category": "Utilities", "description": "Airtel Prepaid",
         "date": date(2025, 6, 18), "payment_method": "UPI"},
        {"title": "Petrol Refill", "amount": 1500, "category": "Travel", "description": "Bike fuel",
         "date": date(2025, 6, 21), "payment_method": "Cash"},
        {"title": "T-Shirt Shopping", "amount": 850, "category": "Shopping", "description": "Myntra purchase",
         "date": date(2025, 6, 25), "payment_method": "UPI"},
        {"title": "Dinner Takeaway", "amount": 400, "category": "Food", "description": "Biryani from Behrouz",
         "date": date(2025, 7, 1), "payment_method": "UPI"},
        {"title": "Room Rent", "amount": 8500, "category": "Rent", "description": "Rent for July",
         "date": date(2025, 7, 5), "payment_method": "Bank Transfer"},
        {"title": "Train Ticket", "amount": 700, "category": "Travel", "description": "Lucknow to Kanpur",
         "date": date(2025, 7, 7), "payment_method": "UPI"},
        {"title": "Amazon Shopping", "amount": 2200, "category": "Shopping", "description": "Power bank + charger",
         "date": date(2025, 7, 8), "payment_method": "Credit Card"},
        {"title": "Internet Bill", "amount": 999, "category": "Utilities", "description": "WiFi recharge",
         "date": date(2025, 7, 11), "payment_method": "Net Banking"},
        {"title": "Pizza Night", "amount": 600, "category": "Food", "description": "Domino's with friends",
         "date": date(2025, 7, 14), "payment_method": "UPI"},
        {"title": "Movie Tickets", "amount": 750, "category": "Entertainment", "description": "Cinepolis Avengers",
         "date": date(2025, 7, 18), "payment_method": "UPI"},
        {"title": "Grocery Top-up", "amount": 600, "category": "Groceries", "description": "Vegetables & Snacks",
         "date": date(2025, 7, 20), "payment_method": "Cash"},
        {"title": "Gym Membership", "amount": 1500, "category": "Health", "description": "1-month gym pass",
         "date": date(2025, 7, 24), "payment_method": "Debit Card"},
        {"title": "Uber to Airport", "amount": 480, "category": "Travel", "description": "Morning ride",
         "date": date(2025, 7, 30), "payment_method": "UPI"},
        {"title": "August Rent", "amount": 8800, "category": "Rent", "description": "Monthly rent",
         "date": date(2025, 8, 1), "payment_method": "Cash"},
        {"title": "Breakfast", "amount": 150, "category": "Food", "description": "Tea and toast",
         "date": date(2025, 8, 3), "payment_method": "UPI"},
        {"title": "Swiggy Dinner", "amount": 560, "category": "Food", "description": "Fried Rice & Manchurian",
         "date": date(2025, 8, 4), "payment_method": "UPI"},
        {"title": "Laundry", "amount": 250, "category": "Miscellaneous", "description": "Washed 10 clothes",
         "date": date(2025, 8, 6), "payment_method": "Cash"},
        {"title": "Electricity Bill", "amount": 1100, "category": "Utilities", "description": "Monthly bill",
         "date": date(2025, 8, 8), "payment_method": "Net Banking"},
        {"title": "Amazon Essentials", "amount": 1400, "category": "Shopping", "description": "Toiletries etc.",
         "date": date(2025, 8, 10), "payment_method": "UPI"},
        {"title": "Travel Snacks", "amount": 300, "category": "Food", "description": "Train snacks",
         "date": date(2025, 8, 13), "payment_method": "UPI"},
        {"title": "Train Ticket", "amount": 750, "category": "Travel", "description": "Round trip Lucknow",
         "date": date(2025, 8, 14), "payment_method": "UPI"},
        {"title": "Sunday Movie", "amount": 400, "category": "Entertainment", "description": "Weekend movie",
         "date": date(2025, 8, 18), "payment_method": "UPI"},
        {"title": "Groceries Refill", "amount": 800, "category": "Groceries", "description": "Rice, Daal, Milk",
         "date": date(2025, 8, 20), "payment_method": "Cash"},
    ]

    for item in data:
        Expense.objects.create(
            user=user,
            title=item["title"],
            amount=item["amount"],
            category=item["category"],
            date=item["date"],
            description=item["description"],
            payment_method=item["payment_method"]
        )

    print("✅ 30 expenses inserted successfully.")
