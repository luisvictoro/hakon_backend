# Heroku Deployment Fix

## Problem
The Heroku deployment was failing due to a compatibility issue between `pydantic-core==2.14.1` and Python 3.13. The error occurred during the build process when trying to compile the Rust-based `pydantic-core` package.

## Root Cause
- `pydantic==2.5.0` was pinned to an older version that included `pydantic-core==2.14.1`
- `pydantic-core==2.14.1` has compatibility issues with Python 3.13
- The build process failed during Rust compilation with a `ForwardRef._evaluate()` error

## Solution

### 1. Updated Pydantic Version
Changed `requirements.txt`:
```diff
- pydantic==2.5.0
+ pydantic>=2.6.0
```

This allows pip to install a newer version of pydantic that includes a compatible version of pydantic-core.

### 2. Added Python Version Specification
Created `.python-version` file:
```
3.13
```

This explicitly tells Heroku to use Python 3.13, eliminating the warning about unspecified Python version.

### 3. Updated Pydantic Schema Syntax
Updated the pydantic model configurations to use the newer v2 syntax:

**Before:**
```python
class Config:
    from_attributes = True
```

**After:**
```python
from pydantic import BaseModel, ConfigDict

model_config = ConfigDict(from_attributes=True)
```

Files updated:
- `app/schemas/auth.py`
- `app/schemas/vulnerability.py`

## Verification
- Tested locally with Python 3.13 virtual environment
- Confirmed that `pydantic>=2.6.0` installs `pydantic-core==2.33.2` which is compatible with Python 3.13
- Updated schema syntax is compatible with newer pydantic versions

## Files Modified
1. `requirements.txt` - Updated pydantic version
2. `.python-version` - Added Python version specification
3. `app/schemas/auth.py` - Updated pydantic syntax
4. `app/schemas/vulnerability.py` - Updated pydantic syntax

## Deployment
The application should now deploy successfully on Heroku with Python 3.13 and the updated dependencies.