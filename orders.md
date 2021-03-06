# Orders

An order is essentially a list of product IDs with quantity

The Order resource has the following schema:

|Field| Type| Description|
|-----|-----|------------|
|id|uuid v4 string| the product id (is autogenerated at creation time)|
|products|object| the list of key(product_id)-value(quantity) pairs representing the product list|

## Order Resource endpoints and examples

### Create an Order 
HTTP verb: POST

HTTP successful return code: 201, 400, 500

Endpoint: http://localhost:5000/orders

Curl example:
```bash
curl -X POST http://localhost:5000/orders -d '
{
	"products":{
		"077f0d58-8420-4d36-b4da-9dd45469c5dc": 1,
		"f3753db3-0521-4214-b311-d31bae67921d": 2
	}
}'
```

Returns a detailed receipt for the submitted order with an oder ID. Example: 
```json
{
    "total": 25.89,
    "sales_tax": 1.9,
    "products": [
        {
            "price": 18.99,
            "quantity": 1,
            "description": "",
            "imported": false,
            "category": "miscellaneous",
            "id": "077f0d58-8420-4d36-b4da-9dd45469c5dc",
            "name": "Bottle of Perfume 3"
        },
        {
            "price": 2.5,
            "quantity": 2,
            "description": "",
            "imported": false,
            "category": "food",
            "id": "f3753db3-0521-4214-b311-d31bae67921d",
            "name": "Bag of potato chips"
        }
    ],
    "order_id": "a29dd512-9a07-426d-b645-b2340986b956"
}
```


