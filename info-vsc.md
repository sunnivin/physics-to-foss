# Vertical Sky Component (VSC) for Daylight Calculation

## Overview

The sky-view analysis backend calculates the **Vertical Sky Component (VSC)** contribution of daylight, which measures the proportion of sky visible from a point on a vertical surface. This is a key metric in daylight analysis for building design.

## Standard Equation

The Vertical Sky Component is calculated using the following formula:

### General Form

```
VSC = (1/π) × ∫∫ cos(θ) × cos(α) dω
```

Where:
- **VSC** = Vertical Sky Component (dimensionless, range 0-1)
- **θ** = Zenith angle (angle from vertical direction)
- **α** = Angle between the surface normal and the direction to the sky patch
- **dω** = Solid angle element
- **π** = Pi (normalization constant)
- The integral is taken over the **visible sky hemisphere**

### Physical Meaning

- **VSC = 1.0**: Complete unobstructed view of the sky (100% sky visible)
- **VSC = 0.0**: No sky visible (completely obstructed)
- **VSC = 0.5**: Half of the sky hemisphere is visible

## Implementation in This Codebase

### Architecture

The actual sky view factor calculation is **not performed in this Python codebase**. Instead:

1. **This Backend** (`sky-view-analysis-backend`):
   - Prepares observation points (ground and roof surfaces)
   - Sends 3D meshes and observation points to GPU worker
   - Receives calculated scores from GPU worker
   - Normalizes and stores results

2. **GPU Worker** (`analysis-gpu-jsworker`):
   - Performs the actual sky view factor calculation
   - Uses ray-casting or similar algorithms
   - Integrates over the sky hemisphere
   - Returns scores in range 0-100

### Code Location

The normalization of GPU results happens in:

```python
# state_machine/collect_results/process.py (lines 42, 54)
scores[ground_scores_mask] = ground_scores / 100
scores[roof_scores_mask] = roof_scores / 100
```

This converts GPU scores (0-100) to sky view factors (0-1).

### Data Flow

```
1. Input: 3D meshes (buildings, terrain) + observation points
   ↓
2. GPU Worker: Calculates sky view factors using VSC equation
   ↓
3. Returns: Scores (0-100 range)
   ↓
4. Backend: Normalizes scores / 100 → (0-1 range)
   ↓
5. Output: Sky view factor values stored in H5 files
```

## Key Components

### Observation Points

- **Ground points**: Grid points on terrain surfaces
- **Roof points**: Points on roof surfaces (filtered by `maxHorizontalRoofAngleDegrees`)

### Obstructions

The calculation accounts for:
- **Blocking meshes**: Buildings and structures
- **Terrain meshes**: Ground elevation
- **Vegetation meshes**: Trees and plants

### Surface Normals

For vertical surfaces, the calculation uses:
- Surface normal vectors to determine the angle `α`
- Cosine weighting to account for surface orientation

## References

The Vertical Sky Component follows standard daylight calculation methods, typically based on:

- **CIE (Commission Internationale de l'Éclairage)** standards
- **British Standard BS 8206-2** (Daylight in buildings)
- Integration over the sky hemisphere with cosine weighting

## Notes

- The actual implementation details (ray-casting algorithm, sampling method, etc.) are in the GPU worker codebase
- The division by 100 in this codebase is purely for normalization
- Values are stored as float arrays in H5 format for efficient retrieval
- Results can be visualized as textures/sprites via the API endpoints

