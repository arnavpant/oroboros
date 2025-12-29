from ddtrace import tracer

def traced(name):
    def wrapper(fn):
        def inner(*args, **kwargs):
            with tracer.trace(name) as span:
                result = fn(*args, **kwargs)
                span.set_tag("output_length", len(str(result)))
                return result
        return inner
    return wrapper
