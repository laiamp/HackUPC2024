from matches import *
from dataset import *


cats = ['Culture', 'Gastronomy', 'Music', 'Architecture', 'Religion/Spiritual', 'Adventure/Sport', 'Rest', 'History', 'Shopping']

root = User(2000,"juan", 23, datetime(2024, 5, 20), datetime(2024, 5, 28), "Barcelona", "Berlin", {cat: i for i, cat in enumerate(cats)}, 20)
flex = (timedelta(days=2),timedelta(days=2))

print(get_routes(root, flex, get_users("data.csv")))
