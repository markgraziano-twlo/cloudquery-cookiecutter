import sys
import signal
from cloudquery.sdk import serve
from plugin import ExamplePlugin

import structlog
logger = structlog.getLogger(__name__)

def signal_handler(sig, frame):
    logger.debug("Caught signal %s, exiting" % sig)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    p = ExamplePlugin()
    serve.PluginCommand(p).run(sys.argv[1:])


if __name__ == "__main__":
    main()
