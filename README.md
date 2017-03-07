# pygster_logparsers
Parsers for pygster https://pypi.python.org/pypi/pygster

Usage:

`pygster [options] pygster_logparsers.PARSER logfile`

For use Sentry add dsn in parser-options:

`pygster [options] --parser-options '--sentry_dsn {SENTRY_DSN}' pygster_logparsers.PARSER logfile`

PARSER is only HAProxyPygster on this moment...

pygster options like as `logster` https://github.com/etsy/logster
