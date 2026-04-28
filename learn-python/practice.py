from enum import Enum   
from collections import Counter
from collections import defaultdict
import json  
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

d = {"name": "Prem", "age": 27}
text = json.dumps(d)
print(text)
print(type(text))
parsed = json.loads(text)
print(parsed)
print(type(parsed))

user = {"name": "Prem", "age": 27}                                                                                                                                                                                      
print(user.get("city"))     # none                              
print(user.get("name", "Unknown"))  # unknown                                                                                                                                                                                    
print("age" in user)    # True                                                                                                                                                                                                
print(27 in user)   # True

products = [                                                                                                                                                                                                            
      {"name": "shirt", "price": 800},                                                                                                                                                                                    
      {"name": "watch", "price": 5000},                                                                                                                                                                                   
      {"name": "cap", "price": 300},                        
  ]   

dis={product["name"]:product["price"] for product in products if product["price"]<1000}
print(dis)