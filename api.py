from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from ruin import (
    gambler_ruin,
    gambler_ruin_generalized,
    gambler_ruin_with_credit,
    gambler_ruin_with_changing_bets,
    gambler_ruin_with_max_bets,
)

app = FastAPI(
    title="Gambler's Ruin Simulation API",
    description="API for simulating various gambling scenarios and calculating probabilities",
    version="1.0.0"
)

class SimulationRequest(BaseModel):
    p: Optional[float] = Field(default=0.5, ge=0.0, le=1.0, description="Probability of winning each bet")
    q: Optional[float] = Field(default=2.0, ge=1.0, description="Payout ratio when winning")
    j: Optional[int] = Field(default=1, ge=1, description="Size of each bet")
    i: Optional[int] = Field(default=10, ge=1, description="Initial amount of money")
    n: Optional[int] = Field(default=20, description="Goal amount to win")
    k: Optional[int] = Field(default=0, ge=0, description="Credit line (amount that can be borrowed)")
    m: Optional[float] = Field(default=float('inf'), ge=1, description="Maximum bet allowed per game")
    trials: Optional[int] = Field(default=10000, ge=1000, le=1000000, description="Number of simulation trials")

class SimulationResponse(BaseModel):
    success: bool
    result: dict

@app.post("/simulate", response_model=SimulationResponse)
async def simulate(request: SimulationRequest):
    try:
        # Validate that n is greater than i
        if request.n <= request.i:
            raise HTTPException(
                status_code=400,
                detail="Goal amount (n) must be greater than initial amount (i)"
            )
        
        # Validate that m is greater than or equal to j if m is provided
        if request.m != float('inf') and request.m < request.j:
            raise HTTPException(
                status_code=400,
                detail="Maximum bet (m) must be greater than or equal to bet size (j)"
            )

        # Determine which simulation to run based on provided parameters
        if request.k > 0 and request.m != float('inf'):
            result = gambler_ruin_with_max_bets(
                request.p, request.q, request.j, request.i, request.n, 
                request.k, request.m, request.trials
            )
            method = "with maximum bets and credit line"
        elif request.k > 0:
            result = gambler_ruin_with_credit(
                request.p, request.q, request.j, request.i, request.n, 
                request.k, request.trials
            )
            method = "with credit line"
        elif all(getattr(request, param) is not None for param in ['p', 'q', 'j', 'i', 'n']):
            result = gambler_ruin_generalized(
                request.p, request.q, request.j, request.i, request.n, 
                request.trials
            )
            method = "generalized"
        else:
            result = gambler_ruin(request.i, request.n, request.trials)
            method = "basic"
        
        # Calculate additional statistics
        expected_value = (request.p * request.q * request.j) - ((1-request.p) * request.j)
        max_possible_loss = request.k + request.i if request.k > 0 else request.i
        required_wins = (request.n - request.i) / (request.q * request.j)
        
        return {
            "success": True,
            "result": {
                "win_probability": result,
                "loss_probability": 1 - result,
                "method": method,
                "statistics": {
                    "expected_value_per_bet": expected_value,
                    "max_possible_loss": max_possible_loss,
                    "required_wins": required_wins
                },
                "input_parameters": {
                    "p": request.p,
                    "q": request.q,
                    "j": request.j,
                    "i": request.i,
                    "n": request.n,
                    "k": request.k,
                    "m": float(request.m) if request.m != float('inf') else "inf",
                    "trials": request.trials
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
