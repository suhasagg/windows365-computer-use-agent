# Human Takeover
A production UI should expose live screenshare using the supported Windows 365 supervision path. Agent execution transitions RUNNING -> PAUSED_FOR_HUMAN -> HUMAN_CONTROL. Agent tool calls are rejected while the human owns the session. On return, capture a new screenshot/UI tree, invalidate stale plans/coordinates, and replan from observed state.
