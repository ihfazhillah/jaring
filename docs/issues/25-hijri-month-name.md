# Issue 25: Convert Hijri Month Number to Name

## Description

The post date currently displays the month as a number (e.g., "1447-02-01"). This should be converted to the actual Hijri month name (e.g., "1 Safar 1447") to be more user-friendly and readable.

## Acceptance Criteria

- A function needs to be created that takes a Hijri date string (e.g., "1447-02-01") as input.
- This function will use a library like `hijri-converter` or a simple mapping to convert the month number to its corresponding name (e.g., 1 -> Muharram, 2 -> Safar).
- The `parse_file` function should be updated to use this new function to format the date.
- The formatted date should be passed to the templates and displayed on both the index and message pages.
