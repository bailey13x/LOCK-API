
# Lock API

Lock API is a simple and secure product key management system built with **FastAPI**. It allows developers to deploy their own API for managing product keys, enabling features like key generation, validation, and revocation. This project is perfect for licensing applications, securing software products, or implementing a subscription-based system.

---

## Features

- 🔑 **Key Generation**: Generate unique and secure product keys for applications.
- ✅ **Key Validation**: Validate product keys using a RESTful API endpoint.
- ❌ **Key Revocation**: Revoke keys that are no longer valid.
- 🗄️ **Database Integration**: Uses PostgreSQL for secure key storage.
- 🚀 **Easy Deployment**: Deploy your own Lock API on platforms like **Render**, **Heroku**, or **locally**.

---

## Getting Started

Follow these steps to set up your own Lock API instance.

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/yourusername/lock-api.git
cd lock-api
```

---

### 2. Install Dependencies
Set up a virtual environment and install the required Python dependencies:
```bash
python -m venv venv
source venv/bin/activate    # For Linux/Mac
venv\Scripts\activate       # For Windows
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables
Create a `.env` file in the root directory of the project and add the following environment variable:
```plaintext
DATABASE_URL=postgres://<username>:<password>@<hostname>:<port>/<dbname>
```
- Replace `<username>`, `<password>`, `<hostname>`, `<port>`, and `<dbname>` with your PostgreSQL database credentials.

---

### 4. Initialize the Database
Run the following script to set up the database schema:
```bash
python initialize_db.py
```

---

### 5. Run the API Locally
Start the FastAPI application locally using `uvicorn`:
```bash
uvicorn app:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

---

### 6. Deploy the API
You can deploy the API on Render, Heroku, or another platform of your choice.

#### Deploying on Render
1. Log in to [Render](https://render.com/).
2. Create a **Web Service** and link your GitHub repository.
3. Set the **build command**:
   ```bash
   pip install -r requirements.txt
   ```
4. Set the **start command**:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 10000
   ```
5. Add the `DATABASE_URL` environment variable in the Render settings.
6. Deploy the service. Once deployed, your API will be accessible via the Render URL.

---

## API Endpoints

### Base URL:
```
http://127.0.0.1:8000    # Local
https://your-render-url.com    # Deployed
```

---

### 1. Generate Key
- **Endpoint**: `POST /generate`
- **Description**: Generate a new product key.
- **Request Body**:
  ```json
  {
    "app_id": "APP001",
    "user_id": "USER123",
    "expiration_date": "2024-12-31"
  }
  ```
- **Response**:
  ```json
  {
    "key": "APP001-XXXX-YYYY-ZZZZ-ABCDEFGH"
  }
  ```

---

### 2. Validate Key
- **Endpoint**: `POST /validate`
- **Description**: Validate a product key.
- **Request Body**:
  ```json
  {
    "key": "APP001-XXXX-YYYY-ZZZZ-ABCDEFGH"
  }
  ```
- **Response**:
  - **Valid Key**:
    ```json
    {
      "valid": true
    }
    ```
  - **Invalid Key**:
    ```json
    {
      "valid": false
    }
    ```

---

### 3. Revoke Key
- **Endpoint**: `POST /revoke`
- **Description**: Revoke a product key.
- **Request Body**:
  ```json
  {
    "key": "APP001-XXXX-YYYY-ZZZZ-ABCDEFGH"
  }
  ```
- **Response**:
  ```json
  {
    "status": "Key revoked successfully."
  }
  ```

---

## Contributing

We welcome contributions to improve the Lock API! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push the changes to your fork:
   ```bash
   git push origin feature-branch
   ```
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support

If you encounter any issues or have questions, please open an issue in the repository or contact us at support@yourdomain.com.

---

### Screenshots
#### Key Validation Flow
1. **Key Validation Request**:
   ![Key Validation Request Example](https://via.placeholder.com/800x400?text=Key+Validation+Request)

2. **Successful Validation**:
   ![Successful Validation Example](https://via.placeholder.com/800x400?text=Successful+Validation)

3. **Invalid Key**:
   ![Invalid Key Example](https://via.placeholder.com/800x400?text=Invalid+Key)

---

## Future Enhancements

- Add JWT-based authentication for endpoints.
- Add analytics for key usage.
- Enhance the UI for managing keys.

---

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/).
- Deployment supported by [Render](https://render.com/).

---

### Star This Repository ⭐

If you find this project helpful, please give it a star on GitHub to show your support!
