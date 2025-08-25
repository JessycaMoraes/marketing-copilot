# 🎯 Personalized Marketing Copilot

An AI-powered **Marketing Assistant** that helps marketers create tailored digital campaigns across multiple channels (push, email, notifications, etc.), built with **Streamlit + Python** and powered by **Gemini 2.5-pro**.  

This project was developed during **Hackday 2025 at Globo**, in collaboration with **Laura Muller, Bruno Farias, Ighor Miranda, and Leonardo Belchior**.  

---

## 👤 User Profile

Marketing professionals responsible for digital campaigns across multiple channels (push, email, social media) for products such as **streaming, content portals, entertainment, and recipes**.  

---

## 🚀 User Journey

### 1. Accessing the Tool
- The user opens the **Marketing Copilot dashboard** in the browser.  
- The interface is built with **Streamlit**.  
- Clusters are displayed based on simulated data from **BigQuery**.  

📊 **Example clusters**:  
- Cluster 1: Young sports fans (high traffic, not subscribed)  
- Cluster 2: Recipe enthusiasts who access content at night  
- Cluster 3: Former subscribers with recent re-engagement  

---

### 2. Exploring Profiles
- The user selects a **cluster**.  
- Adds a **business objective** (e.g., *"I want to promote COP30 coverage"*).  

---

### 3. Campaign Generation
With **one click**, the user requests a personalized campaign from the AI agent (Gemini):  
- Suggested message  
- Best channel  
- Optimal sending time  
- Recommended offer
- Estimated engagement (likelihood of clicks/views)    

🧠 **Example AI response**:  
- **Message**: "Have you chosen today’s dish? Watch our exclusive cooking series that everyone is talking about."  
- **Channel**: Push Notification  
- **Time**: 8 PM  
- **Offer**: Exclusive bonus episode
- **Estimated engagement**: 32% CTR    

---

## 📌 Business Questions the Agent Helps Answer
- How to personalize campaigns to increase **engagement** across different clusters?  
- What is the **best channel** for each profile (push, email, social)?  
- What is the **optimal sending time** to maximize clicks and views?  
- How to design different strategies for **subscribers vs. non-subscribers**?  
- What is the **most relevant offer** (e.g., free trial, bonus episode, discount)?  

---

## 🛠️ Tech Stack
- **Python**  
- **Streamlit** (web interface)  
- **BigQuery** (simulated dataset)  
- **Gemini 2.5-pro** (personalized campaign generation with AI)  

---

## 🗄️ Fake Dataset in BigQuery

The dataset was generated via SQL, producing:  
- **10,000 simulated rows**  
- **10,000 distinct clusters** (each with a unique `cluster_id`)  
- User attributes including:  
  - `content_interest` (sports, recipes, news)  
  - `device_type` (mobile, smart_tv, web)  
  - `previous_engagement` (push, email, etc.)  
  - `is_subscriber` (subscriber or not)  
  - `last_access`, `access_time`, `avg_daily_minutes`, `location`, `age`
 
---

## 📷 Demo

- Cluster selection screen
<img width="1920" height="1027" alt="image" src="https://github.com/user-attachments/assets/3db18d6f-294f-4003-b91a-89935c96bf6e" />


- AI-generated campaign suggestion
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/c5221170-d06c-4ec9-906c-73888488bc6b" />


---

## 🙌 Acknowledgments

Developed during Hackday 2025 at Globo by:

Laura Muller

Bruno Farias

Ighor Miranda

Leonardo Belchior

Jessyca Moraes
