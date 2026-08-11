# Project Notes

## Known Data Limitations

- Adzuna's free-tier API truncates job descriptions to ~500 characters,
  meaning skill extraction only sees the beginning portion of each
  posting.
- Investigated fetching full descriptions via each posting's `redirect_url`
  using `trafilatura`. Testing showed Adzuna's redirect pages
  (`adzuna.com/land/ad/...`) consistently fail to return content to
  automated fetchers, likely due to bot detection or JS-based redirects —
  this held true across both old and recently-collected postings, not just
  expired ones.
- Decision: not pursuing this further, since defeating Adzuna's bot
  protection would require a significant, disproportionate time investment
  (headless browser automation, header spoofing) for a data source that
  isn't designed to be scraped this way. Skill trend counts are documented
  as directional signals based on visible (truncated) text, not exhaustive
  coverage.
  
## Resolved: Database Sync Across Environments

Originally, this project used a local SQLite file tracked in git,
shared across local dev, GitHub Actions, and Docker — which caused
sync conflicts (e.g. an automated run could overwrite local data).

**Fix:** migrated to a hosted PostgreSQL database (Neon). All
environments (local, GitHub Actions, Streamlit Cloud, Docker) now
connect to the same database via a `DATABASE_URL` environment
variable, eliminating sync issues entirely.