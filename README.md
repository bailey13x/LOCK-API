
# Lock API

Lock API is a simple and secure product key management system built with **FastAPI**. It allows developers to deploy their own API for managing product keys, enabling features like key generation, validation, and revocation. This project is perfect for licensing applications, securing software products, or implementing a subscription-based system.

---

## Features

- 🔑 **Key Generation**: Create unique and secure product keys for applications.
- ✅ **Key Validation**: Validate product keys using a RESTful API endpoint.
- ❌ **Key Revocation**: Revoke keys that are no longer valid.
- 🗄️ **Database Integration**: Uses PostgreSQL for secure key storage.
- 🚀 **Easy Deployment**: Deploy your own Lock API on platforms like **Render**.

---

## Getting Started

Follow these steps to set up your own Lock API instance.

### **Step 1: Prepare and Clone the Repository**

Before deploying the Lock API, you need to set up GitHub and clone the repository.

1. **Create a GitHub Account (if you don’t have one):**
   - Visit [GitHub](https://github.com/) and sign up for a free account.

2. **Fork the Repository:**
   - Navigate to the original repository on GitHub (e.g., `https://github.com/bailey13x/lock-api`).
   - Click the **Fork** button at the top-right corner of the page to create a copy of the repository in your own GitHub account.

### **Step 2: Create a PostgreSQL Database on Render**

1. Log in to your [Render Dashboard](https://dashboard.render.com/).
2. Click **"New +"** > **"PostgreSQL"**.
3. Fill in the required details:
   - **Name:** Choose a name for your database (e.g., `lock-db`).
   - **Region:** Select your preferred region.
   - **Plan:** Choose the **free plan** if it suits your needs.
4. Click **Create Database**.
5. Once created, Render will generate a `DATABASE_URL` for your database. Copy this URL for use in the next steps.

### **Step 3: Generate Encyption Info**

1. Run key-generator.py (copy provided key and save)
2. Run encrypt_data.py (filling in porvided key and database url where asked)
3. Save the Encrypted Database URL given

---

### **Step 4: Deploy the Lock API on Render**

1. Go to your Render Dashboard and click **"New +"** > **"Web Service"**.
2. Select **"Connect to GitHub"** or **"Deploy Manually"** to upload your project files.
3. Fill in the required details:
   - **Name:** Choose a name for your service (e.g., `lock-api`).
   - **Environment:** Set the following environment variable:
     - `DATABASE_URL_ENCRYPTED`: Paste the Encrypted `DATABASE_URL` you copied earlier.
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

### **Step 5: Initialize and Test the Database Using Postman**

#### **5.1 Add the Database Table**

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

#### **5.2 Manually Create the Database Table**

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

#### **5.3 Validate the Generated Key**

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

#### **5.4 Revoke the Key**

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

### **Step 6: Verify Deployment**

1. Open your Render web service URL in a browser (e.g., `https://lock-api.onrender.com`).
2. You should see the root message:
   ```json
   {
       "message": "Welcome to your Lock API!"
   }
   ```

---

## License

This project is licensed under a Custom User Agreement. See the LICENSE file for details.
