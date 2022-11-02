[![Build Status](https://travis-ci.com/arakhmati/rogue.svg?branch=master)](https://travis-ci.com/arakhmat/rogue)

# Rogue
Implementation of rogue using persistent data structures and entity component system

## Installation
```bash
git clone https://github.com/arakhmati/rogue
cd rogue
conda env create -f environment.yaml
conda activate rogue
pip install -e . -v
```

## Usage
### Pygcurse Renderer
```bash
conda activate rogue
rogue pygcurse configs/sample_room_config.yaml
```

### Panda3D Renderer
```bash
conda activate rogue
rogue panda3d configs/sample_room_config.yaml
```