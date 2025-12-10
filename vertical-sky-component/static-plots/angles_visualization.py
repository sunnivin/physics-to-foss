"""
Visualization of Spherical Coordinates on a Hemisphere

This script helps build intuition about how elevation (θ) and azimuth (α)
angles map onto a hemisphere representing the sky dome.

Terminology:
- Elevation angle (θ): Angle from horizon (0° = horizon, 90° = zenith)
- Zenith angle (γ): Angle from zenith (0° = zenith, 90° = horizon)
  Note: γ = 90° - θ, so sin(θ) = cos(γ)
- Azimuth angle (α): Horizontal rotation (0° to 360°)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def spherical_to_cartesian(elevation_rad, azimuth_rad, radius=1.0):
    """
    Convert spherical coordinates to Cartesian.

    Args:
        elevation_rad: Elevation angle from horizon (radians)
        azimuth_rad: Azimuth angle (radians)
        radius: Sphere radius

    Returns:
        x, y, z coordinates
    """
    x = radius * np.cos(elevation_rad) * np.cos(azimuth_rad)
    y = radius * np.cos(elevation_rad) * np.sin(azimuth_rad)
    z = radius * np.sin(elevation_rad)
    return x, y, z


def plot_elevation_rings():
    """Show how elevation angle creates horizontal rings on the dome."""
    fig = plt.figure(figsize=(16, 6))

    # 3D view
    ax1 = fig.add_subplot(131, projection='3d')

    azimuth = np.linspace(0, 2*np.pi, 100)
    elevations = [0, 15, 30, 45, 60, 75, 90]  # degrees
    colors = cm.viridis(np.linspace(0, 1, len(elevations)))

    for elev_deg, color in zip(elevations, colors):
        elev_rad = np.radians(elev_deg)
        x, y, z = spherical_to_cartesian(elev_rad, azimuth)

        if elev_deg == 90:  # Zenith is a point
            ax1.scatter([0], [0], [1], c=[color], s=100, label=f'θ = {elev_deg}° (zenith)')
        else:
            ax1.plot(x, y, z, c=color, linewidth=2, label=f'θ = {elev_deg}°')

    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z (up)')
    ax1.set_title('Elevation Angle (θ)\nRings of constant elevation')
    ax1.legend(loc='upper left', fontsize=8)
    ax1.set_xlim(-1.1, 1.1)
    ax1.set_ylim(-1.1, 1.1)
    ax1.set_zlim(0, 1.1)

    # Side view (X-Z plane)
    ax2 = fig.add_subplot(132)

    for elev_deg, color in zip(elevations, colors):
        elev_rad = np.radians(elev_deg)
        # Draw arc in X-Z plane
        theta_range = np.linspace(0, np.pi, 50)
        x = np.cos(elev_rad) * np.cos(theta_range)
        z = np.sin(elev_rad) * np.ones_like(theta_range)
        ax2.axhline(y=np.sin(elev_rad), color=color, linewidth=2,
                   label=f'θ = {elev_deg}°, z = {np.sin(elev_rad):.2f}')

    # Draw dome outline
    theta_outline = np.linspace(0, np.pi/2, 50)
    ax2.plot(np.cos(theta_outline), np.sin(theta_outline), 'k--', alpha=0.3)
    ax2.plot(-np.cos(theta_outline), np.sin(theta_outline), 'k--', alpha=0.3)

    ax2.set_xlabel('X')
    ax2.set_ylabel('Z (height)')
    ax2.set_title('Side View\nz = sin(θ)')
    ax2.set_aspect('equal')
    ax2.set_xlim(-1.2, 1.2)
    ax2.set_ylim(-0.1, 1.2)
    ax2.legend(fontsize=8, loc='upper right')
    ax2.grid(True, alpha=0.3)

    # Top-down view showing radial distance
    ax3 = fig.add_subplot(133)

    for elev_deg, color in zip(elevations, colors):
        elev_rad = np.radians(elev_deg)
        r = np.cos(elev_rad)  # Radial distance in projection
        circle = plt.Circle((0, 0), r, fill=False, color=color, linewidth=2,
                           label=f'θ = {elev_deg}°, r = {r:.2f}')
        ax3.add_patch(circle)

    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_title('Top-Down View\nradius = cos(θ)')
    ax3.set_aspect('equal')
    ax3.set_xlim(-1.3, 1.3)
    ax3.set_ylim(-1.3, 1.3)
    ax3.legend(fontsize=8, loc='upper right')
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_azimuth_lines():
    """Show how azimuth angle creates radial lines on the dome."""
    fig = plt.figure(figsize=(16, 6))

    # 3D view
    ax1 = fig.add_subplot(131, projection='3d')

    elevation = np.linspace(0, np.pi/2, 50)
    azimuths = np.linspace(0, 360, 13)[:-1]  # 0, 30, 60, ..., 330 degrees
    colors = cm.hsv(np.linspace(0, 1, len(azimuths)))

    for azim_deg, color in zip(azimuths, colors):
        azim_rad = np.radians(azim_deg)
        x, y, z = spherical_to_cartesian(elevation, azim_rad)
        ax1.plot(x, y, z, c=color, linewidth=2, label=f'α = {int(azim_deg)}°')

    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z (up)')
    ax1.set_title('Azimuth Angle (α)\nRadial lines from center')
    ax1.legend(loc='upper left', fontsize=7, ncol=2)
    ax1.set_xlim(-1.1, 1.1)
    ax1.set_ylim(-1.1, 1.1)
    ax1.set_zlim(0, 1.1)

    # Top-down view
    ax2 = fig.add_subplot(132)

    for azim_deg, color in zip(azimuths, colors):
        azim_rad = np.radians(azim_deg)
        x_end = np.cos(azim_rad)
        y_end = np.sin(azim_rad)
        ax2.plot([0, x_end], [0, y_end], c=color, linewidth=2,
                label=f'α = {int(azim_deg)}°')
        ax2.scatter([x_end], [y_end], c=[color], s=50)

    # Horizon circle
    theta = np.linspace(0, 2*np.pi, 100)
    ax2.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.3, label='Horizon')

    ax2.set_xlabel('X = cos(α)')
    ax2.set_ylabel('Y = sin(α)')
    ax2.set_title('Top-Down View\nAzimuth = rotation angle')
    ax2.set_aspect('equal')
    ax2.set_xlim(-1.3, 1.3)
    ax2.set_ylim(-1.3, 1.3)
    ax2.legend(fontsize=7, loc='upper right', ncol=2)
    ax2.grid(True, alpha=0.3)

    # Azimuth as color wheel
    ax3 = fig.add_subplot(133, projection='polar')

    r = np.linspace(0, 1, 50)
    theta = np.linspace(0, 2*np.pi, 360)
    R, THETA = np.meshgrid(r, theta)

    # Color by azimuth
    ax3.pcolormesh(THETA, R, np.degrees(THETA), cmap='hsv', shading='auto')
    ax3.set_title('Azimuth Color Wheel\n(color = azimuth angle)')
    ax3.set_rticks([])

    plt.tight_layout()
    return fig


def plot_combined_grid():
    """Show the full sampling grid with both angles varying."""
    fig = plt.figure(figsize=(16, 12))

    # Create sample points
    n_elevation = 9  # 0, 10, 20, ..., 80 degrees
    n_azimuth = 12   # 0, 30, 60, ..., 330 degrees

    elevations = np.linspace(0, 80, n_elevation)  # degrees
    azimuths = np.linspace(0, 330, n_azimuth)     # degrees

    # 3D view - colored by elevation
    ax1 = fig.add_subplot(221, projection='3d')

    for elev_deg in elevations:
        elev_rad = np.radians(elev_deg)
        for azim_deg in azimuths:
            azim_rad = np.radians(azim_deg)
            x, y, z = spherical_to_cartesian(elev_rad, azim_rad)
            color = cm.viridis(elev_deg / 90)
            ax1.scatter([x], [y], [z], c=[color], s=50, alpha=0.8)

    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('Sample Grid (colored by ELEVATION)\nHigher = brighter in CIE sky')
    ax1.set_xlim(-1.1, 1.1)
    ax1.set_ylim(-1.1, 1.1)
    ax1.set_zlim(0, 1.1)

    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(0, 90))
    plt.colorbar(sm, ax=ax1, label='Elevation θ (degrees)', shrink=0.6)

    # 3D view - colored by azimuth
    ax2 = fig.add_subplot(222, projection='3d')

    for elev_deg in elevations:
        elev_rad = np.radians(elev_deg)
        for azim_deg in azimuths:
            azim_rad = np.radians(azim_deg)
            x, y, z = spherical_to_cartesian(elev_rad, azim_rad)
            color = cm.hsv(azim_deg / 360)
            ax2.scatter([x], [y], [z], c=[color], s=50, alpha=0.8)

    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_title('Sample Grid (colored by AZIMUTH)\nRotation around vertical axis')
    ax2.set_xlim(-1.1, 1.1)
    ax2.set_ylim(-1.1, 1.1)
    ax2.set_zlim(0, 1.1)

    sm2 = plt.cm.ScalarMappable(cmap='hsv', norm=plt.Normalize(0, 360))
    plt.colorbar(sm2, ax=ax2, label='Azimuth α (degrees)', shrink=0.6)

    # Top-down projection with both angles labeled
    ax3 = fig.add_subplot(223)

    for elev_deg in elevations:
        elev_rad = np.radians(elev_deg)
        r = np.cos(elev_rad)  # Projected radius

        for azim_deg in azimuths:
            azim_rad = np.radians(azim_deg)
            x = r * np.cos(azim_rad)
            y = r * np.sin(azim_rad)
            color = cm.viridis(elev_deg / 90)
            ax3.scatter([x], [y], c=[color], s=50, alpha=0.8)

    # Draw elevation rings
    for elev_deg in [0, 30, 60]:
        r = np.cos(np.radians(elev_deg))
        circle = plt.Circle((0, 0), r, fill=False, color='gray',
                           linestyle='--', alpha=0.5)
        ax3.add_patch(circle)
        ax3.text(r + 0.05, 0, f'θ={elev_deg}°', fontsize=9, alpha=0.7)

    # Draw azimuth lines
    for azim_deg in [0, 90, 180, 270]:
        azim_rad = np.radians(azim_deg)
        ax3.plot([0, np.cos(azim_rad)], [0, np.sin(azim_rad)],
                'gray', linestyle='--', alpha=0.5)
        ax3.text(1.1*np.cos(azim_rad), 1.1*np.sin(azim_rad),
                f'α={azim_deg}°', fontsize=9, ha='center')

    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_title('Top-Down Projection\nCenter = zenith, Edge = horizon')
    ax3.set_aspect('equal')
    ax3.set_xlim(-1.4, 1.4)
    ax3.set_ylim(-1.4, 1.4)
    ax3.grid(True, alpha=0.2)

    # Coordinate formulas
    ax4 = fig.add_subplot(224)
    ax4.axis('off')

    formula_text = """
    SPHERICAL COORDINATES ON A HEMISPHERE
    ══════════════════════════════════════

    Angles:
    • θ (theta) = Elevation angle from horizon
      - θ = 0°  → horizon (z = 0)
      - θ = 90° → zenith  (z = 1)

    • α (alpha) = Azimuth angle (horizontal rotation)
      - α = 0°   → +X direction
      - α = 90°  → +Y direction
      - α = 180° → -X direction
      - α = 270° → -Y direction

    ══════════════════════════════════════

    Cartesian Conversion:
    ┌─────────────────────────────────────┐
    │  x = cos(θ) · cos(α)                │
    │  y = cos(θ) · sin(α)                │
    │  z = sin(θ)                         │
    └─────────────────────────────────────┘

    Key Relationships:
    • z = sin(θ)  ← Used in CIE formula: (1 + 2z)
    • Projected radius r = cos(θ)
    • At zenith: r = 0 (point at center in top view)
    • At horizon: r = 1 (edge of circle)

    ══════════════════════════════════════

    CIE Sky Luminance:
    L(θ) = Lz · (1 + 2·sin(θ)) / 3
         = Lz · (1 + 2·z) / 3

    → Zenith (z=1) is 3× brighter than horizon (z=0)
    """

    ax4.text(0.05, 0.95, formula_text, transform=ax4.transAxes,
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()
    return fig


def plot_angle_values_on_dome():
    """Annotated dome showing actual angle values at specific points."""
    fig = plt.figure(figsize=(14, 10))

    # Create a dense hemisphere surface
    u = np.linspace(0, 2*np.pi, 50)
    v = np.linspace(0, np.pi/2, 25)
    U, V = np.meshgrid(u, v)

    X = np.cos(V) * np.cos(U)
    Y = np.cos(V) * np.sin(U)
    Z = np.sin(V)

    # 3D view with elevation coloring
    ax1 = fig.add_subplot(121, projection='3d')

    # Plot surface colored by elevation
    surf = ax1.plot_surface(X, Y, Z, facecolors=cm.viridis(V / (np.pi/2)),
                           alpha=0.6, linewidth=0, antialiased=True)

    # Add specific labeled points
    labeled_points = [
        (0, 0, 'Horizon, East', 'red'),
        (0, 90, 'Horizon, North', 'blue'),
        (0, 180, 'Horizon, West', 'green'),
        (0, 270, 'Horizon, South', 'orange'),
        (45, 0, 'θ=45°, α=0°', 'purple'),
        (45, 90, 'θ=45°, α=90°', 'purple'),
        (90, 0, 'ZENITH', 'black'),
    ]

    for elev_deg, azim_deg, label, color in labeled_points:
        elev_rad = np.radians(elev_deg)
        azim_rad = np.radians(azim_deg)
        x, y, z = spherical_to_cartesian(elev_rad, azim_rad)
        ax1.scatter([x], [y], [z], c=color, s=100, zorder=5)
        ax1.text(x*1.15, y*1.15, z+0.05, label, fontsize=9, color=color)

    ax1.set_xlabel('X (East)')
    ax1.set_ylabel('Y (North)')
    ax1.set_zlabel('Z (Up)')
    ax1.set_title('Sky Dome with Labeled Points\n(color = elevation angle)')
    ax1.set_xlim(-1.3, 1.3)
    ax1.set_ylim(-1.3, 1.3)
    ax1.set_zlim(0, 1.3)

    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(0, 90))
    plt.colorbar(sm, ax=ax1, label='Elevation θ (degrees)', shrink=0.5)

    # Cross-section view showing z = sin(θ)
    ax2 = fig.add_subplot(122)

    theta_range = np.linspace(0, np.pi/2, 100)
    x_dome = np.cos(theta_range)
    z_dome = np.sin(theta_range)

    ax2.plot(x_dome, z_dome, 'b-', linewidth=3, label='Dome profile')
    ax2.plot(-x_dome, z_dome, 'b-', linewidth=3)

    # Mark specific angles
    angles_to_mark = [0, 15, 30, 45, 60, 75, 90]
    for theta_deg in angles_to_mark:
        theta_rad = np.radians(theta_deg)
        x = np.cos(theta_rad)
        z = np.sin(theta_rad)

        # Draw radial line from origin
        ax2.plot([0, x], [0, z], 'gray', linestyle='--', alpha=0.5)
        ax2.scatter([x], [z], s=80, zorder=5)

        # Add label
        ax2.annotate(f'θ={theta_deg}°\nz={z:.2f}',
                    xy=(x, z), xytext=(x+0.15, z+0.05),
                    fontsize=9, ha='left',
                    arrowprops=dict(arrowstyle='->', color='gray', alpha=0.5))

    ax2.axhline(y=0, color='brown', linewidth=2, label='Ground/Horizon')
    ax2.set_xlabel('Horizontal Distance')
    ax2.set_ylabel('Height (z)')
    ax2.set_title('Cross-Section of Sky Dome\nz = sin(θ) determines brightness in CIE model')
    ax2.set_aspect('equal')
    ax2.set_xlim(-0.2, 1.5)
    ax2.set_ylim(-0.1, 1.3)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)

    # Add formula annotation
    ax2.text(0.7, 0.5, 'CIE Luminance:\nL ∝ (1 + 2z)\n\nz=0 → L=1\nz=1 → L=3',
            fontsize=11, bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

    plt.tight_layout()
    return fig


def main():
    """Generate all angle visualization plots."""
    print("="*60)
    print("  SPHERICAL COORDINATES ON A HEMISPHERE")
    print("  Understanding Elevation and Azimuth Angles")
    print("="*60)

    print("\n📐 Generating visualizations...")

    fig1 = plot_elevation_rings()
    fig1.savefig('angles_01_elevation_rings.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved: angles_01_elevation_rings.png")
    print("     → Shows how elevation angle (θ) creates horizontal rings")
    print("     → Higher rings = closer to zenith = brighter in CIE sky")

    fig2 = plot_azimuth_lines()
    fig2.savefig('angles_02_azimuth_lines.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved: angles_02_azimuth_lines.png")
    print("     → Shows how azimuth angle (α) creates radial lines")
    print("     → Rotation around the vertical axis")

    fig3 = plot_combined_grid()
    fig3.savefig('angles_03_combined_grid.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved: angles_03_combined_grid.png")
    print("     → Shows the full sampling grid with formulas")

    fig4 = plot_angle_values_on_dome()
    fig4.savefig('angles_04_labeled_dome.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved: angles_04_labeled_dome.png")
    print("     → Annotated dome with specific angle values")

    print("\n" + "="*60)
    print("KEY INSIGHTS:")
    print("="*60)
    print("""
    1. ELEVATION (θ) - "How high in the sky?"
       • θ = 0°  → Looking at horizon (z = 0)
       • θ = 90° → Looking straight up at zenith (z = 1)
       • z = sin(θ) is used in CIE formula

    2. AZIMUTH (α) - "Which compass direction?"
       • α = 0°   → East  (+X direction)
       • α = 90°  → North (+Y direction)
       • α = 180° → West  (-X direction)
       • α = 270° → South (-Y direction)

    3. CARTESIAN CONVERSION:
       x = cos(θ) · cos(α)
       y = cos(θ) · sin(α)
       z = sin(θ)

    4. CIE SKY MODEL:
       L(θ) ∝ (1 + 2·sin(θ)) = (1 + 2z)
       → Zenith is 3× brighter than horizon
    """)

    print("\n✅ All visualizations generated!")
    plt.show()


if __name__ == "__main__":
    main()


