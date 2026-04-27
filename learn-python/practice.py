# nums = [1, 2, 3, 4, 5]                                                                                                                                                                                                  
# squares = [n * n for n in nums if n % 2 == 0]             
# print(squares)


# data = {"a": 1, "b": 2, "c": 3}                           
# total = 0                      
# for key, value in data:                                                                                                                                                                                         
#     if value > 1:              
#         total += value                                                                                                                                                                                                  
# print(total)  
from enum import Enum   
class Intent(Enum):
     ORDER = "order_status"                                                                                                                                                                                              
     CANCEL = "cancellation"
                                                                                                                                                                                                                          
x = Intent.ORDER                                          
print(x.value)  
print(x == Intent.ORDER)
print(x == "order_status")