# Anime Pipeline

End-to-end anime production workflow.

## Usage

```bash
# Initialize project
python scripts/generate.py init my_project --scenes 5

# Run pipeline
python scripts/generate.py run my_project/project.yaml

# Run specific stages
python scripts/generate.py run my_project/project.yaml --stages images,video
```

See [SKILL.md](SKILL.md) for full documentation.
