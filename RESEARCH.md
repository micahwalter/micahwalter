# Dynamic GitHub profile READMEs: The complete guide

GitHub profile READMEs that auto-update have become a powerful way to showcase real-time activity, releases, and content. The dominant approach uses **GitHub Actions with scheduled cron jobs** to run scripts that fetch data from APIs and regenerate markdown files. Simon Willison pioneered this pattern in July 2020, and since then an ecosystem of tools has emerged—from zero-configuration services like github-readme-stats to comprehensive solutions like lowlighter/metrics with 300+ customization options.

## Simon Willison's implementation set the standard

Simon Willison created the foundational self-updating profile README approach, publishing his method in July 2020. His system runs a **~150-line Python script via GitHub Actions every hour** that fetches data from three sources: GitHub releases via GraphQL API, blog posts via Atom feed parsing, and Today I Learned entries via his Datasette SQL API.

The key innovation in Willison's approach is using **GitHub's GraphQL API instead of REST** to efficiently query releases across his 300+ repositories. Where REST would require 300+ individual API calls, GraphQL retrieves all repository release data in just 3-4 paginated requests (100 repos per request). His GraphQL query structure fetches the latest release for each repository:

```graphql
query {
  viewer {
    repositories(first: 100, privacy: PUBLIC, after: AFTER) {
      pageInfo { hasNextPage, endCursor }
      nodes {
        name
        releases(last: 1) {
          nodes { name, publishedAt, url }
        }
      }
    }
  }
}
```

His workflow file (`.github/workflows/build.yml`) triggers on push, manual dispatch, and **cron schedule at 32 minutes past every hour** (`32 * * * *`)—deliberately offset from the top of the hour to avoid GitHub's peak load times. The workflow checks out the repo, installs Python dependencies including `python-graphql-client` and `feedparser`, runs the build script, and commits changes back if the README was modified.

The README uses **HTML comment markers as placeholders** for dynamic content injection:

```markdown
<!-- recent_releases starts -->
...dynamically generated content...
<!-- recent_releases ends -->
```

The Python script uses regex to find and replace content between these markers. This pattern has become the de facto standard for dynamic README generation.

**Key repositories:**
- Profile README: github.com/simonw/simonw
- Original blog post: simonwillison.net/2020/Jul/10/self-updating-profile-readme/
- Related TIL repo: github.com/simonw/til

## The ecosystem spans zero-config services to full customization

Dynamic GitHub profile tools fall into two categories: **serverless services requiring no setup** (just embed a URL) and **GitHub Action-based solutions** requiring workflow configuration.

**github-readme-stats** (77k+ stars) dominates the zero-configuration space. It renders SVG stats cards via Vercel serverless functions—simply embed a URL with your username and the image generates in real-time. No GitHub Actions needed:

```markdown
![Stats](https://github-readme-stats.vercel.app/api?username=YOUR_USERNAME)
```

**lowlighter/metrics** (15.7k+ stars) offers the most comprehensive customization with **30+ plugins** including achievements, language breakdowns, isometric calendars, and integrations with Spotify, WakaTime, Chess.com, and more. It requires GitHub Actions setup but provides stunning visual templates.

**Blog syndication** is handled by gautamkrishnar/blog-post-workflow, one of the top 20 most-installed GitHub Actions. It parses any RSS/Atom feed and supports multiple sources simultaneously—Dev.to, Medium, YouTube, StackOverflow, or custom blogs.

For **coding activity stats**, anmol098/waka-readme-stats integrates with WakaTime to display actual coding time by language, editor, and operating system—showing data beyond just GitHub commits.

**Visual engagement tools** include Platane/snk (animated snake "eating" your contribution graph), ryo-ma/github-profile-trophy (gamified achievement badges), and DenverCoder1/github-readme-streak-stats (streak counters for motivation).

| Tool | Stars | Setup | Update Method |
|------|-------|-------|---------------|
| github-readme-stats | 77k+ | URL only | Real-time |
| lowlighter/metrics | 15.7k+ | GitHub Action | Scheduled |
| github-profile-trophy | 6.3k+ | URL only | Real-time |
| blog-post-workflow | 3.2k+ | GitHub Action | Scheduled |
| waka-readme-stats | 3.8k+ | GitHub Action | Daily |

## GitHub Actions workflows power scheduled updates

The technical foundation for dynamic READMEs is a GitHub Actions workflow in your `username/username` repository. The workflow file lives at `.github/workflows/update-readme.yml` and typically includes three triggers: push events, manual dispatch, and cron schedule.

```yaml
name: Update README
on:
  push:
    branches: [main]
  workflow_dispatch:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM UTC

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v2
        with:
          python-version: 3.x
      - run: pip install -r requirements.txt
      - run: python build_readme.py
      - name: Commit changes
        run: |
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git config user.name "github-actions[bot]"
          git add -A
          git diff --staged --quiet || (git commit -m "Update README" && git push)
```

**Cron syntax uses five fields** representing minute (0-59), hour (0-23), day of month (1-31), month (1-12), and day of week (0-6). All times are UTC. Common schedules: `0 0 * * *` (daily midnight), `0 */6 * * *` (every 6 hours), `*/30 * * * *` (every 30 minutes). The minimum interval is 5 minutes.

Critical best practices for workflows:
- **Offset from top-of-hour**: Schedule at minutes like `:32` to avoid peak load delays
- **Always include workflow_dispatch**: Enables manual testing via GitHub UI
- **Check before committing**: The `git diff --staged --quiet ||` pattern prevents empty commits
- **Use permissions block**: `contents: write` explicitly grants push access
- **Cache dependencies**: `actions/cache@v3` reduces installation time

Scheduled workflows have limitations: they only run on the default branch, can be delayed during high-load periods, and **automatically disable after 60 days of repository inactivity**.

## API strategies determine efficiency and capability

The GitHub API offers two approaches: REST for simple queries and **GraphQL for complex, batched requests**. For profile READMEs fetching data across many repositories, GraphQL dramatically reduces API calls.

**REST API endpoints** useful for profile READMEs:
- `GET /users/{username}/repos` — list repositories
- `GET /users/{username}/events` — recent activity
- `GET /repos/{owner}/{repo}/releases/latest` — latest release

**GraphQL enables single-request data aggregation**. This query fetches recent repositories with details:

```graphql
{
  user(login: "username") {
    repositories(first: 10, orderBy: {field: UPDATED_AT, direction: DESC}) {
      nodes {
        name
        description
        url
        stargazerCount
        primaryLanguage { name }
      }
    }
  }
}
```

For contribution data:

```graphql
{
  user(login: "username") {
    contributionsCollection {
      totalCommitContributions
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays { contributionCount, date }
        }
      }
    }
  }
}
```

**Rate limits**: Unauthenticated requests allow 60/hour; authenticated requests allow **5,000/hour** for both REST and GraphQL. The built-in `${{ secrets.GITHUB_TOKEN }}` works for most profile README use cases. For cross-repository access, create a Personal Access Token with minimal scopes.

## Template replacement patterns make generation straightforward

The dominant implementation pattern uses **HTML comment markers in the README** as placeholders, with a script replacing content between markers. This approach preserves static content while updating dynamic sections.

Python replacement function:

```python
import re

def replace_chunk(content, marker, chunk):
    pattern = re.compile(
        r'<!-- {} starts -->.*<!-- {} ends -->'.format(marker, marker),
        re.DOTALL
    )
    replacement = '<!-- {} starts -->\n{}\n<!-- {} ends -->'.format(
        marker, chunk, marker
    )
    return pattern.sub(replacement, content)
```

**RSS feed parsing** for blog posts uses feedparser:

```python
import feedparser

entries = feedparser.parse('https://blog.example.com/feed/')['entries'][:5]
posts = '\n'.join([f"- [{e['title']}]({e['link']})" for e in entries])
```

For JavaScript/Node.js implementations, the `rss-parser` package provides equivalent functionality. TypeScript projects often use `markdown-it` for markdown generation.

**Pre-built Actions simplify common use cases**:
- `gautamkrishnar/blog-post-workflow` — RSS feed integration
- `jamesgeorge007/github-activity-readme` — activity feed display  
- `Platane/snk` — contribution snake animation

## Design patterns that work well for profile READMEs

Content types with proven engagement fall into several categories. **Activity-based content** works best with frequent updates: recent commits, pull requests, issues opened, and stars given. The GitHub Events API (`/users/{username}/events`) provides this data, and tools like github-activity-readme format it automatically.

**Stats and metrics** create visual interest: contribution counts, language breakdowns, streak counters, and achievement trophies. These typically use SVG rendering for clean presentation. The Vercel-hosted services (github-readme-stats, profile-trophy) generate these in real-time without requiring GitHub Actions.

**External integrations** add personality: Spotify now-playing widgets, WakaTime coding time, blog post feeds, and YouTube video lists. These require OAuth tokens stored in repository secrets.

Recommended update frequencies by content type:

| Content | Frequency | Rationale |
|---------|-----------|-----------|
| Blog posts | Daily | New posts are infrequent |
| GitHub activity | 6-12 hours | Balances freshness with API usage |
| Stats/metrics | Daily | Changes are gradual |
| Releases | Hourly (high activity) or daily | Depends on release frequency |

**Visual elements that enhance profiles**: contribution snake animations, trophy displays, language pie charts, and streak counters. The `<picture>` tag enables dark/light mode variants:

```markdown
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="snake-dark.svg">
  <img src="snake-light.svg">
</picture>
```

## Conclusion

Building a dynamic GitHub profile README requires three components: a workflow file triggering on schedule, a script fetching and formatting data, and marker comments in your README for content injection. Simon Willison's GraphQL-based approach remains the most efficient for users with many repositories, while zero-config services like github-readme-stats offer instant setup for common visualizations.

The most impactful implementations combine multiple data sources—GitHub activity, blog feeds, and external services—updated at appropriate frequencies. Key technical decisions include choosing GraphQL over REST for batched queries, offsetting cron schedules from peak times, and implementing conditional commits to avoid empty commit history. The ecosystem has matured significantly since 2020, with lowlighter/metrics offering the most comprehensive customization and github-readme-stats providing the easiest entry point.

**Essential repositories to explore:**
- github.com/simonw/simonw — the original implementation
- github.com/lowlighter/metrics — comprehensive visualization
- github.com/anuraghazra/github-readme-stats — most popular stats service
- github.com/abhisheknaiidu/awesome-github-profile-readme — curated examples