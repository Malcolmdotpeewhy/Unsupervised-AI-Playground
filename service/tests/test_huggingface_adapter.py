import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from huggingface_adapter import HuggingFaceAdapterLayer

@pytest.fixture
def adapter():
    return HuggingFaceAdapterLayer()

def test_gguf_resolution(adapter):
    # Testing a repo containing GGUF models
    result = adapter.evaluate_execution_engine("City96/Flux.1-schnell-gguf")
    assert result["backend"] == "llama_cpp"
    assert result["engine"] == "GGML"

def test_openvino_resolution(adapter):
    # Testing a standard OpenVINO optimized conversational or whisper model
    result = adapter.evaluate_execution_engine("OpenVINO/whisper-large-v3-int4-ov")
    assert result["backend"] == "openvino"
    assert result["engine"] == "OpenVINO"

def test_comfyui_resolution(adapter):
    # Testing a standard Diffusers Checkpoint node
    result = adapter.evaluate_execution_engine("runwayml/stable-diffusion-v1-5")
    assert result["backend"] == "comfyui"
    assert result["engine"] == "Diffusers"
    assert result["pipeline_tag"] in ["text-to-image", "image-to-image"] or "stable-diffusion" in result["pipeline_tag"].lower()

def test_failed_resolution(adapter):
    # Testing an invalid or pure transformers fallback repo
    result = adapter.evaluate_execution_engine("gpt2")
    # GPT2 is a text-generation transformers model
    assert result["backend"] == "transformers"
    assert result["engine"] == "Transformers"
