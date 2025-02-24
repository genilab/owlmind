# 🛠️ **GENILAB FAU Startup Scripts Documentation**

## 📖 **Introduction**

The **GENILAB FAU Startup Scripts** provide a streamlined, automated solution to set up, configure, test, and manage environments for Local Ollama and the FAU HPC Server. The scripts support **Windows (Git Bash)**, **macOS**, and **Linux** environments and guide users through the setup and configuration process with minimal effort.

### ⚙️ **Quickstart**

1. **Open a Terminal in the Project Root**.
2. **Run the startup script**:

```bash
bash ./start.sh
```

3. **Follow the prompts** to choose between:
   - **Environment Setup**
   - **Configuration Update**
   - **LLM Server Tests**
   - **Removing GENAIENV**

4. Upon completion, the environment will be **activated and ready for use**.

---

## 🧩 **Script Overview**

The startup process is modular and follows a logical sequence of execution:

### 1️⃣ **`scripts/1_setup_venv.sh` – Environment Setup**

**Purpose:**
- Detect the OS and create the virtual environment **`GENAIENV`**.
- Install dependencies from **`requirements.txt`**.
- Handle activation across **Windows, macOS, and Linux**.

**Key Features:**
- **Cross-platform compatibility**.
- **Smart detection** of existing environments.
- **Automatic dependency installation**.

**Edge Cases:**
- **Windows activation** uses `Scripts/activate`.
- **macOS/Linux activation** uses `bin/activate`.
- If **`GENAIENV`** already exists, the user is prompted to:
  - **Recreate** the environment.
  - **Bypass** and activate the existing environment.

**Manual Run Command:**

```bash
bash scripts/1_setup_venv.sh
```

---

### 2️⃣ **`scripts/2_setup_config.sh` – Configuration Setup**

**Purpose:**
- Locate the **`_config.example`** file across directories.
- Create or replace **`_config`** based on user input.
- Configure the server connection:
  - **Local Ollama**.
  - **FAU HPC Server** (requires **API key**).

**Key Features:**
- **Dynamic file search** without hard-coded paths.
- Prompts user to enter their **FAU API key**.
- Automatically **uncomments** the correct server settings.

**Edge Cases:**
- Missing **API key** triggers documentation reference: **`docs/CONFIG-FAU.md`**.
- **Replacing an existing `_config`** asks for user confirmation.
- **Invalid server selection** defaults to **Local Ollama**.

**Manual Run Command:**

```bash
bash scripts/2_setup_config.sh
```

**Example Final Configuration (FAU):**

```ini
# this is file: prompt-eng/config
# Point to the target Ollama or Open-WebUI Server

#URL_GENERATE=http://localhost:11434/api/generate
URL_GENERATE=https://chat.hpc.fau.edu/api/chat/completions
API_KEY=YOUR_API_KEY_HERE
```

---

### 3️⃣ **`scripts/3_setup_ollama.sh` – Ollama Server Verification**

**Purpose:**
- Validate connectivity with the selected LLM server.
- Confirm that the configured **`URL_GENERATE`** is reachable.

**Key Features:**
- **Interactive status messages**.
- **Automatic retry mechanism** on failure.
- **Clear error descriptions** for misconfigurations.

**Edge Cases:**
- **404 Not Found**: Server might not be running.
- **401 Unauthorized**: Incorrect or missing API key.
- **500 Internal Error**: Check server-side logs.

**Manual Run Command:**

```bash
bash scripts/3_setup_ollama.sh
```

**Sample Success Output:**

```plaintext
🔍 Testing server: http://localhost:11434/api/generate
✅ Success! Response: "Hello, Ollama!"
```

---

### 4️⃣ **`scripts/4_setup_llm_test.sh` – LLM Server Testing**

**Purpose:**
- Conducts **targeted tests** for configured servers.

**Key Features:**
- Allows users to test:
  - **Local Ollama**
  - **FAU HPC Server**
  - **Both servers simultaneously**
- **Looped menu** for continuous testing.
- Includes a **graceful exit option**.

**Edge Cases:**
- **API key absence** when testing **FAU** triggers a warning.
- **Server connectivity failures** are reported with HTTP status codes.

**Manual Run Command:**

```bash
bash scripts/4_setup_llm_test.sh
```

**Example Menu Interaction:**

```plaintext
🎛️ Select a test to run:
1) Test Local Ollama
2) Test FAU HPC Server
3) Test Both
4) Exit
Enter choice (1/2/3/4): 3

🔍 Testing server: http://localhost:11434/api/generate
✅ Success! Response: "Hello, Ollama!"

🔍 Testing server: https://chat.hpc.fau.edu/api/chat/completions
✅ Success! Response: "Hello from FAU HPC!"
```

---

### 5️⃣ **`scripts/remove_ve.sh` – Virtual Environment Removal**

**Purpose:**
- **Safely deletes** the **`GENAIENV`** virtual environment.

**Key Features:**
- **Confirmation prompt** before deletion.
- **Cross-platform directory removal**.
- **Forced recursive delete** ensures cleanup.

**Edge Cases:**
- **Permissions issues** require **admin access**.
- If the environment **does not exist**, the user is notified.

**Manual Run Command:**

```bash
bash scripts/remove_ve.sh
```

**Expected Interaction:**

```plaintext
This will permanently delete the virtual environment 'GENAIENV'.
Are you sure you want to proceed? (y/n): y
✅ Virtual environment 'GENAIENV' has been successfully removed.
```

---

## 🚀 **How the `start.sh` Script Works**

The `start.sh` script orchestrates the entire process. It performs the following steps:

1. **Detect OS** *(Linux, macOS, Windows Git Bash)*.
2. Checks for an existing virtual environment.
   - If found, prompts the user to either:
     - **Bypass** and activate it.
     - **Recreate** it.
     - **Remove** it.
3. **Initiates the scripts** in the correct order:
   - `1_setup_venv.sh`
   - `2_setup_config.sh`
   - `3_setup_ollama.sh`
   - `4_setup_llm_test.sh`
4. **Manages configuration logic**.
5. **Activates the environment upon completion**.

**Command:**

```bash
bash ./start.sh
```

**Menu Interaction:**

```plaintext
Welcome to the GENILAB FAU Startup Utility:
1) Set up Virtual Environment
2) Update Configuration
3) Run LLM Tests
4) Remove Virtual Environment
5) Exit

Enter your choice (1/2/3/4/5):
```

---

## 🧠 **Best Practices and Troubleshooting**

### ✅ **Best Practices**

- **Run the startup scripts from the project root**.
- **Use Bash** (Git Bash on Windows) for execution.
- **Ensure Python 3.x** is installed and available.
- **Read through `docs/CONFIG-FAU.md`** if using the FAU server.

### ⚠️ **Common Issues and Fixes**

| **Issue**              | **Cause**                     | **Fix**                                   |
|------------------------|--------------------------------|------------------------------------------|
| Environment not found  | Wrong directory or deleted env | Re-run `./start.sh` and select option 1. |
| FAU test fails          | Missing or incorrect API key   | Re-run `2_setup_config.sh` and input key.|
| Ollama test fails       | Server not running             | Start Ollama manually and retry.         |

---

## 🎯 **Conclusion**

The **GENILAB FAU Startup Scripts** provide a robust, intuitive framework to configure and test LLM-based environments. Follow the steps above to ensure seamless integration, and always consult **`docs/CONFIG-FAU.md`** when using the FAU server instance.

Happy coding! 🚀

