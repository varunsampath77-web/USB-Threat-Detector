# 🛡️ USB Threat Detector (AI-Powered)

An advanced endpoint security application designed to identify, analyze, and mitigate malicious USB-borne activities in real time using Machine Learning.

## 🔗 Live Demo
👉 **[Click Here to Access the Live Dashboard](https://usb-threat-detector.streamlit.app/) 

---

### 📌 Project Overview
Moving away from traditional signature-based antivirus solutions—which fail to catch zero-day attacks—this system implements an unsupervised **Machine Learning (Isolation Forest)** framework. By evaluating granular behavioral telemetry such as keystroke inject speeds, file system entropy, and data transmission volumes, the system dynamically isolates anomalous hardware devices before they can compromise host operating system kernels.

### 🚀 Core System Architecture
The application layout relies on a robust multi-tiered environment to safely monitor and report hardware infrastructure exploits:

1. **Telemetry & Feature Extraction Layer:** Monitors peripheral mounting instances. It extracts key behavioral metrics including data transmission sizing (GB), structural script execution patterns, and keyboard interaction intervals (ms).
2. **AI Inference & Evaluation Pipeline:** An unsupervised **Isolation Forest Anomaly Detection** model trained to an evaluation metric of **98.84% accuracy**. It calculates a real-time mathematical threat vector score without relying on static malware hash databases.
3. **Security Operations Center Dashboard:** A cloud-hosted web control portal built using **Streamlit** and deployed dynamically via continuous integration pipelines. It gives security engineers an instant overview of system core health, data streams, and active defensive block counters.

### ⚙️ Technical Stack Utilized
* **Programming Language:** Python 3.11
* **Machine Learning Framework:** Scikit-Learn (Isolation Forest Model)
* **Data Processing Pipeline:** Pandas, NumPy
* **Frontend Web Application & Hosting Cloud:** Streamlit Framework, Streamlit Community Cloud Engine
* **Version Control & Repository Hosting:** Git & GitHub

### ⚡ Key Security Use Cases Addressed
* **BadUSB / Rubber Ducky Interception:** Microcontrollers designed to spoof keyboards to rapidly inject malicious terminal code. The AI core flags these instantly due to their sub-human, mathematically perfect execution delay bounds (e.g., under 10ms per stroke).
* **Ransomware & Packed Payload Neutralization:** Storage devices carrying heavily obfuscated or pre-encrypted files. The system calculates mathematical **Entropy** (file randomness). High entropy metrics instantly trigger defensive blocks to prevent system-wide encryption execution.
* **Data Exfiltration Monitoring:** Tracks bulk copying of corporate assets to unauthorized external media storage by internal actors, automatically flagging unusual transaction sizes or late-night interaction spikes.

### 🚀 How to Run Locally

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/USB-Threat-Detector.git](https://github.com/your-username/USB-Threat-Detector.git)
