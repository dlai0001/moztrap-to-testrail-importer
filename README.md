# MozTrap TestRail Importer

Import your MozTrap Test Suites into TestRail

## Requirements
- Python 3
- `pip install -r requirements.txt` to install dependencies.

## Instructions

1. Edit config.py and enter your TestRail API credentials and URL config for
both TestRail and MozTrap.
2. Run the importer passing in the target suite to export from, and import to.

      #> python importer [moztrap suite id] [testrail suiteid]
