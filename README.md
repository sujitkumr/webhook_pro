# GitHub Webhook Monitor

A **Flask-based webhook receiver** that captures GitHub repository events (Push, Pull Request, Merge) and displays them in a real-time web UI.

---

## 🚀 Features

- 🔄 Real-time GitHub webhook processing  
- 📊 Live dashboard with auto-refresh every 15 seconds  
- 🗄️ MongoDB storage for event persistence  
- 🎨 Modern, responsive UI design  
- 🔒 Webhook signature verification  
- 📱 Mobile-friendly interface  
![image](https://github.com/user-attachments/assets/0ef5cc52-dbcc-4612-8822-695ab4c7b4a9)

---

## 📊 Event Types Supported

### ✉️ PUSH Events  
**Format:** `"{author}" pushed to "{to_branch}" on {timestamp}`  
**Example:** "Travis" pushed to "staging" on 1st April 2021 – 9:30 PM UTC
![image](https://github.com/user-attachments/assets/21b31654-c9f5-4ce8-8115-9168a4208786)


### 📈 Pull Request Events  
**Format:** `"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}`  
**Example:** "Travis" submitted a pull request from "staging" to "master" on 1st April 2021 – 9:00 AM UTC
![image](https://github.com/user-attachments/assets/2a47ffc5-e779-46b3-be6e-b77b6acae428)


### 🔄 Merge Events  
**Format:** `"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}`  
**Example:** "Travis" merged branch "dev" to "master" on 2nd April 2021 – 12:00 PM UTC
![image](https://github.com/user-attachments/assets/3b6721a1-1692-4222-bdd3-505cee90aa42)


---

## 🧰 Prerequisites

- Python 3.8+  
- MongoDB (local or cloud instance)  
- A GitHub repository with webhook access  

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <your-webhook-repo-url>
   cd webhook-repo
