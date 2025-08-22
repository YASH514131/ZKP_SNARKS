from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, date
import hashlib
import secrets
import json
from typing import Dict, Any

app = FastAPI(title="ZKP Age Verification API", version="1.0.0")

# Add CORS middleware for Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgeProofRequest(BaseModel):
    birth_date: str  # Format: YYYY-MM-DD
    minimum_age: int = 18

class AgeProofResponse(BaseModel):
    proof: str
    commitment: str
    challenge: str
    is_valid: bool

class VerificationRequest(BaseModel):
    proof: str
    commitment: str
    challenge: str
    minimum_age: int = 18

class ZKPAgeVerifier:
    """
    Simple Zero-Knowledge Proof system for age verification
    Uses commitment scheme with hash functions
    """
    
    def __init__(self):
        self.salt_length = 32
    
    def calculate_age(self, birth_date: str) -> int:
        """Calculate age from birth date"""
        birth = datetime.strptime(birth_date, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return age
    
    def generate_commitment(self, age: int, salt: bytes) -> str:
        """Generate a commitment to the age using salt"""
        data = f"{age}:{salt.hex()}".encode()
        return hashlib.sha256(data).hexdigest()
    
    def generate_proof(self, birth_date: str, minimum_age: int) -> Dict[str, Any]:
        """
        Generate a zero-knowledge proof that age >= minimum_age
        without revealing the actual age
        """
        try:
            actual_age = self.calculate_age(birth_date)
            
            # Generate random salt for commitment
            salt = secrets.token_bytes(self.salt_length)
            
            # Create commitment to age
            commitment = self.generate_commitment(actual_age, salt)
            
            # Generate challenge (in real ZKP, this would come from verifier)
            challenge = secrets.token_hex(16)
            
            # Check if age meets requirement
            meets_requirement = actual_age >= minimum_age
            
            # Create proof object (simplified - in real ZKP this would be cryptographic proof)
            proof_data = {
                "salt": salt.hex(),
                "meets_requirement": meets_requirement,
                "timestamp": datetime.now().isoformat()
            }
            
            # Hash the proof data
            proof = hashlib.sha256(json.dumps(proof_data, sort_keys=True).encode()).hexdigest()
            
            return {
                "proof": proof,
                "commitment": commitment,
                "challenge": challenge,
                "proof_data": proof_data,  # In real implementation, this would be hidden
                "is_valid": meets_requirement
            }
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid birth date format: {e}")
    
    def verify_proof(self, proof: str, commitment: str, challenge: str, minimum_age: int) -> bool:
        """
        Verify the zero-knowledge proof
        In a real implementation, this would verify cryptographic proofs
        """
        # This is a simplified verification
        # In practice, the verifier wouldn't have access to proof_data
        return True  # Simplified for demo

# Initialize the ZKP verifier
zkp_verifier = ZKPAgeVerifier()

@app.get("/")
async def root():
    return {"message": "ZKP Age Verification API", "status": "running"}

@app.post("/generate-proof", response_model=AgeProofResponse)
async def generate_proof(request: AgeProofRequest):
    """
    Generate a zero-knowledge proof for age verification
    """
    try:
        result = zkp_verifier.generate_proof(request.birth_date, request.minimum_age)
        
        return AgeProofResponse(
            proof=result["proof"],
            commitment=result["commitment"],
            challenge=result["challenge"],
            is_valid=result["is_valid"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/verify-proof")
async def verify_proof(request: VerificationRequest):
    """
    Verify a zero-knowledge proof
    """
    try:
        is_valid = zkp_verifier.verify_proof(
            request.proof,
            request.commitment,
            request.challenge,
            request.minimum_age
        )
        
        return {"is_valid": is_valid, "message": "Proof verification completed"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
