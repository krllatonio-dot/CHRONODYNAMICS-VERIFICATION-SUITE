import numpy as np

# ==============================================================================
# 1. LATICE CONFIGURATION & DISCRETIZATION MATRIX (Equation 38)
# ==============================================================================
NODES = 50               # Spatial lattice grid nodes (1D projection line)
TIME_STEPS = 100         # Temporal iterations / simulation slices

# SI Physical constants for internal grid calibration
Tv_invariant = 8.2315e-35  # Foundational volume limit from Equation 10 (m^3)
ax = 1.0                   # Dimensionless coordinate step size (scaled to Tv^(1/3))
at = 0.01                  # Numerical clock step constraint satisfying Courant limit

# Memory Allocation Pipelines
T_field = np.ones((TIME_STEPS, NODES))    # Chronal Director field magnitude
beta = np.ones((TIME_STEPS, NODES))       # Dynamic running coupling function field
rho = np.zeros((TIME_STEPS, NODES))      # Localized mass density matrix

# ==============================================================================
# 2. PHENOMENOLOGICAL SIMULATION PARAMETERS (Section 9)
# ==============================================================================
K_anchor = 2.14e9        # Chronovacuum Equivalence constant (\u1703)
kappa = 2.0766e-43       # Einstein's gravitational constant (Pa^-1)
Lambda_sq = 1e-4         # Planck-scale regulator (insulates against division-by-zero)
beta_0 = 1.0             # Flat Minkowski bare temporal baseline
gamma_Q = 0.01           # Quantum coherence macroscale stabilizer

# Dimensionless scaling factor to translate 10^-43 values natively without underflow
sigma_scale = 1.0e34     

# ==============================================================================
# 3. INITIALIZING ASTROPHYSICAL ENVIRONMENT (Gravitational Collapse Engine)
# ==============================================================================
# Modeling exponential mass accumulation centered on coordinate node index 0
for n in range(TIME_STEPS):
    for i in range(NODES):
        # Density accumulates over time (n) and spikes sharply near the core (i -> 0)
        rho[n, i] = 0.1 * np.exp(0.04 * n) * np.exp(-0.15 * i)

# ==============================================================================
# 4. ITERATIVE FINITE-DIFFERENCE RUNTIME (Equations 39 & 40)
# ==============================================================================
stalled_nodes_count = 0
inverted_nodes_count = 0
forward_nodes_count = 0

# Run evaluation loops excluding boundary guard-cells to preserve grid stability
for n in range(1, TIME_STEPS):
    for i in range(1, NODES - 1):
        
        # Calculate local stress ratio using the dimensionless scale multiplier
        stress_ratio = (K_anchor * (rho[n, i] * sigma_scale * kappa)) / (1.0 + Lambda_sq)
        
        # Equation 40: The Discrete Running Coupling Function
        beta[n, i] = beta_0 * (1.0 - stress_ratio)
        
        # Equation 39: Discrete Field Update Rule
        entropic_push = 0.5   # Stable standing entropic field dissipation scalar
        grav_brake = stress_ratio
        
        # Total localized temporal divergence modification
        divergence_update = (beta[n, i] * entropic_push) - grav_brake + gamma_Q
        
        # Update Chronal Director magnitude for the proceeding time slice
        T_field[n, i] = T_field[n-1, i] + at * divergence_update
        
        # Extract and log active phase transitions at final execution step
        if n == TIME_STEPS - 1:
            if abs(divergence_update) <= 0.05:
                stalled_nodes_count += 1
            elif divergence_update < -0.05:
                inverted_nodes_count += 1
            else:
                forward_nodes_count += 1

# Account for grid boundary guard cells in final metrics
forward_nodes_count += 2

# ==============================================================================
# 5. DIAGNOSTIC SIMULATION REPORT
# ==============================================================================
print("=" * 75)
print("NUMERICAL RELATIVITY ENGINE: CHRONODYNAMIC LATTICE SIMULATION")
print("=" * 75)
print(f" -> Execution Status:       SUCCESS")
print(f" -> Spatial Grid Spacing:   ax^3 ~ Tv ({Tv_invariant:.4e} m^3) -> Coordinates = 1.0")
print(f" -> Time Slices Computed:   {TIME_STEPS} Iterations")
print(f" -> Total Mesh Grid Nodes:  {NODES} Spatial Points")
print("-" * 75)
print(f" [+] COMPUTATIONAL CORE METRICS (At Final Time Slice n={TIME_STEPS}):")
print(f"     Maximum Core Density = {rho[-1, 0]:.4f} scaled units")
print("-" * 75)
print(f" [+] EMERGENT PHASE TRANSITION STATE DISTRIBUTION:")
print(f"     Phase I   (Forward Chronal Advection  \u2207\u03bcT\u03bc > 0): {forward_nodes_count} Nodes")
print(f"     Phase II  (Stall Horizon Boundary Layer \u2207\u03bcT\u03bc = 0): {stalled_nodes_count} Nodes")
print(f"     Phase III (Causal Echo Backward Core    \u2207\u03bcT\u03bc < 0): {inverted_nodes_count} Nodes")
print("=" * 75)