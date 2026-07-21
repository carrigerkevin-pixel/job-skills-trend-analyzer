# Project Notes

## Known Data Limitations

- Adzuna's free-tier API truncates job descriptions to ~500 characters.
  This means skill extraction only sees the beginning portion of each
  posting, likely undercounting skills mentioned later (e.g. in
  "requirements" or "qualifications" sections).
- Skill trend counts should be read as directional signals based on
  visible text, not exhaustive skill coverage.
- Possible future improvement: scrape full descriptions from the
  `redirect_url` field for a sample of postings.