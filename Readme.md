> # It's a backend API of a restaurant apps .







# **Restaurant**:
> ### restaurant_signup ***(sudip) done***
- id
- username
- name
- email
- phone number
- address
- password\
(show signup successful)
> ### restaurant_signin ***(sudip) done***
  - email
  - password
  (show signed in successfully)
 >### add_items ***(Tuhin)***
  - item name
  - item description
  - item price
  - item cooking time
  - item quantity
  - ForeignKey('restaurant_signup.id')
    (items added successfully)
> ### get_customer_ordered_dishes ***(Tuhin)***
  - restaurant_id\
  (show order details of current restaurant)

# **User**:
> ### customer_signup ***(subhajit)***
  - id
  - name
  - email
  - phone number
  - address
  - password\
  (signup successful)
>### customer_signin ***(Rounak)***
  - username
  - password\
  (signed in successfully)
> ### choose_restaurant ***(sayan)***
  - restaurant_name\
  (if restaurant_name not match --> restaurant not available)\
  (if restaurant_name matched --> show available dishes and its rating)
> ### choose_dishes_place_order ***(subhajit)***
  - restaurant_name
  - dish_name
  - quantity
  - delivery_address
  - ForeignKey('customer_signup.id')
  
  (if quantity not available then show the available quantity) \
  (if quantity available show dishes are available.)\
  (Order successful. Payment should be done in cash to the delivery person.)
> ### check ordered history of customers
  - username
  >show dictionary of oredered history of customers where keys are 
  ```
  >- restaurant_name
  >- dish_name
  >- quantity
  >- price
  >- Total_price
  >- delivery_address
  ```
> ### delivery
- restaurant_name\
  (it will be deleted the first order from the customer order table of the specific restaurant and show it's delivered order successfully)
> ###  give_rating_feedback ***(sayan)***
  - restaurant_name
  - customer_name
  - item_name
  - item_rating
  - item_feedback \
  (Thanks for your feedback)
