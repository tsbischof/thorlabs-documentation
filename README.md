# thorlabs_documentation
Bulk downloading of documentation from Thorlabs. 
Currently this is just the main documents like CAD models, manuals, etc.
This does not include software, spectra, or the like.

## Installing
```
cd thorlabs_documentation
pip install .
```

## Examples
Download documents for a single part:
```
fetch_thorlabs TR50/M
```

Or multiple parts:
```
fetch_thorlabs TR50/M SM1L05
```

## Contributing
See the [Github page](https://github.com/tsbischof/thorlabs_documentation)
