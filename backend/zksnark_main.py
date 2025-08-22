"""
Real zk-SNARKs Age Verification API

This FastAPI server implements true Zero-Knowledge Proofs using zk-SNARKs
for age verification where the server never learns the user's actual age.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, Optional, List
import secrets
import json

# Import our zk-SNARK implementation
from zksnark_age_verification import ZKSNARKAgeVerifier, Proof

app = FastAPI(
    title="zk-SNARKs Age Verification API", 
    version="2.0.0",
    description="True Zero-Knowledge Age Verification using zk-SNARKs"
)

# Add CORS middleware for Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the zk-SNARK verifier
zksnark_verifier = ZKSNARKAgeVerifier()

# API Models
class ChallengeRequest(BaseModel):
    minimum_age: int = 18

class ChallengeResponse(BaseModel):
    challenge: str
    minimum_age: int
    session_id: str
    message: str

class ZKProofRequest(BaseModel):
    proof: Dict[str, Any]  # The zk-SNARK proof
    public_inputs: List[int]  # [minimum_age, result]
    challenge: str
    session_id: str

class ZKProofResponse(BaseModel):
    is_valid: bool
    message: str
    verification_details: Dict[str, Any]

class ClientProofRequest(BaseModel):
    """For client-side proof generation demo"""
    actual_age: int  # This would normally not be sent to server!
    minimum_age: int
    challenge: str

# Store active sessions
active_sessions = {}

@app.get("/")
async def root():
    return {
        "message": "zk-SNARKs Age Verification API",
        "status": "running",
        "zkp_type": "zk-SNARKs",
        "zero_knowledge": True
    }

@app.post("/request-challenge", response_model=ChallengeResponse)
async def request_challenge(request: ChallengeRequest):
    """
    Step 1: Client requests a verification challenge
    Server generates random challenge for the zk-SNARK protocol
    """
    try:
        # Generate cryptographic challenge
        challenge = zksnark_verifier.generate_challenge()
        session_id = secrets.token_hex(16)
        
        # Store session information
        active_sessions[session_id] = {
            "challenge": challenge,
            "minimum_age": request.minimum_age,
            "created_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        return ChallengeResponse(
            challenge=challenge,
            minimum_age=request.minimum_age,
            session_id=session_id,
            message="Challenge generated. Generate proof on client side."
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Challenge generation failed: {e}")

@app.post("/verify-zkproof", response_model=ZKProofResponse)
async def verify_zkproof(request: ZKProofRequest):
    """
    Step 2: Verify client-generated zk-SNARK proof
    Server verifies proof WITHOUT learning user's actual age
    """
    try:
        # Validate session
        if request.session_id not in active_sessions:
            raise HTTPException(status_code=400, detail="Invalid session ID")
        
        session = active_sessions[request.session_id]
        
        # Verify challenge matches
        if session["challenge"] != request.challenge:
            raise HTTPException(status_code=400, detail="Challenge mismatch")
        
        # Verify minimum age matches
        if len(request.public_inputs) < 1 or request.public_inputs[0] != session["minimum_age"]:
            raise HTTPException(status_code=400, detail="Minimum age mismatch")
        
        # Package proof data for verification
        proof_data = {
            "proof": request.proof,
            "public_inputs": request.public_inputs,
            "challenge": request.challenge,
            "timestamp": datetime.now().isoformat()
        }
        
        # Verify the zk-SNARK proof
        is_valid = zksnark_verifier.server_verify_proof(proof_data, request.challenge)
        
        # Update session status
        session["status"] = "completed"
        session["result"] = is_valid
        session["verified_at"] = datetime.now().isoformat()
        
        verification_details = {
            "zkp_type": "zk-SNARKs",
            "proof_verified": is_valid,
            "server_learned_age": False,  # This is the key!
            "minimum_age_required": session["minimum_age"],
            "cryptographic_security": "Bilinear pairings on elliptic curves",
            "session_id": request.session_id
        }
        
        return ZKProofResponse(
            is_valid=is_valid,
            message="Age verification successful ✅" if is_valid else "Invalid proof ❌",
            verification_details=verification_details
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Proof verification failed: {e}")

@app.post("/demo-client-proof")
async def demo_client_proof(request: ClientProofRequest):
    """
    DEMO ONLY: Shows how client would generate proof
    In real implementation, this happens on client device!
    """
    try:
        # This simulates what happens on the client side
        proof_data = zksnark_verifier.client_generate_proof(
            actual_age=request.actual_age,
            minimum_age=request.minimum_age,
            challenge=request.challenge
        )
        
        if proof_data is None:
            return {
                "success": False,
                "message": "Cannot generate proof - age requirement not met",
                "note": "This demonstrates the soundness property of zk-SNARKs"
            }
        
        return {
            "success": True,
            "message": "Proof generated successfully",
            "proof_data": proof_data,
            "note": "In real implementation, actual_age never leaves client device"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo proof generation failed: {e}")

@app.get("/zkp-info")
async def zkp_info():
    """
    Information about the zk-SNARK implementation
    """
    return {
        "zkp_type": "zk-SNARKs (Zero-Knowledge Succinct Non-Interactive Arguments of Knowledge)",
        "properties": {
            "zero_knowledge": "Server never learns actual age",
            "soundness": "Cannot fake proof if age requirement not met", 
            "completeness": "Valid proof always convinces verifier",
            "succinctness": "Proof size is constant regardless of computation",
            "non_interactive": "No back-and-forth communication needed"
        },
        "cryptographic_primitives": {
            "elliptic_curves": "BN128 pairing-friendly curve",
            "bilinear_pairings": "For proof verification",
            "trusted_setup": "Required for zk-SNARK system",
            "polynomial_commitments": "Hide witness values"
        },
        "security_assumptions": {
            "discrete_log": "Elliptic curve discrete logarithm problem",
            "trusted_setup": "Setup ceremony must be honest",
            "random_oracle": "Hash functions modeled as random oracles"
        },
        "advantages": [
            "True zero-knowledge privacy",
            "Constant proof size",
            "Fast verification",
            "Non-interactive"
        ],
        "use_cases": [
            "Age verification without revealing age",
            "Income verification without revealing salary", 
            "Credential verification without revealing details",
            "Compliance checking while preserving privacy"
        ]
    }

@app.get("/active-sessions")
async def get_active_sessions():
    """
    View active verification sessions (for debugging)
    """
    return {
        "total_sessions": len(active_sessions),
        "sessions": {
            session_id: {
                "minimum_age": session["minimum_age"],
                "status": session["status"],
                "created_at": session["created_at"]
            }
            for session_id, session in active_sessions.items()
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "zkp_system": "zk-SNARKs",
        "version": "2.0.0"
    }

# Cleanup endpoint
@app.delete("/cleanup-sessions")
async def cleanup_sessions():
    """Clean up old sessions"""
    global active_sessions
    active_sessions.clear()
    return {"message": "All sessions cleared"}

if __name__ == "__main__":
    import uvicorn
    print("🔐 Starting zk-SNARKs Age Verification Server...")
    print("📚 API Documentation: http://localhost:8001/docs")
    print("🔍 ZKP Information: http://localhost:8001/zkp-info")
    uvicorn.run(app, host="0.0.0.0", port=8001)
