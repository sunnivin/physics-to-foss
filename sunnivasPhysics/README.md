# Sunniva's Physics Journey - Marp Presentation

A personal introduction presentation: "My path to NGI"

## 📁 Structure

```
sunnivasPhysics/
├── .github/
│   └── workflows/
│       └── build-slides.yml    # GitHub Actions to build PDF/HTML
├── talk/
│   ├── figures/
│   │   ├── illustrations/      # Presentation images
│   │   └── logos/              # University/company logos
│   ├── slides.md               # The presentation
│   ├── theme.css               # Custom theme
│   └── README.md               # How to build locally
└── README.md                   # This file
```

## 🚀 Quick Start

### Local Preview (VS Code)
1. Install [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
2. Open `talk/slides.md`
3. Press `Cmd+Shift+P` → "Marp: Open Preview"

### Local Preview (Docker)
```bash
cd talk
docker run --rm --init -v $PWD:/home/marp/app \
  -p 8080:8080 -p 37717:37717 \
  marpteam/marp-cli:v3.4.0 --theme theme.css --watch -s --html .
```
Then open http://localhost:8080/

### Export to PDF
```bash
cd talk
docker run --rm -v $PWD:/home/marp/app/ \
  -e MARP_USER="$(id -u):$(id -g)" \
  marpteam/marp-cli:v3.4.0 --theme theme.css slides.md --pdf
```

## 🔧 GitHub Actions

The repository includes a GitHub Actions workflow that:
- ✅ Builds HTML slides on every push
- ✅ Builds PDF slides
- ✅ Deploys to GitHub Pages (optional)

### Enable GitHub Pages
1. Go to repo Settings → Pages
2. Set Source to "GitHub Actions"
3. Push to main branch
4. Your slides will be at: `https://sunnivin.github.io/REPO_NAME/`

## 📷 Adding Images

Place images in `talk/figures/`:
- `illustrations/` - Presentation graphics
- `logos/` - University/company logos

Reference in slides:
```markdown
![](figures/illustrations/my-image.png)
![bg right w:400](figures/logos/ntnu-logo.png)
```

## 🎨 Theme Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Raspberry | `#F80F50` | Highlights |
| Night Blue | `#003B7B` | Headers |
| Dark Gray | `#323232` | Body text |

