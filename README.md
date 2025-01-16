# README

## Overview
This application provides a platform for managing restaurants, orders, and promotions while offering a good customer experience.

---

## 1. Customer Dashboard
### Description
A centralized dashboard that allows customers to view user information, order history, balance details, and manage their account.

### Features
- **User Information**: Display user details.
- **Order History**: List of all orders placed by the user (each order is linked to a restaurant, a list of items, and the total price paid).
- **Balance Information**: Display the current balance of the user.

---

## 2. Restaurant List
### Description
A page displaying a list of restaurants with links to individual restaurant details.

### Features
- Display all available restaurants.
- Link to each restaurant’s menu and details.

---

## 3. Restaurant Details
### Description
Detailed view of a specific restaurant, including its menu and the ability to place an order.

### Features
- **Restaurant Information**: Display details about the restaurant.
- **Menu**: Display the restaurant’s menu items.
- **Order Creation**: Option to place an order.
- **Promotions**: Display ongoing promotions for the restaurant.

---

## 4. Admin Restaurant List
### Description
Admin view of the restaurant list with functionality to add new restaurants.

### Features
- **Restaurant List**: Display all restaurants.
- **Add Restaurant**: Form to create a new restaurant.

---

## 5. Admin Restaurant Management
### Description
Admin view for managing individual restaurants, including adding menu items.

### Features
- **Restaurant Information**: Display restaurant details including name, menu, and description.
- **Menu Management**: Form to add new menu items.

---

## 6. Admin Orders Management
### Description
Admin view to manage orders for each restaurant, including updating order status (processed, cancelled, and done).

### Features
- **Order List**: Display list of orders per restaurant.
- **Order Status Management**: Buttons to cancel, accept, or mark orders as done.

---

## 7. Admin Promotions Management
### Description
Admin view to manage promotions, including viewing and adding new promotions.

### Features
- **Promotion List**: Display all promotions.
- **Add Promotion**: Form to create a new promotion for specific users that will be automatically applied once the user makes an order.

---

## Additional Service Definitions

### Users Service
- **Login**: User authentication.
- **Register**: New user registration.
- **Me**: Retrieve current user information.

### Payment Service
- **Balance Management**:
  - Retrieve user balance.
  - Add funds to the user balance.
- **Payment Processing**:
  - Process payment with promotion application.
- **Promotions**:
  - Retrieve all promotions.
  - Add a promotion for a user.
- **Payment History**:
  - Retrieve all user payments.

### Order Service
- **User Orders**:
  - Retrieve orders made by the user.
- **Restaurant Orders**:
  - Retrieve orders for a restaurant.
- **Order Status Update**:
  - Update the status of an order.

### Restaurant Service
- **Restaurant Management**:
  - Add a new restaurant.
  - Update restaurant details (name, description, etc.).
  - Get restaurant details.
- **Menu Management**:
  - Add, update, or delete menu items for a restaurant.
