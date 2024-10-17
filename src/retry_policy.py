from langgraph.pregel import RetryPolicy

retry_policy = RetryPolicy(max_attempts=3, backoff_factor=2.0)
