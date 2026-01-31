# Batch Producer

Batch content production for anime projects. Create multiple episodes in parallel.

## Installation

```bash
cd skills/ai-batch-producer
pip install -r requirements.txt
```

## Quick Start

### Create Batch Project

```bash
# Create 10-episode series
python scripts/generate.py create anime_series --episodes 10 --output ./projects

# Create with custom scene settings
python scripts/generate.py create short_anime --episodes 5 --duration 3.0
```

### Run Production

```bash
# Run all episodes in parallel
python scripts/generate.py run anime_series --parallel

# Run single stage (images only)
python scripts/generate.py run anime_series --stage images

# Run sequentially
python scripts/generate.py run anime_series
```

### Check Status

```bash
# Project status
python scripts/generate.py status anime_series

# All projects
python scripts/generate.py status
```

### Export All

```bash
# Export all episodes
python scripts/generate.py export anime_series --format mp4 --quality high
```

## Features

| Command | Description |
|---------|-------------|
| `create` | Create batch project with N episodes |
| `run` | Run production (sequential or parallel) |
| `status` | Check project/task status |
| `export` | Export all completed episodes |

## Project Structure

```
projects/
└── anime_series/
    ├── project.yaml          # Master config
    ├── ep01/
    │   ├── project.yaml      # Episode config
    │   ├── scenes/
    │   ├── images/
    │   └── output/
    ├── ep02/
    └── ...
```

## Workflow

```bash
# 1. Create project
python scripts/generate.py create series_01 --episodes 12

# 2. Run production
python scripts/generate.py run series_01 --parallel

# 3. Check progress
python scripts/generate.py status series_01

# 4. Export all
python scripts/generate.py export series_01 --format mp4
```

## Tips

1. **Parallel = Faster**: Use `--parallel` for multiple episodes
2. **Stagger Runs**: Start with `--stage images` for all, then video
3. **Monitor Progress**: Check status frequently during production
4. **Resume Failed**: Just re-run; completed tasks skip automatically
