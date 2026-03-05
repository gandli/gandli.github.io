# Fix for Hugo OpenGraph postAudio Issue

## Problem Analysis

The build is failing because Hugo's built-in OpenGraph template (`_internal/opengraph.html`) is trying to iterate over the `postAudio` parameter, but it's being treated as a string path `/audio/2026-03-04-day14.en.mp3` instead of an array or object.

The error occurs in:
```
template: _internal/opengraph.html:45:22: executing "_internal/opengraph.html" at <6>: range can't iterate over /audio
```

This suggests that Hugo's internal OpenGraph template expects certain parameters to be arrays, but `postAudio` is a string.

## Solution

The issue is that the Dream theme doesn't properly handle custom frontmatter parameters like `postAudio` in the OpenGraph template. We need to override the built-in OpenGraph template to handle this properly.

### Step 1: Create custom OpenGraph template

Create the directory and file:
```bash
mkdir -p layouts/_internal
```

### Step 2: Copy and modify the built-in template

We'll create a custom `_internal/opengraph.html` that safely handles the `postAudio` parameter without trying to iterate over it.