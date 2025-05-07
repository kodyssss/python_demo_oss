from flask import Flask
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from .routes import init_routes

def init_tracing():
    # Set up the tracer provider with service name
    trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": "backend"})))
    tracer_provider = trace.get_tracer_provider()

    # Configure Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name='jaeger',
        agent_port=6831,
    )

    # Add span processor to export traces to Jaeger
    span_processor = BatchSpanProcessor(jaeger_exporter)
    tracer_provider.add_span_processor(span_processor)

    # Instrument Flask and requests
    FlaskInstrumentor().instrument()
    RequestsInstrumentor().instrument()

def init_app():
    app = Flask(__name__)
    init_tracing()  # Initialize tracing
    init_routes(app)
    return app
