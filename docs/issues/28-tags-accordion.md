# Issue 28: Accordion-Style Tag Display

## Description

The current tag display shows all tags at once. To create a cleaner interface, especially when there are many tags, this should be converted into an accordion-style display. By default, it should show only the first 5 tags, with an option to expand and show all of them.

## Acceptance Criteria

- The tag list on the index page should be modified to initially display only the first 5 tags.
- A "Show More" button or link should be present if there are more than 5 tags.
- When the "Show More" button is clicked, the container should expand to show all the tags.
- The button text should then change to "Show Less".
- Clicking "Show Less" should collapse the list back to showing only the first 5 tags.
- This functionality should be implemented using JavaScript for a dynamic user experience.
