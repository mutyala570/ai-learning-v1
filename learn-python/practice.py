from enum import Enum   
from collections import Counter
from collections import defaultdict
import json  
from typing import Literal

# # nums = [1, 2, 3, 4, 5]                                                                                                                                                                                                  
# # squares = [n * n for n in nums if n % 2 == 0]             
# # print(squares)


# # data = {"a": 1, "b": 2, "c": 3}                           
# # total = 0                      
# # for key, value in data:                                                                                                                                                                                         
# #     if value > 1:              
# #         total += value                                                                                                                                                                                                  
# # print(total)  


# user = {"name": "Alice", "age": 30}

# print(user["name"])
# print(user["age"])
# user["city"] = "New York"
# print(user["city"])
# print(user.get("country"))#none
# print(user.get("country", "USA"))#USA this way we can set default value if key is not present in dict

# key=[key for key in user.keys()]
# value=[value for value in user.values()]
# print(key)
# print(value)

# key_value=[(key, value) for key, value in user.items()]
# print("--------",key_value)

# string = "Hello World hello world prem"


# def count_words(s:str):
    
#     caseSensitive = s.lower()  # Convert the string to lowercase for case-insensitive counting
#     words = caseSensitive.split()  # Split the string into individual words
#     word_count = {}  # Initialize an empty dictionary to store word counts

# #     for word in words:
# #             word_count[word] = word_count.get(word, 0) + 1

#     word_count = {word: words.count(word) for word in set(words)}         

#     return word_count


# print(count_words(string))


#sorting
# def demo(*args, **kwargs):
#     print("args:", args)
#     print("kwargs:", kwargs)

# demo(1, 2, k=3, name="Prem", role="dev")

# nums = [3, 1, 4, 1, 5]   
# s1=sorted(nums)      
# print(s1)                                                                                                                                                                                         
# nums.sort()
# print(nums) 

#list comprehension

# user=[{ "name": "Prem", "age": 27 }, { "name": "Ravi", "age": 30 }]
# for u in user:
#     u["city"] = "Hyderabad"
# print(user)

# d = {"a": 1}

# d["b"] = 2                    # add a new key                                                                                                                                                                           
# d["a"] = 10                   # overwrite existing
# d.update({"c": 3, "d": 4})    # add/overwrite multiple at once 

# print(d)
# user = {"name": "Prem", "age": 27}   
# truthCheck="name" in user
# print(truthCheck)
# # Filter an existing dict — keep only positive values     
# prices = {"apple": 50, "banana": -1, "cherry": 100}                                                                                                                                                                     
# valid = {k: v for k, v in prices.items() if v > 0} 
# print(valid)



# # Counter                                                      
# words = ["a", "b", "a", "c", "b", "a"]
# counts = Counter(words)
# print(counts)

# orders = [                                                
#     {"id": 1, "status": "pending"},
#     {"id": 2, "status": "shipped"},                                                                                                                                                                                     
#     {"id": 3, "status": "pending"},
# ]  
# order_by_status = defaultdict(list)
# for o in orders:
#     order_by_status[o["status"]].append(o)
# print(dict(order_by_status))

# d = {"name": "Prem", "age": 27}
# text = json.dumps(d)
# print(text)
# print(type(text))
# parsed = json.loads(text)
# print(parsed)
# print(type(parsed))

# user = {"name": "Prem", "age": 27}                                                                                                                                                                                      
# print(user.get("city"))     # none                              
# print(user.get("name", "Unknown"))  # unknown                                                                                                                                                                                    
# print("age" in user)    # True                                                                                                                                                                                                
# print(27 in user)   # True

# products = [                                                                                                                                                                                                            
#       {"name": "shirt", "price": 800},                                                                                                                                                                                    
#       {"name": "watch", "price": 5000},                                                                                                                                                                                   
#       {"name": "cap", "price": 300},                        
#   ]   

# dis={product["name"]:product["price"] for product in products if product["price"]<1000}
# print(dis)


# nums = [1, 2, 3]
# result = list(map(lambda x: (x * 2)*x, nums))
# print(result)


def build(*parts, sep="-", **opts):
    base = sep.join(parts)
    if opts.get("upper"):
        base = base.upper()
    return base + opts.get("suffix", "")

print(build("a", "b", "c"))
print(build("a", "b", sep="_", upper=True, suffix="!"))

config = {"sep": ":", "upper": True}
print(build("x", "y", "z", **config))

raw = '[{"id": 1, "status": "active"}, {"id": 2, "status": "cancelled"}, {"id": 3}]'

def parse_orders(raw: str) -> list[dict]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []
    return [order for order in data if order.get("status") == "active"]

print(parse_orders(raw))
# Expected output: [{'id': 1, 'status': 'active'}]
print(parse_orders("not json at all"))
# Expected output: []


def normalize_intent(*messages: str, default: Literal["small_talk", "out_of_scope"] = "small_talk", **flags) -> str:
    joined = " ".join(messages).strip().lower()
    if "order" in joined or "status" in joined:
        result = "order_status MMJ"
    elif "cancel" in joined or "refund" in joined:
        result = "cancellation"
    else:
        result = default
    if flags.get("debug"):
        print(f"[debug] joined='{joined}' result='{result}'")
    return result

# print(normalize_intent("I want to check my order status", debug=True))
# Expected output: [debug] joined='i want to check my order status' result='order_status MMJ'
# Return value: 'order_status MMJ'

# print(normalize_intent("I want to cancel my order", default="out_of_scope"))
# Expected output: None
# Return value: 'cancellation'

print(normalize_intent("What's the weather like?", debug=True))
# Expected output: [debug] joined='what's the weather like?' result='small_talk'
# Return value: 'small_talk'

def top_words(text: str, n: int = 3) -> list[tuple[str, int]]:
    words = text.lower().split()
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:n]

print(top_words("the cat sat on the mat the mat was warm", n=2))
# Expected output: [('the', 3), ('mat', 2)]