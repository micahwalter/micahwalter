# Dynamic GitHub Profile README - Implementation Spec

## Overview

This document outlines the implementation plan for transforming the micahwalter GitHub profile README from a static page into a dynamic, self-updating profile that showcases real-time activity, content, and projects.

## Technical Approach

Following Simon Willison's proven pattern, we'll implement:

1. **GitHub Actions workflow** that runs on a schedule
2. **Python script** to fetch data from various APIs and generate markdown
3. **HTML comment markers** in README.md as content injection points
4. **Conditional commits** to avoid empty commits when content hasn't changed

## Architecture

### Workflow Configuration

**File**: `.github/workflows/update-readme.yml`

**Triggers**:
- Push to main branch (for testing)
- Manual dispatch (for on-demand updates)
- Cron schedule: `32 */6 * * *` (every 6 hours at :32 minutes past the hour)

**Permissions**: `contents: write` to allow automated commits

**Steps**:
1. Checkout repository
2. Setup Python 3.x
3. Install dependencies from `requirements.txt`
4. Run `build_readme.py`
5. Commit and push changes if README was modified

### Build Script

**File**: `build_readme.py`

**Core functionality**:
- Read current README.md
- Fetch data from configured sources
- Generate markdown content
- Replace content between HTML comment markers
- Write updated README.md

**Pattern for content replacement**:
```python
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

## Dynamic Content Sections

### 1. Introduction/Bio (Static)
- Brief personal introduction
- Links to website, social media, contact
- **Update frequency**: Manual/as needed

### 2. Recent GitHub Activity
**Marker**: `recent_activity`

**Data source**: GitHub Events API (`/users/micahwalter/events`)

**Content**:
- Recent commits across repositories
- Pull requests opened/merged
- Issues opened
- Repositories starred

**Display**: Bulleted list of 5-10 most recent activities

**Update frequency**: Every 6 hours

**Implementation**:
```python
import requests

def fetch_recent_activity():
    url = 'https://api.github.com/users/micahwalter/events/public'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    events = response.json()[:10]
    # Parse and format events
    return formatted_markdown
```

### 3. Recent Blog Posts
**Marker**: `recent_posts`

**Data source**: RSS/Atom feed from personal blog

**Content**:
- 5 most recent blog posts
- Title and link for each

**Display**:
```markdown
- [Post Title](https://example.com/post)
```

**Update frequency**: Daily (blog posts are infrequent)

**Implementation**:
```python
import feedparser

def fetch_blog_posts(feed_url):
    entries = feedparser.parse(feed_url)['entries'][:5]
    return '\n'.join([
        f"- [{e['title']}]({e['link']})"
        for e in entries
    ])
```

### 4. Featured Projects
**Marker**: `featured_projects`

**Data source**: GitHub GraphQL API

**Content**:
- 3-5 pinned or featured repositories
- Name, description, language, stars

**Display**:
```markdown
### [Project Name](url)
Description text
**Language**: Python | **Stars**: 123
```

**Update frequency**: Daily

**GraphQL query**:
```graphql
{
  user(login: "micahwalter") {
    pinnedItems(first: 6, types: REPOSITORY) {
      nodes {
        ... on Repository {
          name
          description
          url
          stargazerCount
          primaryLanguage { name }
        }
      }
    }
  }
}
```

### 5. Recent Releases
**Marker**: `recent_releases`

**Data source**: GitHub GraphQL API

**Content**:
- Latest releases across all public repositories
- Release name, repository, date

**Display**:
```markdown
- [release-name](url) in [repo-name](repo-url) - *Dec 19, 2025*
```

**Update frequency**: Every 6 hours (or daily depending on release frequency)

**GraphQL query**: (Similar to Simon Willison's approach)
```graphql
{
  user(login: "micahwalter") {
    repositories(first: 100, privacy: PUBLIC, orderBy: {field: UPDATED_AT, direction: DESC}) {
      nodes {
        name
        releases(last: 1) {
          nodes {
            name
            publishedAt
            url
          }
        }
      }
    }
  }
}
```

### 6. Stats Visualizations (Optional)
**Zero-config services** (no workflow needed, just embed URLs):

**GitHub Stats Card**:
```markdown
![Stats](https://github-readme-stats.vercel.app/api?username=micahwalter&show_icons=true&theme=default)
```

**Language Stats**:
```markdown
![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=micahwalter&layout=compact)
```

**Update frequency**: Real-time (rendered on-demand by Vercel)

## README.md Template Structure

```markdown
# Hi, I'm Micah Walter

[Brief bio and introduction - static content]

## Recent Activity

<!-- recent_activity starts -->
This content will be automatically updated
<!-- recent_activity ends -->

## Recent Blog Posts

<!-- recent_posts starts -->
This content will be automatically updated
<!-- recent_posts ends -->

## Featured Projects

<!-- featured_projects starts -->
This content will be automatically updated
<!-- featured_projects ends -->

## Recent Releases

<!-- recent_releases starts -->
This content will be automatically updated
<!-- recent_releases ends -->

## GitHub Stats

![Stats](https://github-readme-stats.vercel.app/api?username=micahwalter&show_icons=true)

## Connect

[Links to social media, website, etc. - static content]
```

## Dependencies

**File**: `requirements.txt`
```
requests
feedparser
python-dateutil
```

For GraphQL:
```
python-graphql-client
```

Or use `requests` directly with GraphQL endpoint.

## Environment Variables / Secrets

**GITHUB_TOKEN**: Use built-in `${{ secrets.GITHUB_TOKEN }}` for GitHub API access
- Provides 5,000 requests/hour
- Has read access to public repositories
- Automatically available in GitHub Actions

**BLOG_FEED_URL**: RSS/Atom feed URL (can be hardcoded in script or set as environment variable)

## Implementation Phases

### Phase 1: Setup Infrastructure
- Create `.github/workflows/update-readme.yml`
- Create `build_readme.py` with basic structure
- Add HTML comment markers to README.md
- Test workflow with manual dispatch

### Phase 2: Implement GitHub Activity
- Add GitHub Events API integration
- Parse and format activity events
- Implement content replacement for `recent_activity` marker
- Test and verify

### Phase 3: Add Blog Posts
- Add RSS feed parsing
- Implement content replacement for `recent_posts` marker
- Handle edge cases (feed unavailable, malformed entries)

### Phase 4: Featured Projects
- Implement GraphQL query for pinned repositories
- Format project display
- Add to README generation

### Phase 5: Recent Releases
- Implement GraphQL query for releases across repositories
- Filter and sort releases by date
- Format release list
- Add to README generation

### Phase 6: Polish and Optimization
- Add error handling and logging
- Optimize API calls (use GraphQL for batched queries)
- Add caching if needed to avoid redundant API calls
- Document configuration options

## Best Practices

1. **Offset cron schedule**: Use `:32` minutes to avoid GitHub's peak load times
2. **Conditional commits**: Only commit if content actually changed
3. **Error handling**: Gracefully handle API failures (don't break the build)
4. **Rate limiting**: Monitor API usage, use GraphQL for efficiency
5. **Token security**: Never hardcode tokens, use GitHub secrets
6. **Testing**: Always include `workflow_dispatch` for manual testing

## Customization Options

After initial implementation, consider:

- **WakaTime integration**: Show coding activity and time spent
- **Spotify now-playing**: Display currently listening to
- **Contribution snake**: Animated visualization of contribution graph
- **Dark/light mode variants**: Use `<picture>` tag for theme-aware images
- **Achievement badges**: Trophy/badge displays for milestones

## Success Metrics

- Workflow runs successfully on schedule
- No empty commits
- Content updates within expected timeframes
- API rate limits not exceeded
- README displays correctly on GitHub profile

## References

- [Simon Willison's implementation](https://github.com/simonw/simonw)
- [Simon's blog post](https://simonwillison.net/2020/Jul/10/self-updating-profile-readme/)
- [GitHub REST API](https://docs.github.com/en/rest)
- [GitHub GraphQL API](https://docs.github.com/en/graphql)
- [Awesome GitHub Profile README](https://github.com/abhisheknaiidu/awesome-github-profile-readme)
