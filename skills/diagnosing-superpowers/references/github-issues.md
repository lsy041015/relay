# GitHub issues

Search Relay first. If the evidence points to unchanged upstream behavior,
search [Superpowers issues](https://github.com/obra/superpowers/issues) as
read-only background. File in the upstream repository only when the user
explicitly requests that destination.

Use `gh` when installed and authenticated. Otherwise use the public API or
give the user a browser URL. Issue creation requires the user's explicit
authorization.

## Search Relay

```bash
gh search issues --repo lsy041015/relay --limit 10 "<terms>" \
  --json number,state,title --jq '.[] | "\(.number)\t\(.state)\t\(.title)"'
```

Without `gh`, use the public API. URL-encode the search terms:

```bash
curl -s -H "Accept: application/vnd.github+json" \
  "https://api.github.com/search/issues?q=repo:lsy041015/relay+is:issue+<url-encoded terms>&per_page=10"
```

Without `curl`, hand over
`https://github.com/lsy041015/relay/issues?q=<url-encoded terms>`.

## File in Relay

Write the filled `templates/issue.md` to the workspace and show the exact
text. After the user approves the issue and destination:

```bash
gh issue create --repo lsy041015/relay --title "<title>" --body-file <path>
```

Do not assume a label or issue template exists. `gh` cannot attach files:
give the user the bundle path to attach through the browser if needed.

Without `gh`, hand over a prefilled URL:

```text
https://github.com/lsy041015/relay/issues/new?title=<url-encoded title>&body=<url-encoded body>
```

If the URL is too long, include only the title and ask the user to paste the
body from the saved file.
