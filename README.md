# Walter P. Reuther Library Digitization Utilities

This repository contains Python utilities to assist the Walter P. Reuther Library in its preservation digitization efforts. The utilities currently provide helper functions for setting up projects and working with individual items within those projects, including setting up directory structures, enforcing filenaming conventions, and generating derivatives.

## Requirements
- Python 3
- Ghostscript
- OpenJPEG
- ocrmypdf

## Installation

- Ensure that the above requirements are installed on your computer
- `git clone` this repository
- `cd reuther_digitization_utils`
- `pip install .`

## Use

The utilities consist of two primary utility classes: `ProjectUtils` and `ItemUtils`

### Projects

`reuther_digitization_utils/project_utils.py` defines a `ProjectUtils` class that requires the following parameters:

- `project_base_dir`: A directory where the project will be initialized
- `project_csv`: A CSV, exported from ArchivesSpace, containing the following information for each item: 
    - `component_id`: This serves as the directory/filenaming structure base and should be of the form `[collection_id]_[part_#]_[series_#]_[subseries_#]_[box_#]_[folder_#]`
    - `title`
    - `dates`
    - `box`
    - `folder`
    - `uri`: The ArchivesSpace URI for the corresponding archival object

Instantiating a project and calling the `setup_project` class function will create a directory structure at `project_base_dir` with one subdirectory for the project's collection ID, one or more subdirectories per item within the collection directory, and an access and preservation directory within each item directory.

```python
from reuther_digitization_utils.project_utils import ProjectUtils
project_base_dir = '/path/to/project/directory'
project_csv = '/path/to/project.csv'
project = ProjectUtils(project_base_dir, project_csv)
project.setup_project()
```

```
project_base_dir\
    collection_id\ <-- e.g., LR000261
        component_id_1\ <-- e.g., LR000261_00_16_A_546_003
            access\
            preservation\
        component_id_2\ <-- e.g., LR000261_00_16_A_546_004
            access\
            preservation\
        ...
```

### Items

`reuther_digitization_utils/item_utils.py` defines an `ItemUtils` class that requires the following parameters:

- `collection_dir`: Path to a directory containing the item, e.g. `/path/to/project_base_dir/LR000261`
- `item_identifier`: Component ID for the specific item, e.g. `LR000261_00_16_A_546_003`

```python
from reuther_digitization_utils.item_utils import ItemUtils
collection_dir = '/path/to/project_base_dir/LR000261'
item_identifier = 'LR000261_00_16_A_546_003'
item = ItemUtils(collection_dir, item_identifier)
item.rename_preservation_scans()
item.generate_derivatives()
```

#### Filenaming

The `renaming_preservation_scans` class function will rename scanned images in the item's `preservation` directory according to the Reuther's filenaming convention.

#### Derivatives

The `generate_derivatives` class function will generate derivative image files (currently only JPEG 2000) and a combined, compressed, and OCR'd PDF in the item's `access` directory.
