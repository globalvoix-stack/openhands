# IMPORTANT: LEGACY V0 CODE - Deprecated since version 1.0.0, scheduled for removal April 1, 2026
# This file is part of the legacy (V0) implementation of Thinksoft and will be removed soon as we complete the migration to V1.
# Thinksoft V1 uses the Software Agent SDK for the agentic core and runs a new application server. Please refer to:
#   - V1 agentic core (SDK): https://github.com/Thinksoft/software-agent-sdk
#   - V1 application server (in this repo): thinksoft/app_server/
# Unless you are working on deprecation, please avoid extending this legacy file and consult the V1 codepaths above.
# Tag: Legacy-V0
# This module belongs to the old V0 web server. The V1 application server lives under thinksoft/app_server/.
from thinksoft.core.config.thinksoft_config import ThinksoftConfig
from thinksoft.events.event import Event


class MonitoringListener:
    """Abstract base class for monitoring application activity.

    This is an extension point in Thinksoft that allows applications to customize how
    application activity is monitored. Applications can substitute their own implementation by:
    1. Creating a class that inherits from MonitoringListener
    2. Implementing desired methods (all methods have default no-op implementations)
    3. Setting server_config.monitoring_listener_class to the fully qualified name of the class

    The class is instantiated via get_impl() in thinksoft.server.shared.py.

    Implementations should be non-disruptive, do not raise or block to perform I/O.
    """

    def on_session_event(self, event: Event) -> None:
        """Track metrics about events being added to a Session's EventStream."""
        pass

    def on_agent_session_start(self, success: bool, duration: float) -> None:
        """Track an agent session start.
        Success is true if startup completed without error.
        Duration is start time in seconds observed by AgentSession.
        """
        pass

    def on_create_conversation(self) -> None:
        """Track the beginning of conversation creation.
        Does not currently capture whether it succeed.
        """
        pass

    @classmethod
    def get_instance(
        cls,
        config: ThinksoftConfig,
    ) -> 'MonitoringListener':
        return cls()
