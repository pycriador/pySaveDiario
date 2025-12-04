# 🚀 pySaveDiário - API Documentation

**Version:** 1.0  
**Base URL:** `http://localhost:5000/api`  
**Authentication:** Token-based (Bearer Token)

---

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [Sellers](#sellers)
3. [Categories](#categories)
4. [Manufacturers](#manufacturers)
5. [Templates](#templates)
6. [Offers](#offers)
7. [Users](#users)
8. [Groups](#groups)
9. [Wishlists](#wishlists)
10. [Publications](#publications)
11. [Namespaces](#namespaces)
12. [Error Handling](#error-handling)

---

## 🔐 Authentication

### Get Token

**POST** `/api/auth/token`

```bash
curl -X POST http://localhost:5000/api/auth/token \
  -u "email@example.com:password"
```

**Response:**
```json
{
  "token": "your-access-token-here",
  "expires_in": 3600
}
```

### Using the Token

Include the token in the `Authorization` header:

```
Authorization: Bearer your-access-token-here
```

---

## 🏪 Sellers

### List All Sellers

**GET** `/api/sellers`

**Query Parameters:**
- `active_only` (boolean): Filter only active sellers

**cURL:**
```bash
curl http://localhost:5000/api/sellers
```

**Python:**
```python
import requests

response = requests.get('http://localhost:5000/api/sellers')
sellers = response.json()
```

**Node.js:**
```javascript
const axios = require('axios');

const response = await axios.get('http://localhost:5000/api/sellers');
const sellers = response.data;
```

**PHP:**
```php
<?php
$ch = curl_init('http://localhost:5000/api/sellers');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
$sellers = json_decode($response, true);
?>
```

### Create Seller

**POST** `/api/sellers`

**Required Role:** Admin or Editor

**Request Body:**
```json
{
  "name": "Shopee",
  "slug": "shopee",
  "description": "Online marketplace",
  "website": "https://shopee.com.br",
  "active": true
}
```

**cURL:**
```bash
curl -X POST http://localhost:5000/api/sellers \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Shopee",
    "slug": "shopee",
    "description": "Online marketplace",
    "website": "https://shopee.com.br"
  }'
```

**Python:**
```python
import requests

headers = {'Authorization': 'Bearer YOUR_TOKEN'}
data = {
    'name': 'Shopee',
    'slug': 'shopee',
    'description': 'Online marketplace',
    'website': 'https://shopee.com.br'
}

response = requests.post(
    'http://localhost:5000/api/sellers',
    headers=headers,
    json=data
)
seller = response.json()
```

**Node.js:**
```javascript
const axios = require('axios');

const response = await axios.post(
  'http://localhost:5000/api/sellers',
  {
    name: 'Shopee',
    slug: 'shopee',
    description: 'Online marketplace',
    website: 'https://shopee.com.br'
  },
  {
    headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
  }
);
```

**PHP:**
```php
<?php
$ch = curl_init('http://localhost:5000/api/sellers');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Authorization: Bearer YOUR_TOKEN',
    'Content-Type: application/json'
]);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([
    'name' => 'Shopee',
    'slug' => 'shopee',
    'description' => 'Online marketplace',
    'website' => 'https://shopee.com.br'
]));
$response = curl_exec($ch);
?>
```

### Get Single Seller

**GET** `/api/sellers/{id}`

### Update Seller

**PUT** `/api/sellers/{id}`

### Delete Seller

**DELETE** `/api/sellers/{id}`

**Required Role:** Admin only

---

## 🏷️ Categories

### List All Categories

**GET** `/api/categories`

**Query Parameters:**
- `active_only` (boolean): Filter only active categories

### Create Category

**POST** `/api/categories`

**Request Body:**
```json
{
  "name": "Eletrônicos",
  "slug": "eletronicos",
  "description": "Electronic products",
  "icon": "bi bi-laptop",
  "active": true
}
```

### Get Single Category

**GET** `/api/categories/{id}`

### Update Category

**PUT** `/api/categories/{id}`

### Delete Category

**DELETE** `/api/categories/{id}`

---

## 🏭 Manufacturers

### List All Manufacturers

**GET** `/api/manufacturers`

### Create Manufacturer

**POST** `/api/manufacturers`

**Request Body:**
```json
{
  "name": "Sony",
  "slug": "sony",
  "description": "Japanese electronics company",
  "website": "https://www.sony.com",
  "logo": "https://example.com/sony-logo.png",
  "active": true
}
```

### Get Single Manufacturer

**GET** `/api/manufacturers/{id}`

### Update Manufacturer

**PUT** `/api/manufacturers/{id}`

### Delete Manufacturer

**DELETE** `/api/manufacturers/{id}`

---

## 📝 Templates

### List All Templates

**GET** `/api/templates`

### Create Template

**POST** `/api/templates`

**Request Body:**
```json
{
  "name": "Instagram Post",
  "slug": "instagram-post",
  "description": "Template for Instagram posts",
  "body": "Check out this amazing deal!\n\n{product_name} for only {price}!",
  "channels": ["instagram", "facebook"]
}
```

---

## 🎯 Offers

### List All Offers

**GET** `/api/offers`

### Create Offer

**POST** `/api/offers`

**Request Body:**
```json
{
  "product_name": "PlayStation 5",
  "vendor_name": "Amazon",
  "price": 3999.99,
  "currency": "BRL",
  "offer_url": "https://amazon.com.br/ps5",
  "seller_id": 1,
  "category_id": 2,
  "manufacturer_id": 3
}
```

---

## 👥 Users

### List All Users

**GET** `/api/users`

**Required Role:** Admin

### Register User

**POST** `/api/users`

**Request Body:**
```json
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "secure_password",
  "role": "viewer"
}
```

---

## 🔔 Error Handling

### Standard Error Response

```json
{
  "message": "Error description",
  "code": 400
}
```

### HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

---

## 📦 Complete Python Example

```python
import requests

class PySaveDiarioAPI:
    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.token = self.get_token(email, password)
    
    def get_token(self, email, password):
        response = requests.post(
            f'{self.base_url}/auth/token',
            auth=(email, password)
        )
        return response.json()['token']
    
    def headers(self):
        return {'Authorization': f'Bearer {self.token}'}
    
    # Sellers
    def list_sellers(self):
        response = requests.get(
            f'{self.base_url}/sellers',
            headers=self.headers()
        )
        return response.json()
    
    def create_seller(self, data):
        response = requests.post(
            f'{self.base_url}/sellers',
            headers=self.headers(),
            json=data
        )
        return response.json()
    
    # Categories
    def list_categories(self):
        response = requests.get(
            f'{self.base_url}/categories',
            headers=self.headers()
        )
        return response.json()
    
    def create_category(self, data):
        response = requests.post(
            f'{self.base_url}/categories',
            headers=self.headers(),
            json=data
        )
        return response.json()
    
    # Manufacturers
    def list_manufacturers(self):
        response = requests.get(
            f'{self.base_url}/manufacturers',
            headers=self.headers()
        )
        return response.json()
    
    def create_manufacturer(self, data):
        response = requests.post(
            f'{self.base_url}/manufacturers',
            headers=self.headers(),
            json=data
        )
        return response.json()

# Usage
api = PySaveDiarioAPI(
    'http://localhost:5000/api',
    'admin@example.com',
    'password'
)

# List sellers
sellers = api.list_sellers()
print(sellers)

# Create new seller
new_seller = api.create_seller({
    'name': 'Kabum',
    'slug': 'kabum',
    'website': 'https://www.kabum.com.br'
})
print(new_seller)
```

---

## 🎨 Complete Node.js Example

```javascript
const axios = require('axios');

class PySaveDiarioAPI {
  constructor(baseURL, email, password) {
    this.baseURL = baseURL;
    this.email = email;
    this.password = password;
    this.token = null;
  }
  
  async getToken() {
    const response = await axios.post(
      `${this.baseURL}/auth/token`,
      {},
      {
        auth: {
          username: this.email,
          password: this.password
        }
      }
    );
    this.token = response.data.token;
    return this.token;
  }
  
  headers() {
    return {
      'Authorization': `Bearer ${this.token}`
    };
  }
  
  // Sellers
  async listSellers() {
    const response = await axios.get(
      `${this.baseURL}/sellers`,
      { headers: this.headers() }
    );
    return response.data;
  }
  
  async createSeller(data) {
    const response = await axios.post(
      `${this.baseURL}/sellers`,
      data,
      { headers: this.headers() }
    );
    return response.data;
  }
  
  // Categories
  async listCategories() {
    const response = await axios.get(
      `${this.baseURL}/categories`,
      { headers: this.headers() }
    );
    return response.data;
  }
  
  async createCategory(data) {
    const response = await axios.post(
      `${this.baseURL}/categories`,
      data,
      { headers: this.headers() }
    );
    return response.data;
  }
}

// Usage
(async () => {
  const api = new PySaveDiarioAPI(
    'http://localhost:5000/api',
    'admin@example.com',
    'password'
  );
  
  await api.getToken();
  
  const sellers = await api.listSellers();
  console.log(sellers);
  
  const newSeller = await api.createSeller({
    name: 'Kabum',
    slug: 'kabum',
    website: 'https://www.kabum.com.br'
  });
  console.log(newSeller);
})();
```

---

**Documentation Version:** 1.0  
**Last Updated:** 2025-11-19  
**Contact:** support@pysavediario.com

