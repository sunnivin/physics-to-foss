"""
Vertical Sky Component (VSC) Visualization

This module visualizes the mathematical principles behind the VSC calculation,
implementing the CIE Standard Overcast Sky luminance distribution model.

Key concepts:
- CIE Standard Overcast Sky: L(ε) = Lz · (1 + 2·sin(ε)) / 3
- Lambert's Cosine Law: Φ = r · n = cos(θᵢ)
- Numerical integration over the sky hemisphere
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


# ═══════════════════════════════════════════════════════════════════════════════
# Constants (matching the CUDA implementation)
# ═══════════════════════════════════════════════════════════════════════════════

IDEAL_HORIZONTAL_SKY_COMPONENT = 7.330383  # Theoretical maximum for horizontal surface
HORIZONTAL_ANGLE_RESOLUTION = 180  # Azimuth samples
VERTICAL_ANGLE_RESOLUTION = 45     # Elevation samples

DELTA_THETA = (np.pi / 2) / VERTICAL_ANGLE_RESOLUTION
DELTA_ALPHA = (2 * np.pi) / HORIZONTAL_ANGLE_RESOLUTION


# ═══════════════════════════════════════════════════════════════════════════════
# CIE Standard Overcast Sky Model
# ═══════════════════════════════════════════════════════════════════════════════

def cie_luminance_factor(elevation_rad: np.ndarray) -> np.ndarray:
    """
    CIE Standard Overcast Sky luminance distribution.

    Formula: L(ε) = Lz · (1 + 2·sin(ε)) / 3

    We return the relative factor (1 + 2·sin(ε)) / 3, normalized so that
    the zenith (ε = 90°) has a factor of 1.0.

    Args:
        elevation_rad: Elevation angle in radians (0 = horizon, π/2 = zenith)

    Returns:
        Relative luminance factor (0.333 at horizon, 1.0 at zenith)
    """
    return (1 + 2 * np.sin(elevation_rad)) / 3


def cie_luminance_factor_code_form(rz: np.ndarray) -> np.ndarray:
    """
    CIE luminance factor as implemented in the CUDA code.

    The code uses: (1 + 2 * ray_direction.z) where ray_direction.z = sin(ε)

    This is proportional to the CIE formula, with the 1/3 normalization
    absorbed into IDEAL_HORIZONTAL_SKY_COMPONENT.

    Args:
        rz: Z-component of ray direction (0 = horizon, 1 = zenith)

    Returns:
        Luminance factor (1 at horizon, 3 at zenith)
    """
    return 1 + 2 * rz


# ═══════════════════════════════════════════════════════════════════════════════
# Sky Component Calculation
# ═══════════════════════════════════════════════════════════════════════════════

def compute_ray_directions() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute all ray directions for hemisphere sampling.

    Returns:
        Tuple of (x, y, z) coordinates for each ray direction on unit sphere
    """
    # Create angle grids
    theta = np.linspace(DELTA_THETA/2, np.pi/2 - DELTA_THETA/2, VERTICAL_ANGLE_RESOLUTION)
    alpha = np.linspace(0, 2*np.pi - DELTA_ALPHA, HORIZONTAL_ANGLE_RESOLUTION)

    THETA, ALPHA = np.meshgrid(theta, alpha)

    # Convert to Cartesian coordinates (for upward-pointing hemisphere)
    X = np.cos(THETA) * np.cos(ALPHA)
    Y = np.cos(THETA) * np.sin(ALPHA)
    Z = np.sin(THETA)

    return X, Y, Z


def compute_vsc_for_surface_normal(normal: np.ndarray) -> float:
    """
    Compute VSC for a given surface normal (unobstructed sky).

    This implements the full numerical integration without any obstructions.

    Args:
        normal: Unit vector representing the surface normal [nx, ny, nz]

    Returns:
        VSC value (percentage)
    """
    normal = normal / np.linalg.norm(normal)  # Ensure unit vector

    # Sample angles
    theta_samples = np.linspace(DELTA_THETA/2, np.pi/2 - DELTA_THETA/2, VERTICAL_ANGLE_RESOLUTION)
    alpha_samples = np.linspace(0, 2*np.pi - DELTA_ALPHA, HORIZONTAL_ANGLE_RESOLUTION)

    integral = 0.0

    for theta in theta_samples:
        for alpha in alpha_samples:
            # Ray direction in world coordinates
            rx = np.cos(theta) * np.cos(alpha)
            ry = np.cos(theta) * np.sin(alpha)
            rz = np.sin(theta)
            ray = np.array([rx, ry, rz])

            # Surface flux (Lambert's cosine law)
            surface_flux = np.dot(ray, normal)

            if surface_flux <= 0:
                continue  # Back-facing

            # CIE luminance factor
            cie_factor = 1 + 2 * rz

            # VSC at this angle
            vsc_at_angle = surface_flux * cie_factor

            # Solid angle element
            delta_omega = np.cos(theta) * DELTA_ALPHA * DELTA_THETA

            # Accumulate
            integral += vsc_at_angle * delta_omega

    # Normalize to percentage
    return 100 * integral / IDEAL_HORIZONTAL_SKY_COMPONENT


def compute_theoretical_bounds():
    """
    Compute and explain the theoretical bounds of the VSC model.

    Returns:
        Dictionary with theoretical bounds and explanations
    """
    bounds = {}

    # Maximum: Horizontal surface facing up (normal = [0, 0, 1])
    # This is the reference case, should give ~100%
    horizontal_up = compute_vsc_for_surface_normal(np.array([0, 0, 1]))
    bounds['horizontal_up'] = horizontal_up

    # Vertical surface facing north (normal = [1, 0, 0])
    vertical_north = compute_vsc_for_surface_normal(np.array([1, 0, 0]))
    bounds['vertical_north'] = vertical_north

    # Surface tilted 45° up
    tilted_45 = compute_vsc_for_surface_normal(np.array([1, 0, 1]) / np.sqrt(2))
    bounds['tilted_45'] = tilted_45

    # Surface facing down (normal = [0, 0, -1])
    # This should give 0% (all rays are back-facing)
    horizontal_down = compute_vsc_for_surface_normal(np.array([0, 0, -1]))
    bounds['horizontal_down'] = horizontal_down

    # Compute VSC for various tilt angles
    tilt_angles = np.linspace(0, 180, 37)  # 0° = up, 90° = horizontal, 180° = down
    vsc_values = []

    for tilt in tilt_angles:
        tilt_rad = np.radians(tilt)
        normal = np.array([np.sin(tilt_rad), 0, np.cos(tilt_rad)])
        vsc = compute_vsc_for_surface_normal(normal)
        vsc_values.append(vsc)

    bounds['tilt_angles'] = tilt_angles
    bounds['vsc_vs_tilt'] = np.array(vsc_values)

    return bounds


# ═══════════════════════════════════════════════════════════════════════════════
# Visualization Functions
# ═══════════════════════════════════════════════════════════════════════════════

def plot_cie_luminance_distribution():
    """Plot the CIE Standard Overcast Sky luminance distribution."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    elevation_deg = np.linspace(0, 90, 100)
    elevation_rad = np.radians(elevation_deg)

    # Standard form (normalized, 0.333 to 1.0)
    luminance_normalized = cie_luminance_factor(elevation_rad)

    # Code form (proportional, 1.0 to 3.0)
    rz = np.sin(elevation_rad)
    luminance_code = cie_luminance_factor_code_form(rz)

    # Left plot: Standard CIE form
    ax1 = axes[0]
    ax1.plot(elevation_deg, luminance_normalized, 'b-', linewidth=2.5)
    ax1.axhline(y=1/3, color='gray', linestyle='--', alpha=0.7, label='Horizon (1/3)')
    ax1.axhline(y=1.0, color='gray', linestyle=':', alpha=0.7, label='Zenith (1.0)')
    ax1.set_xlabel('Elevation Angle ε (degrees)', fontsize=12)
    ax1.set_ylabel('Relative Luminance L(ε)/Lz', fontsize=12)
    ax1.set_title('CIE Standard Overcast Sky\nL(ε) = Lz · (1 + 2·sin(ε)) / 3', fontsize=13)
    ax1.set_xlim(0, 90)
    ax1.set_ylim(0, 1.1)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='lower right')

    # Right plot: Code implementation form
    ax2 = axes[1]
    ax2.plot(elevation_deg, luminance_code, 'r-', linewidth=2.5)
    ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.7, label='Horizon (1.0)')
    ax2.axhline(y=3.0, color='gray', linestyle=':', alpha=0.7, label='Zenith (3.0)')
    ax2.set_xlabel('Elevation Angle ε (degrees)', fontsize=12)
    ax2.set_ylabel('Luminance Factor (1 + 2·rz)', fontsize=12)
    ax2.set_title('Code Implementation Form\n(1 + 2 · ray_direction.z)', fontsize=13)
    ax2.set_xlim(0, 90)
    ax2.set_ylim(0, 3.3)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='lower right')

    # Add annotation about 3x ratio
    ax2.annotate('Sky is 3× brighter\nat zenith than horizon',
                xy=(45, 2.0), fontsize=11,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    return fig


def plot_hemisphere_sampling():
    """Visualize the hemisphere sampling pattern with CIE luminance coloring."""
    fig = plt.figure(figsize=(12, 5))

    X, Y, Z = compute_ray_directions()

    # Color by CIE luminance factor
    luminance = 1 + 2 * Z  # (1 to 3 range)

    # Left: 3D view
    ax1 = fig.add_subplot(121, projection='3d')
    scatter = ax1.scatter(X, Y, Z, c=luminance, cmap='YlOrRd', s=15, alpha=0.8)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z (up)')
    ax1.set_title(f'Sky Hemisphere Sampling\n({HORIZONTAL_ANGLE_RESOLUTION}×{VERTICAL_ANGLE_RESOLUTION} = {HORIZONTAL_ANGLE_RESOLUTION * VERTICAL_ANGLE_RESOLUTION} samples)')
    ax1.set_xlim(-1.1, 1.1)
    ax1.set_ylim(-1.1, 1.1)
    ax1.set_zlim(0, 1.1)

    cbar1 = plt.colorbar(scatter, ax=ax1, shrink=0.6, pad=0.1)
    cbar1.set_label('CIE Luminance Factor (1 + 2·rz)')

    # Right: Top-down view (projection)
    ax2 = fig.add_subplot(122)
    scatter2 = ax2.scatter(X, Y, c=luminance, cmap='YlOrRd', s=15, alpha=0.8)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('Top-Down View\n(brighter near center = zenith)')
    ax2.set_aspect('equal')
    ax2.set_xlim(-1.2, 1.2)
    ax2.set_ylim(-1.2, 1.2)

    # Add horizon circle
    theta_circle = np.linspace(0, 2*np.pi, 100)
    ax2.plot(np.cos(theta_circle), np.sin(theta_circle), 'k--', alpha=0.5, label='Horizon')
    ax2.legend()

    cbar2 = plt.colorbar(scatter2, ax=ax2, shrink=0.8)
    cbar2.set_label('CIE Luminance Factor')

    plt.tight_layout()
    return fig


def plot_vsc_contribution_map():
    """Visualize VSC contribution for each sky direction (for horizontal surface)."""
    fig = plt.figure(figsize=(14, 5))

    # Sample angles
    theta = np.linspace(DELTA_THETA/2, np.pi/2 - DELTA_THETA/2, VERTICAL_ANGLE_RESOLUTION)
    alpha = np.linspace(0, 2*np.pi - DELTA_ALPHA, HORIZONTAL_ANGLE_RESOLUTION)

    THETA, ALPHA = np.meshgrid(theta, alpha)

    # For a horizontal surface (normal = [0, 0, 1])
    # surface_flux = dot([rx, ry, rz], [0, 0, 1]) = rz = sin(theta)
    surface_flux = np.sin(THETA)

    # CIE factor
    cie_factor = 1 + 2 * np.sin(THETA)

    # VSC at angle
    vsc_at_angle = surface_flux * cie_factor

    # Solid angle element
    delta_omega = np.cos(THETA) * DELTA_ALPHA * DELTA_THETA

    # Total contribution
    contribution = vsc_at_angle * delta_omega

    # Convert to Cartesian for plotting
    R = np.cos(THETA)  # Radial distance in projection
    X = R * np.cos(ALPHA)
    Y = R * np.sin(ALPHA)

    # Left: VSC at angle (before solid angle weighting)
    ax1 = fig.add_subplot(131)
    scatter1 = ax1.scatter(X, Y, c=vsc_at_angle, cmap='plasma', s=20, alpha=0.9)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_title('VSC at Angle\n= surface_flux × CIE_factor')
    ax1.set_aspect('equal')
    plt.colorbar(scatter1, ax=ax1, label='VSC contribution')

    # Middle: Solid angle element
    ax2 = fig.add_subplot(132)
    scatter2 = ax2.scatter(X, Y, c=delta_omega, cmap='viridis', s=20, alpha=0.9)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('Solid Angle Element\n= cos(θ) × Δα × Δθ')
    ax2.set_aspect('equal')
    plt.colorbar(scatter2, ax=ax2, label='Solid angle (sr)')

    # Right: Total contribution
    ax3 = fig.add_subplot(133)
    scatter3 = ax3.scatter(X, Y, c=contribution, cmap='hot', s=20, alpha=0.9)
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_title('Total Contribution\n= VSC × solid_angle')
    ax3.set_aspect('equal')
    plt.colorbar(scatter3, ax=ax3, label='Contribution')

    plt.tight_layout()
    return fig


def plot_vsc_vs_tilt():
    """Plot VSC as a function of surface tilt angle."""
    bounds = compute_theoretical_bounds()

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(bounds['tilt_angles'], bounds['vsc_vs_tilt'], 'b-', linewidth=2.5)

    # Mark key points
    key_tilts = [0, 45, 90, 135, 180]
    key_labels = ['Up (0°)', '45° tilt', 'Vertical (90°)', '135° tilt', 'Down (180°)']

    for tilt, label in zip(key_tilts, key_labels):
        idx = np.argmin(np.abs(bounds['tilt_angles'] - tilt))
        vsc = bounds['vsc_vs_tilt'][idx]
        ax.scatter([tilt], [vsc], s=100, zorder=5)
        ax.annotate(f'{label}\nVSC={vsc:.1f}%',
                   xy=(tilt, vsc), xytext=(tilt+5, vsc+5),
                   fontsize=10, ha='left',
                   arrowprops=dict(arrowstyle='->', color='gray', alpha=0.5))

    ax.axhline(y=100, color='green', linestyle='--', alpha=0.7, label='Theoretical max (100%)')
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.7, label='Theoretical min (0%)')

    ax.set_xlabel('Surface Tilt Angle (degrees)\n0° = facing up, 90° = vertical, 180° = facing down', fontsize=12)
    ax.set_ylabel('Vertical Sky Component (%)', fontsize=12)
    ax.set_title('VSC vs. Surface Orientation (Unobstructed Sky)', fontsize=14)
    ax.set_xlim(-5, 185)
    ax.set_ylim(-5, 110)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')

    plt.tight_layout()
    return fig


def plot_theoretical_bounds_summary():
    """Create a summary visualization of theoretical bounds."""
    bounds = compute_theoretical_bounds()

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: Bar chart of key orientations
    ax1 = axes[0]
    orientations = ['Horizontal Up\n(reference)', 'Tilted 45°', 'Vertical', 'Horizontal Down']
    values = [bounds['horizontal_up'], bounds['tilted_45'],
              bounds['vertical_north'], bounds['horizontal_down']]
    colors = ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c']

    bars = ax1.bar(orientations, values, color=colors, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('VSC (%)', fontsize=12)
    ax1.set_title('VSC for Different Surface Orientations\n(Unobstructed Sky)', fontsize=14)
    ax1.set_ylim(0, 120)

    # Add value labels on bars
    for bar, val in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{val:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Add reference line at 100%
    ax1.axhline(y=100, color='gray', linestyle='--', alpha=0.7)
    ax1.text(3.5, 102, 'Reference (100%)', fontsize=10, alpha=0.7)

    # Right: Polar plot showing VSC vs azimuth for vertical surface
    ax2 = axes[1]
    ax2 = fig.add_subplot(122, projection='polar')

    azimuths = np.linspace(0, 2*np.pi, 72)
    vsc_values = []

    for azimuth in azimuths:
        normal = np.array([np.cos(azimuth), np.sin(azimuth), 0])  # Vertical surface
        vsc = compute_vsc_for_surface_normal(normal)
        vsc_values.append(vsc)

    ax2.plot(azimuths, vsc_values, 'b-', linewidth=2)
    ax2.fill(azimuths, vsc_values, alpha=0.3)
    ax2.set_title('VSC for Vertical Surface\n(varying azimuth orientation)', fontsize=14)
    ax2.set_ylabel('VSC (%)', labelpad=30)

    plt.tight_layout()
    return fig


def print_theoretical_analysis():
    """Print a comprehensive analysis of theoretical bounds."""
    print("\n" + "="*70)
    print("VERTICAL SKY COMPONENT - THEORETICAL BOUNDS ANALYSIS")
    print("="*70)

    print("\n📊 MODEL PARAMETERS:")
    print(f"   • Horizontal resolution: {HORIZONTAL_ANGLE_RESOLUTION} samples")
    print(f"   • Vertical resolution: {VERTICAL_ANGLE_RESOLUTION} samples")
    print(f"   • Total sample directions: {HORIZONTAL_ANGLE_RESOLUTION * VERTICAL_ANGLE_RESOLUTION}")
    print(f"   • Ideal horizontal sky component: {IDEAL_HORIZONTAL_SKY_COMPONENT:.6f}")

    print("\n📐 CIE STANDARD OVERCAST SKY MODEL:")
    print("   Formula: L(ε) = Lz · (1 + 2·sin(ε)) / 3")
    print("   • Horizon (ε=0°): L = Lz/3  (relative factor = 0.333)")
    print("   • Zenith (ε=90°): L = Lz    (relative factor = 1.000)")
    print("   → Sky is 3× brighter at zenith than at horizon")

    bounds = compute_theoretical_bounds()

    print("\n📏 THEORETICAL BOUNDS:")
    print("\n   MAXIMUM VSC (100%):")
    print("   • Condition: Horizontal surface facing upward")
    print("   • Surface normal: n = [0, 0, 1]")
    print(f"   • Computed value: {bounds['horizontal_up']:.2f}%")
    print("   • Physical meaning: All sky directions contribute optimally")

    print("\n   MINIMUM VSC (0%):")
    print("   • Condition: Surface facing downward OR completely obstructed")
    print("   • Surface normal: n = [0, 0, -1]")
    print(f"   • Computed value: {bounds['horizontal_down']:.2f}%")
    print("   • Physical meaning: No sky directions contribute (all back-facing)")

    print("\n   VERTICAL SURFACE:")
    print("   • Surface normal: n = [1, 0, 0] (or any horizontal direction)")
    print(f"   • Computed value: {bounds['vertical_north']:.2f}%")
    print("   • Physical meaning: Only half the sky hemisphere is visible")

    print("\n   TILTED SURFACE (45°):")
    print("   • Surface normal: n = [1/√2, 0, 1/√2]")
    print(f"   • Computed value: {bounds['tilted_45']:.2f}%")

    print("\n🔍 KEY INSIGHTS:")
    print("   1. The VSC is bounded between 0% and 100% (by definition)")
    print("   2. A horizontal surface always achieves 100% (unobstructed)")
    print("   3. A vertical surface achieves ~40% (half sky visible)")
    print("   4. Any obstruction can only REDUCE the VSC")
    print("   5. The CIE model weights zenith light more heavily")

    print("\n   PRACTICAL INTERPRETATION:")
    print("   • VSC < 27%: Significant loss of daylight (BRE guideline)")
    print("   • VSC reduction > 20%: May require further assessment")
    print("   • VSC ≈ 40%: Typical for vertical facades")
    print("   • VSC = 100%: Ideal reference case")

    print("\n" + "="*70)


def main():
    """Main function to run all visualizations."""
    print("="*70)
    print("  VERTICAL SKY COMPONENT (VSC) VISUALIZATION")
    print("  Based on CIE Standard Overcast Sky Model")
    print("="*70)

    # Print theoretical analysis
    print_theoretical_analysis()

    # Generate all plots
    print("\n📈 Generating visualizations...")

    fig1 = plot_cie_luminance_distribution()
    fig1.savefig('01_cie_luminance_distribution.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved: 01_cie_luminance_distribution.png")

    fig2 = plot_hemisphere_sampling()
    fig2.savefig('02_hemisphere_sampling.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved: 02_hemisphere_sampling.png")

    fig3 = plot_vsc_contribution_map()
    fig3.savefig('03_vsc_contribution_map.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved: 03_vsc_contribution_map.png")

    fig4 = plot_vsc_vs_tilt()
    fig4.savefig('04_vsc_vs_tilt.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved: 04_vsc_vs_tilt.png")

    fig5 = plot_theoretical_bounds_summary()
    fig5.savefig('05_theoretical_bounds_summary.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved: 05_theoretical_bounds_summary.png")

    print("\n✅ All visualizations generated successfully!")
    print("   View the PNG files to understand the VSC calculation.")

    # Show all plots
    plt.show()


if __name__ == "__main__":
    main()
