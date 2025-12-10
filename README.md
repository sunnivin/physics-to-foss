# Physics to FOSS

A collection of talks and interactive notebooks exploring the journey from physics to free and open-source software.

## 📁 Repository Structure

```
physics-to-foss/
├── sunnivasPhysics/          # "My Path to NGI" presentation
│   └── talk/
│       ├── slides.md         # Marp presentation
│       ├── theme.css         # Custom theme
│       └── figures/          # Images and logos
│
└── vertical-sky-component/   # Interactive VSC visualizations
    ├── interactive_coordinates.ipynb
    ├── interactive_cie_model.ipynb
    ├── main.py
    └── angles_visualization.py
```

## 🚀 Interactive Notebooks

Explore the **Vertical Sky Component (VSC)** and **CIE Standard Overcast Sky** model in your browser:

### Binder (recommended)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/sunnivin/physics-to-foss/HEAD?labpath=vertical-sky-component)

**Direct notebook links:**
- [Interactive Coordinates Explorer](https://mybinder.org/v2/gh/sunnivin/physics-to-foss/HEAD?labpath=vertical-sky-component%2Finteractive_coordinates.ipynb)
- [Interactive CIE Model](https://mybinder.org/v2/gh/sunnivin/physics-to-foss/HEAD?labpath=vertical-sky-component%2Finteractive_cie_model.ipynb)

### Google Colab

- [Interactive Coordinates Explorer](https://colab.research.google.com/github/sunnivin/physics-to-foss/blob/main/vertical-sky-component/interactive_coordinates.ipynb)
- [Interactive CIE Model](https://colab.research.google.com/github/sunnivin/physics-to-foss/blob/main/vertical-sky-component/interactive_cie_model.ipynb)

> **Note:** In Colab, run `!pip install ipywidgets` in the first cell if widgets don't display.

## 🎤 Presentations

### My Path to NGI (`sunnivasPhysics/`)

A personal journey through physics, plasmonics, and scientific software development.

**Build locally:**
```bash
cd sunnivasPhysics/talk
docker run --rm -v "$(pwd):/home/marp/app" -p 8080:8080 marpteam/marp-cli --theme theme.css --html -s .
# Open http://localhost:8080/slides.md
```


## 🛠️ Local Development

### VSC Notebooks

```bash
cd vertical-sky-component

# Using uv (recommended)
uv sync
uv run jupyter notebook

# Or using pip
pip install -r requirements.txt
jupyter notebook
```

### Generate Static Plots

```bash
cd vertical-sky-component
uv run python main.py               # VSC visualizations
uv run python angles_visualization.py   # Angle visualizations
```

## 📖 References

- CIE Standard General Sky (CIE S 011/E:2003)
- BRE Guidelines for Daylight Assessment

