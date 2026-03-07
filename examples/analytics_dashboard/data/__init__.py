"""Sample data for the analytics dashboard."""
from __future__ import annotations

import random
from datetime import datetime, timedelta

from cacao.server.data import DataFrame, sample_users_data


def generate_time_series(days: int = 90) -> DataFrame:
    """Generate realistic time series data."""
    base_date = datetime.now() - timedelta(days=days)
    data = []
    base_revenue = 10000
    base_users = 500

    for i in range(days):
        date = base_date + timedelta(days=i)
        v = random.uniform(0.8, 1.2)
        trend = 1 + (i / days) * 0.3

        revenue = base_revenue * v * trend
        users = int(base_users * v * trend)
        orders = int(users * random.uniform(0.3, 0.5))
        conversion = (orders / users * 100) if users else 0

        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "revenue": round(revenue, 2),
            "users": users,
            "orders": orders,
            "conversion": round(conversion, 1),
            "category": random.choice(["Electronics", "Clothing", "Food", "Books"]),
        })

    return DataFrame(data)


def generate_category_breakdown() -> DataFrame:
    return DataFrame([
        {"category": "Electronics", "revenue": 45000, "orders": 320},
        {"category": "Clothing", "revenue": 32000, "orders": 580},
        {"category": "Food", "revenue": 18000, "orders": 1200},
        {"category": "Books", "revenue": 12000, "orders": 890},
        {"category": "Home & Garden", "revenue": 28000, "orders": 420},
    ])


def generate_funnel_data() -> DataFrame:
    return DataFrame([
        {"stage": "Visitors", "count": 10000},
        {"stage": "Sign Ups", "count": 4500},
        {"stage": "Activated", "count": 2800},
        {"stage": "Subscribers", "count": 1200},
        {"stage": "Paying", "count": 450},
    ])


# Pre-generated datasets
time_series = generate_time_series(90)
category_data = generate_category_breakdown()
funnel_data = generate_funnel_data()
users_data = sample_users_data(100)

total_revenue = time_series.sum("revenue")
total_users = time_series.sum("users")
total_orders = time_series.sum("orders")
avg_conversion = time_series.mean("conversion")
