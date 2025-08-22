# 🔐 zk-SNARKs Age Verification System

[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)](https://www.python.org/)  
[![Flutter](https://img.shields.io/badge/flutter-3.22-blue?logo=flutter)](https://flutter.dev/)  
[![FastAPI](https://img.shields.io/badge/fastapi-0.111-green?logo=fastapi)](https://fastapi.tiangolo.com/)  
[![Azure](https://img.shields.io/badge/deploy-Azure-blue?logo=microsoft-azure)](https://azure.microsoft.com/)  
[![CI/CD](https://img.shields.io/badge/CI/CD-GitHub_Actions-black?logo=github)](https://github.com/features/actions)  
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)  

A **privacy-preserving age verification system** built with **zk-SNARKs**, enabling users to prove they are above a required age (e.g., 18+) **without ever revealing their actual age**.  

This project demonstrates **real cryptographic ZKPs** — not just hashing tricks — using **BN128 elliptic curves, bilinear pairings, and arithmetic circuits.**

---

## ✨ Features

- ✅ **Zero-Knowledge:** Server never learns your age  
- ✅ **Cryptographic Soundness:** Proofs cannot be faked  
- ✅ **Succinct Proofs:** Constant proof size (~1KB)  
- ✅ **Fast:** Proof generation (~100ms), verification (~10ms)  
- ✅ **Non-Interactive:** Only one message required  
- ✅ **Cloud Ready:** Azure deployment templates included  

---

## 📖 How It Works

1. **Client requests a challenge** from the server  
2. **Client computes age locally** (never sent to server)  
3. **zk-SNARK proof is generated** using elliptic curve cryptography  
4. **Client sends proof only**  
5. **Server verifies proof** with bilinear pairings  
6. ✅ **Result:** Server confirms “18+” without seeing actual age  

---

## 🧮 Example: Circuit Logic

```python``
# Circuit: Prove age >= 18 without revealing age
def age_verification_circuit(private_age, public_minimum_age):
  difference = private_age - public_minimum_age
    return difference >= 0

ZKP/
├── backend/                          # Python backend
│   ├── zksnark_main.py              # FastAPI server
│   ├── zksnark_age_verification.py  # Core zk-SNARK implementation
│   ├── main.py                      # Educational demo (for learning)
│   └── requirements.txt             # Dependencies (py_ecc, FastAPI)
├── frontend/                        # Flutter frontend
│   └── zkp_age_app/
│       ├── lib/main.dart            # UI connected to API
│       └── pubspec.yaml
├── azure/                           # Azure deployment configs
└── docs/                            # Documentation

cd backend
pip install -r requirements.txt
python zksnark_main.py   # Runs on http://localhost:8001

cd frontend/zkp_age_app
flutter pub get
flutter run -d web-server --web-port 3000

Access Points

🌐 Web App → http://localhost:3000

📚 API Docs → http://localhost:8001/docs

🔍 ZKP Info → http://localhost:8001/zkp-info

Security Properties

🤐 Zero-Knowledge: Age never revealed
🛡️ Soundness: Impossible to fake proof
✅ Completeness: Valid users always verified
⚡ Succinctness: Small, constant-size proofs

# Backend → Azure App Service
az webapp create --resource-group myResourceGroup \
  --plan myAppServicePlan --name zksnark-backend \
  --runtime "PYTHON|3.11"

# Frontend → Azure Static Web Apps
cd frontend/zkp_age_app
flutter build web
az staticwebapp create --name zksnark-frontend --source .

# Backend tests
cd backend
pytest -v

# Flutter tests
cd frontend/zkp_age_app
flutter test

This project is licensed under the MIT License.
For educational and research purposes only.
