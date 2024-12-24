
# Lock API

Lock API is a simple and secure product key management system built with **FastAPI**. It allows developers to deploy their own API for managing product keys, enabling features like key generation, validation, and revocation. This project is perfect for licensing applications, securing software products, or implementing a subscription-based system.

---

## Features

- 🔑 **Key Generation**: Create unique and secure product keys for applications.
- ✅ **Key Validation**: Validate product keys using a RESTful API endpoint.
- ❌ **Key Revocation**: Revoke keys that are no longer valid.
- 🗄️ **Database Integration**: Uses PostgreSQL for secure key storage.
- 🚀 **Easy Deployment**: Deploy your own Lock API on platforms like **Render** or **locally**.

---

## Getting Started

Follow these steps to set up your own Lock API instance.

### **Step 1: Clone the Repository**
Clone this repository to your local machine:
```bash
git clone https://github.com/bailey13x/lock-api.git
cd lock-api
```

---

### **Step 2: Create a PostgreSQL Database on Render**

1. Log in to your [Render Dashboard](https://dashboard.render.com/).
2. Click **"New +"** > **"PostgreSQL"**.
3. Fill in the required details:
   - **Name:** Choose a name for your database (e.g., `lock-db`).
   - **Region:** Select your preferred region.
   - **Plan:** Choose the **free plan** if it suits your needs.
4. Click **Create Database**.
5. Once created, Render will generate a `DATABASE_URL` for your database. Copy this URL for use in the next steps.

---

### **Step 3: Deploy the Lock API on Render**

1. Go to your Render Dashboard and click **"New +"** > **"Web Service"**.
2. Select **"Connect to GitHub"** or **"Deploy Manually"** to upload your project files.
3. Fill in the required details:
   - **Name:** Choose a name for your service (e.g., `lock-api`).
   - **Environment:** Set the following environment variable:
     - `DATABASE_URL`: Paste the PostgreSQL `DATABASE_URL` you copied earlier.
   - **Build Command:** Install the required dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:** Start the FastAPI app:
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port 10000
     ```

4. Click **Create Web Service** to deploy the application.
5. Wait for Render to build and deploy your API. Once deployed, you will get a URL like:
   ```
   https://lock-api.onrender.com
   ```

---

### **Step 4: Initialize and Test the Database Using Postman**

#### **4.1 Add the Database Table**

1. Open Postman.
2. Create a new **POST** request.
3. Set the URL to your Render API's endpoint:
   ```plaintext
   https://lock-api.onrender.com/generate
   ```
4. Add the following **headers**:
   - `Content-Type: application/json`
5. In the **body**, select **raw** and set the following JSON payload:
   ```json
   {
     "app_id": "TEST_APP",
     "user_id": "TEST_USER",
     "expiration_date": "2025-01-01"
   }
   ```
6. Click **Send**.

   - If the database table is set up correctly, you should receive a response like this:
     ```json
     {
       "key": "TEST_APP-XXXX-YYYY-ZZZZ-ABCDEFGH"
     }
     ```

   - If you see a database error, the `ProductKeys` table may not exist. Proceed to **Step 4.2** to manually create it.

---

#### **4.2 Manually Create the Database Table**

1. Open Postman.
2. Create a new **POST** request to the following Render **PostgreSQL Shell** endpoint:
   ```plaintext
   https://your-database-host.onrender.com
   ```
3. Add your `DATABASE_URL` as an authorization header or connect using your database credentials via a database client (e.g., `pgAdmin`, `psql`, or a GUI).

4. Run this SQL query in your database tool to manually create the `ProductKeys` table:
   ```sql
   CREATE TABLE IF NOT EXISTS ProductKeys (
       id SERIAL PRIMARY KEY,
       key TEXT UNIQUE NOT NULL,
       app_id TEXT NOT NULL,
       user_id TEXT,
       is_valid BOOLEAN DEFAULT TRUE,
       expiration_date DATE
   );
   ```

   Once the table is created, retry **Step 4.1** in Postman to verify the `generate` endpoint.

---

#### **4.3 Validate the Generated Key**

1. In Postman, create another **POST** request.
2. Set the URL to:
   ```plaintext
   https://lock-api.onrender.com/validate
   ```
3. Add the following **headers**:
   - `Content-Type: application/json`
4. In the **body**, set this JSON payload:
   ```json
   {
     "key": "TEST_APP-XXXX-YYYY-ZZZZ-ABCDEFGH"
   }
   ```
5. Click **Send**.

   - If the key exists in the database and is valid, you’ll get a response like:
     ```json
     {
       "valid": true
     }
     ```

   - If the key does not exist or has been revoked, you’ll see:
     ```json
     {
       "valid": false
     }
     ```

---

#### **4.4 Revoke the Key**

1. In Postman, create another **POST** request.
2. Set the URL to:
   ```plaintext
   https://lock-api.onrender.com/revoke
   ```
3. Add the following **headers**:
   - `Content-Type: application/json`
4. In the **body**, set this JSON payload:
   ```json
   {
     "key": "TEST_APP-XXXX-YYYY-ZZZZ-ABCDEFGH"
   }
   ```
5. Click **Send**.

   - If the key exists, the response will confirm the revocation:
     ```json
     {
       "status": "Key revoked successfully."
     }
     ```

   - If the key does not exist, you’ll get an error response.

---

### **Step 5: Verify Deployment**

1. Open your Render web service URL in a browser (e.g., `https://lock-api.onrender.com`).
2. You should see the root message:
   ```json
   {
       "message": "Welcome to your Lock API!"
   }
   ```

---

### **Optional: Local Database Setup**

To run the API with a local PostgreSQL database:

1. **Install PostgreSQL:**
   - Download and install PostgreSQL from [PostgreSQL.org](https://www.postgresql.org/).

2. **Create a Database:**
   ```bash
   createdb lock_db
   ```

3. **Set Up Environment Variables:**
   Create a `.env` file in the project root with the following content:
   ```plaintext
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=your_postgres_username
   DB_PASSWORD=your_postgres_password
   DB_NAME=lock_db
   ```

4. **Initialize the Database:**
   Run the initialization script:
   ```bash
   python initialize_db.py
   ```

5. **Start the API Locally:**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Test the API:**
   Use Postman or `curl` with `http://127.0.0.1:8000` as the base URL.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.