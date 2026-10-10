import numpy as np
import matplotlib.pyplot as plt

def generate_radial_simulation_plot():
    """
    Generates and renders the 1D Radial Lattice Simulation mapping
    the transition of the running coupling function and field divergence
    across the Stall Horizon boundary layer (Equations 14-17).
    """
    # ==========================================================================
    # 1. ESTABLISH DIMENSIONLESS RADIAL MESH (Section 9)
    # ==========================================================================
    # Radial coordinate distance r, scaled so the Stall Horizon aligns at r = 1.0
    r = np.linspace(0.0, 2.25, 500)

    # ==========================================================================
    # 2. PHENOMENOLOGICAL CORE PARAMETERS (Scaled)
    # ==========================================================================
    beta_0 = 1.0       # Minkowski flat spacetime temporal constant
    K_constant = 1.0   # Dimensionless Chronovacuum Equivalence constant (\u1703)
    Lambda_sq = 0.01   # Planck-scale regulator preventing metric division singularities

    # ==========================================================================
    # 3. GRAVITATIONAL COLLAPSE CORE DYNAMICS
    # ==========================================================================
    # Exponential mass-energy density accumulation spikes near the core center (r -> 0)
    rho = np.exp(-3.0 * (r - 1.0)) 
    
    # Spacetime Ricci scalar curvature scaling inversely with radial coordinate position
    Ricci_R = 1.0 / (r + 0.1)      

    # ==========================================================================
    # 4. CHRONODYNAMICS COUPLING PIPELINE (Equations 14-17)
    # ==========================================================================
    # Calculating the mechanical stress load ratio within the continuous vacuum fabric
    stress_ratio = (K_constant * rho) / (Ricci_R + Lambda_sq)

    # Equation 14: The Running Thermodynamic Coupling Function
    beta = beta_0 * (1.0 - stress_ratio)

    # Equation 16 & 17: Covariant Chronal Field Divergence Evolution
    field_divergence = 1.2 * (1.0 - stress_ratio)

    # ==========================================================================
    # 5. HIGH-DPI VISUAL EDITING PIPELINE (Figure 1 Blueprint)
    # ==========================================================================
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

    # Plotting continuous tensor field evolution lines
    ax.plot(r, beta, label=r'Running Coupling $\beta(\rho, R)$', color='#002060', linewidth=2.5)
    ax.plot(r, field_divergence, label=r'Field Divergence $\nabla_\mu T^\mu(r)$', color='#FF3300', linestyle='--', linewidth=2.5)

    # Visual Coordinate Anchors for Phase Boundaries
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(1.0, color='red', linestyle=':', linewidth=1.5)
    ax.scatter([1.0], [0.0], color='black', zorder=5)

    # Equation 16 Dynamic Callout: Labeling the Stall Horizon Phase Interface
    ax.annotate(r'Stall Horizon ($r_{\rm stall}$)', xy=(1.0, 0.0), xytext=(1.15, 0.4),
                arrowprops=dict(facecolor='black', arrowstyle='->'),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF2CC', edgecolor='grey'))

    # Shading the Multi-Sheet Topology Operational Domains (Section VIII)
    ax.axvspan(0.0, 1.0, facecolor='#EAD8ED', alpha=0.5, label='Phase III: Causal Echo Core')
    ax.axvspan(1.0, 2.25, facecolor='#EAF7F0', alpha=0.5, label='Phase I: Steady-State Advection')

    # Canvas Presentation Formatting
    ax.set_title('Figure 1: Numerical 1D Radial Lattice Simulation', fontsize=14, pad=15)
    ax.set_xlabel('Radial Distance $r$ (arbitrary scaled units)', fontsize=12)
    ax.set_ylabel('Amplitude', fontsize=12)
    ax.set_xlim(0.0, 2.25)
    ax.set_ylim(-1.5, 1.5)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='lower right', framealpha=0.95)

    # Render clean output
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Test script locally when run independently
    generate_radial_simulation_plot()
