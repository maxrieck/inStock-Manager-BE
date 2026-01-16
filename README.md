
# API Routes Overview

## User Routes (`/users`)
| Method | Route | Description |
|--------|-----------------------------|-----------------------------------------------|
| POST   | /users/login                | User login                                    |
| POST   | /users/                     | Create user                                   |
| GET    | /users/                     | List users                                    |
| GET    | /users/&lt;int:user_id&gt;        | Get user by ID                                |
| PUT    | /users/&lt;int:user_id&gt;         | Update user                                   |
| DELETE | /users/                     | User self-delete (token required)             |
| DELETE | /users/&lt;int:user_id&gt;         | Admin delete user (token required)            |
| PUT    | /users/&lt;int:user_id&gt;/role    | Assign role to user                           |

## Category Routes (`/categories`)
| Method | Route | Description |
|--------|-------------------------------|--------------------------|
| POST   | /categories/                  | Create category          |
| GET    | /categories/                  | List categories          |
| GET    | /categories/&lt;int:category_id&gt;   | Get category by ID       |
| PUT    | /categories/&lt;int:category_id&gt;   | Update category          |

## Location Routes (`/locations`)
| Method | Route | Description |
|--------|-------------------------------------|--------------------------|
| POST   | /locations/                         | Create location          |
| GET    | /locations/                         | List locations           |
| GET    | /locations/&lt;int:location_id&gt;           | Get location by ID       |
| PUT    | /locations/&lt;int:location_id&gt;           | Update location          |
| PUT    | /locations/&lt;int:location_id&gt;/deactivate | Deactivate location      |
| PUT    | /locations/&lt;int:location_id&gt;/reactivate | Reactivate location      |

## Product Routes (`/products`)
| Method | Route | Description |
|--------|-------------------------------------|--------------------------|
| POST   | /products/                          | Create product           |
| GET    | /products/                          | List products            |
| GET    | /products/&lt;int:product_id&gt;              | Get product by ID        |
| PUT    | /products/&lt;int:product_id&gt;              | Update product           |
| DELETE | /products/&lt;int:product_id&gt;              | Delete product           |

## Inventory Routes (`/inventory`)
| Method | Route | Description |
|--------|------------------------------------------------------|-------------------------------|
| GET    | /inventory/                                         | List inventory (optional filters: product_id, location_id) |
| GET    | /inventory/product/&lt;int:product_id&gt;                     | Get inventory by product      |
| GET    | /inventory/location/&lt;int:location_id&gt;                     | Get inventory by location     |
| GET    | /inventory/low-stock                                | Get low-stock items           |

## Stock Transaction Routes (`/stock_transactions`)
| Method | Route | Description |
|--------|-----------------------------------------------|-------------------------------|
| POST   | /stock_transactions/                          | Create stock transaction      |
| GET    | /stock_transactions/                          | List all stock transactions   |
| GET    | /stock_transactions/&lt;int:tx_id&gt;                   | Get transaction by ID         |

## Role Routes (`/roles`)
| Method | Route | Description |
|--------|---------|----------------|
| POST   | /roles/ | Create role    |