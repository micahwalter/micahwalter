#!/usr/bin/env python3
"""
Build script for dynamic GitHub profile README
Fetches data from various APIs and updates README.md with dynamic content
"""

import os
import re
import sys
from datetime import datetime
from typing import List, Dict, Any
import requests
import feedparser
from dateutil import parser as date_parser


# Configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
GITHUB_USERNAME = 'micahwalter'
BLOG_FEED_URL = os.environ.get('BLOG_FEED_URL', '')  # Set this to your blog's RSS/Atom feed
README_PATH = 'README.md'


def replace_chunk(content: str, marker: str, chunk: str) -> str:
    """Replace content between HTML comment markers"""
    pattern = re.compile(
        r'<!-- {} starts -->.*<!-- {} ends -->'.format(marker, marker),
        re.DOTALL
    )
    replacement = '<!-- {} starts -->\n{}\n<!-- {} ends -->'.format(
        marker, chunk, marker
    )
    new_content = pattern.sub(replacement, content)
    if new_content == content:
        print(f"Warning: Marker '{marker}' not found in README")
    return new_content


def fetch_github_activity() -> str:
    """Fetch recent GitHub activity using Events API"""
    url = f'https://api.github.com/users/{GITHUB_USERNAME}/events/public'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        events = response.json()[:10]

        activities = []
        for event in events:
            event_type = event['type']
            repo = event['repo']['name']
            created_at = date_parser.parse(event['created_at'])
            date_str = created_at.strftime('%b %d, %Y')

            if event_type == 'PushEvent':
                commits = event['payload'].get('commits', [])
                commit_count = len(commits)
                if commit_count > 0:
                    activities.append(f"- Pushed {commit_count} commit{'s' if commit_count != 1 else ''} to [{repo}](https://github.com/{repo}) - *{date_str}*")
                else:
                    activities.append(f"- Pushed to [{repo}](https://github.com/{repo}) - *{date_str}*")
            elif event_type == 'PullRequestEvent':
                action = event['payload']['action']
                pr_number = event['payload']['pull_request']['number']
                activities.append(f"- {action.capitalize()} pull request [#{pr_number}](https://github.com/{repo}/pull/{pr_number}) in {repo} - *{date_str}*")
            elif event_type == 'IssuesEvent':
                action = event['payload']['action']
                issue_number = event['payload']['issue']['number']
                activities.append(f"- {action.capitalize()} issue [#{issue_number}](https://github.com/{repo}/issues/{issue_number}) in {repo} - *{date_str}*")
            elif event_type == 'WatchEvent':
                activities.append(f"- Starred [{repo}](https://github.com/{repo}) - *{date_str}*")
            elif event_type == 'CreateEvent':
                ref_type = event['payload'].get('ref_type', 'repository')
                activities.append(f"- Created {ref_type} in [{repo}](https://github.com/{repo}) - *{date_str}*")

        if not activities:
            return "*No recent activity*"

        return '\n'.join(activities[:8])

    except Exception as e:
        print(f"Error fetching GitHub activity: {e}")
        return "*Unable to fetch recent activity*"


def fetch_blog_posts() -> str:
    """Fetch recent blog posts from RSS/Atom feed"""
    if not BLOG_FEED_URL:
        return "*Blog feed URL not configured*"

    try:
        feed = feedparser.parse(BLOG_FEED_URL)
        entries = feed.entries[:5]

        if not entries:
            return "*No recent blog posts*"

        posts = []
        for entry in entries:
            title = entry.get('title', 'Untitled')
            link = entry.get('link', '#')
            posts.append(f"- [{title}]({link})")

        return '\n'.join(posts)

    except Exception as e:
        print(f"Error fetching blog posts: {e}")
        return "*Unable to fetch blog posts*"


def graphql_query(query: str) -> Dict[str, Any]:
    """Execute a GraphQL query against GitHub API"""
    url = 'https://api.github.com/graphql'
    headers = {
        'Authorization': f'bearer {GITHUB_TOKEN}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json={'query': query}, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_featured_projects() -> str:
    """Fetch pinned repositories using GraphQL"""
    if not GITHUB_TOKEN:
        return "*GitHub token required for featured projects*"

    query = """
    {
      user(login: "%s") {
        pinnedItems(first: 6, types: REPOSITORY) {
          nodes {
            ... on Repository {
              name
              description
              url
              stargazerCount
              primaryLanguage {
                name
              }
            }
          }
        }
      }
    }
    """ % GITHUB_USERNAME

    try:
        result = graphql_query(query)

        if 'errors' in result:
            print(f"GraphQL errors: {result['errors']}")
            return "*Unable to fetch featured projects*"

        pinned_items = result['data']['user']['pinnedItems']['nodes']

        if not pinned_items:
            return "*No pinned repositories*"

        projects = []
        for repo in pinned_items:
            name = repo['name']
            description = repo.get('description', 'No description provided')
            url = repo['url']
            stars = repo['stargazerCount']
            language = repo.get('primaryLanguage', {})
            lang_name = language.get('name', 'Unknown') if language else 'Unknown'

            project_md = f"### [{name}]({url})\n{description}\n\n**Language**: {lang_name} | **Stars**: {stars}"
            projects.append(project_md)

        return '\n\n'.join(projects)

    except Exception as e:
        print(f"Error fetching featured projects: {e}")
        return "*Unable to fetch featured projects*"


def fetch_recent_releases() -> str:
    """Fetch recent releases across all repositories using GraphQL"""
    if not GITHUB_TOKEN:
        return "*GitHub token required for releases*"

    query = """
    {
      user(login: "%s") {
        repositories(first: 100, privacy: PUBLIC, orderBy: {field: UPDATED_AT, direction: DESC}) {
          nodes {
            name
            url
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
    """ % GITHUB_USERNAME

    try:
        result = graphql_query(query)

        if 'errors' in result:
            print(f"GraphQL errors: {result['errors']}")
            return "*Unable to fetch releases*"

        repositories = result['data']['user']['repositories']['nodes']

        # Collect all releases
        all_releases = []
        for repo in repositories:
            repo_name = repo['name']
            repo_url = repo['url']
            releases = repo.get('releases', {}).get('nodes', [])

            for release in releases:
                release_name = release.get('name', 'Unnamed Release')
                published_at = date_parser.parse(release['publishedAt'])
                release_url = release['url']

                all_releases.append({
                    'name': release_name,
                    'repo_name': repo_name,
                    'repo_url': repo_url,
                    'published_at': published_at,
                    'url': release_url
                })

        # Sort by published date (newest first)
        all_releases.sort(key=lambda x: x['published_at'], reverse=True)

        # Take top 10
        recent_releases = all_releases[:10]

        if not recent_releases:
            return "*No recent releases*"

        releases_md = []
        for release in recent_releases:
            date_str = release['published_at'].strftime('%b %d, %Y')
            releases_md.append(
                f"- [{release['name']}]({release['url']}) in [{release['repo_name']}]({release['repo_url']}) - *{date_str}*"
            )

        return '\n'.join(releases_md)

    except Exception as e:
        print(f"Error fetching releases: {e}")
        return "*Unable to fetch releases*"


def main():
    """Main function to update README"""
    print("Starting README update...")

    # Read current README
    try:
        with open(README_PATH, 'r', encoding='utf-8') as f:
            readme_content = f.read()
    except FileNotFoundError:
        print(f"Error: {README_PATH} not found")
        sys.exit(1)

    # Fetch data from various sources
    print("Fetching GitHub activity...")
    activity = fetch_github_activity()

    print("Fetching blog posts...")
    blog_posts = fetch_blog_posts()

    print("Fetching featured projects...")
    featured_projects = fetch_featured_projects()

    print("Fetching recent releases...")
    releases = fetch_recent_releases()

    # Replace content
    readme_content = replace_chunk(readme_content, 'recent_activity', activity)
    readme_content = replace_chunk(readme_content, 'recent_posts', blog_posts)
    readme_content = replace_chunk(readme_content, 'featured_projects', featured_projects)
    readme_content = replace_chunk(readme_content, 'recent_releases', releases)

    # Write updated README
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print("README updated successfully!")


if __name__ == '__main__':
    main()
