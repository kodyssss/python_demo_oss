from flask import Flask
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from .routes import create_app

def init_tracing():
    trace.set_tracer_provider(TracerProvider())
    tracer_provider = trace.get_tracer_provider()
    jaeger_exporter = JaegerExporter(
        agent_host_name='jaeger',
        agent_port=6831,
    )
    span_processor = BatchSpanProcessor(jaeger_exporter)
    tracer_provider.add_span_processor(span_processor)
    FlaskInstrumentor().instrument()

def init_app():
    init_tracing()
    return create_app()