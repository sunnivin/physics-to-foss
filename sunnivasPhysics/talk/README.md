# Slides with Marp

This folder contains slides written in Markdown using [Marp](https://marp.app/).

## 📁 Structure

```
talk/
├── figures/
│   ├── illustrations/     # Presentation graphics
│   │   ├── iam/           # Personal journey images
│   │   ├── lyrgus/        # Lycurgus cup photos
│   │   ├── saint_gobain/  # Mirror/thin film illustrations
│   │   ├── granfilm_output/
│   │   └── ...
│   └── logos/             # University/company logos
├── slides.md              # The presentation
├── theme.css              # Custom theme
└── README.md              # This file
```

## 🖼️ Required Images

The presentation needs the following images to be placed in `figures/`:

### Logos (`figures/logos/`)
- `ntnu.png` - NTNU logo
- `logo-UNSAM.png` - UNSAM logo
- `sorbonne2.png` - Sorbonne Université logo
- `sgr.png` - Saint-Gobain Research logo
- `UiO_Seal_A_ENG.png` - UiO logo
- `NGI_logo_rgb.png` - NGI logo

### Illustrations (`figures/illustrations/`)
- `iam/the_world.png` - World map for journey
- `iam/physics.png` - Physics illustration
- `iam/communication.png` - Communication illustration
- `iam/female_tech.png` - Technology illustration
- `iam/violin.png` - Music/violin image
- `iam/culture.png` - Culture illustration
- `iam/knitting.png` - Knitting illustration
- `iam/dna.png` - DNA structure
- `iam/fiber_bundle_model.png` - Fiber bundle model diagram
- `lyrgus/lyrgus_trans.png` - Lycurgus cup (transmitted light)
- `lyrgus/lyrgus_ref.png` - Lycurgus cup (reflected light)
- `saint_gobain/matrix.png` - Layer matrix diagram
- `saint_gobain/mirror_big.png` - Mirror image
- `saint_gobain/thin_film.png` - Thin film illustration
- `granfilm_output/sem_cutted.png` - SEM image of Ag/MgO
- `granfilm_output/theory_exp.png` - Theoretical vs experimental curves
- `lazzari/SDRS.png` - SDRS diagram
- `excess_fields_explained/begining_growth.png` - Layer growth beginning
- `excess_fields_explained/system_sketch.png` - System sketch
- `code_quality/computational_science.png` - Computational science illustration
- `code_quality/git_evangelist.png` - Git evangelist image

## 🚀 Local Preview

### Option 1: VS Code Extension
1. Install [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
2. Open `slides.md`
3. Press `Cmd+Shift+P` → "Marp: Open Preview"

### Option 2: Docker (with hot reload)
```bash
docker run --rm --init -v $PWD:/home/marp/app \
  -e LANG=$LANG -p 8080:8080 -p 37717:37717 \
  marpteam/marp-cli:v3.4.0 --theme theme.css --watch -s --html .
```
Open http://localhost:8080/ and click on `slides.md`

### Option 3: Marp CLI
```bash
# Install: npm install -g @marp-team/marp-cli
marp --theme-set theme.css --html -w slides.md
```

## 📄 Export

### PDF Export
```bash
docker run --rm -v $PWD:/home/marp/app/ \
  -e MARP_USER="$(id -u):$(id -g)" -e LANG=$LANG \
  marpteam/marp-cli:v3.4.0 --theme theme.css slides.md --pdf --allow-local-files
```

### HTML Export
```bash
docker run --rm -v $PWD:/home/marp/app/ \
  -e MARP_USER="$(id -u):$(id -g)" -e LANG=$LANG \
  marpteam/marp-cli:v3.4.0 --theme theme.css slides.md --html
```

## 🎨 Theme Colors

The theme uses NGI-inspired colors:
- **Raspberry**: `#F80F50` - highlights and accents
- **Night Blue**: `#003B7B` - section headers
- **Dark Gray**: `#323232` - body text

## 📝 Tips

- Use `<!-- _class: title -->` for title slides
- Use `<!-- _class: section-header -->` for section dividers
- Use `![bg right:50%](image.png)` for background images
- Use `<!-- _footer: 'Credit' -->` for attributions
