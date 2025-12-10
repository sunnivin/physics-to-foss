# Vertical Sky Component (VSC) Visualization

Interactive visualizations to understand the **Vertical Sky Component** calculation and the **CIE Standard Overcast Sky** model.

## 🚀 Run in Browser (No Installation!)

### Option 1: Binder
Click the badge to launch the notebooks in your browser:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/sunnivin/physics-to-foss-vgs/HEAD)

### Option 2: Google Colab
Click to open individual notebooks in Colab:

- [Interactive Coordinates Explorer](https://colab.research.google.com/github/sunnivin/physics-to-foss-vgs/blob/main/interactive_coordinates.ipynb)
- [Interactive CIE Model](https://colab.research.google.com/github/sunnivin/physics-to-foss-vgs/blob/main/interactive_cie_model.ipynb)

> Note: In Colab, run `!pip install ipywidgets` in the first cell if widgets don't work

## 📓 Notebooks

### 1. `interactive_coordinates.ipynb`
Explore **spherical coordinates** on a hemisphere:
- Understand elevation (θ) and azimuth (α) angles
- See how `z = sin(θ)` maps to height on the dome
- Visualize the coordinate transformation

### 2. `interactive_cie_model.ipynb`
Explore the **CIE Standard Overcast Sky** luminance model:
- See how `L ∝ (1 + 2·sin(θ))` varies across the sky
- Experiment with different sky models
- Understand why zenith is 3× brighter than horizon
- See which elevation bands contribute most to VSC

## 🖥️ Local Installation

```bash
# Clone the repo
git clone https://github.com/sunnivin/physics-to-foss-vgs.git
cd physics-to-foss-vgs

# Using uv (recommended)
uv sync
uv run jupyter notebook

# Or using pip
pip install -r requirements.txt
jupyter notebook
```

## 📊 Static Visualizations

Run the scripts to generate static plots:

```bash
uv run python main.py              # VSC visualizations
uv run python angles_visualization.py  # Angle visualizations
```

## 📚 Key Concepts

### CIE Standard Overcast Sky Model

$$L(\theta) = L_z \cdot \frac{1 + 2\sin(\theta)}{3}$$

| Angle | sin(θ) | Luminance Factor |
|-------|--------|------------------|
| 0° (horizon) | 0 | 1 (dim) |
| 45° | 0.71 | 2.41 |
| 90° (zenith) | 1 | 3 (bright) |

### Theoretical VSC Bounds

| Surface Orientation | VSC |
|---------------------|-----|
| Horizontal (facing up) | 100% |
| Tilted 45° | ~80% |
| Vertical | ~40% |
| Horizontal (facing down) | 0% |

## 📖 References

- CIE Standard General Sky (CIE S 011/E:2003)
- BRE Guidelines for Daylight Assessment

