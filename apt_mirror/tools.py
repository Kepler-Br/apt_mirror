import urllib.parse


def join_url(first: str, *args: str) -> str:
    out = first
    for arg in args:
        if not out.endswith('/'):
            out = out + '/'
        out = urllib.parse.urljoin(out, arg)
    return out
